import json
import logging
import random
import platform
import time
import traceback
import undetected_chromedriver

from bs4 import BeautifulSoup
from ctypes import c_int
from multiprocess import Process, Manager, Lock, Value
from pyvirtualdisplay import Display
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import RetryLimitExceedException, PageEmptyException


class UpworkJobScrapeManager:
    def __init__(self, initial_url, webdriver_dir, browser_dir, use_vdisplay, total_job_scrape, jobs_one_page, min_sleep_sec, max_sleep_sec, pageload_timeout, concurrency_factor, output_dir):
        self.min_sleep_sec = min_sleep_sec
        self.max_sleep_sec = max_sleep_sec
        self.pageload_timeout = pageload_timeout

        self.init_url = initial_url
        self.jobs_one_page = jobs_one_page
        self.total_job_scrape = total_job_scrape
        self.output_dir = output_dir

        self.webdriver_dir = webdriver_dir
        self.browser_dir = browser_dir
        self.use_vdisplay = use_vdisplay

        self.manager = Manager()
        self.scraped_job_ls = self.manager.list()
        self.init_lock = Lock()
        self.concurrency_factor = concurrency_factor
        self.ps = []
        self.page_empty_markers = []
        self.assigned_pagenum = 0
        self.inner_retry_times = 3
    
    def _random_sleep(self):
        sleep_duration = random.uniform(self.min_sleep_sec, self.max_sleep_sec)
        time.sleep(sleep_duration)
    
    def _handle_job_detail_page(self, driver, detail_url, scraped_ls):
        job_desc = {}
        driver.get(detail_url)
        expertises = set()
        WebDriverWait(driver, self.pageload_timeout).until(
            EC.all_of(
                EC.presence_of_element_located((By.XPATH, "//h4[@class='m-0']")),
                EC.presence_of_element_located((By.XPATH, "//header[@class='air3-card-section py-4x']")),
                EC.presence_of_element_located((By.XPATH, "//p[@class='text-body-sm']")),
                EC.presence_of_element_located((By.XPATH, "//p[@class='footer-copy']")),
            )
        )
        self._random_sleep()
        title_element = driver.find_element(By.XPATH, "//h4[@class='m-0']")
        job_desc["title"] = title_element.text.strip()

        job_desc["url"] = detail_url
        job_desc["scraped_ts"] = time.time()

        detail_element = driver.find_element(By.XPATH, "//p[@class='text-body-sm']")
        job_desc["description"] = detail_element.text.strip()

        header_element = driver.find_element(By.XPATH, "//header[@class='air3-card-section py-4x']")
        if "Only freelancers located in the U.S. may apply." in header_element.get_attribute("outerHTML") \
            or "U.S. located freelancers only" in header_element.get_attribute("outerHTML"):
            job_desc["area_restriction"] = "US Only"
        elif "Worldwide" in header_element.get_attribute("outerHTML"):
            job_desc["area_restriction"] = "Global"
        else:
            raise

        soup_wholepage = BeautifulSoup(driver.page_source, "html.parser")
        skills = soup_wholepage.find_all("span", {"class": "air3-badge air3-badge-highlight badge disabled"})
        for skill in skills:
            expertises.add(skill.text.strip())
        if '' in expertises:
            logging.warning(f"found empty str in expertise like {expertises}, original skills like {skills}, job_url {detail_url}")
        job_desc["skill_and_expertise"] = list(expertises)
        job_feature_elements = driver.find_elements(By.XPATH, "//li[@data-v-ad039828='']")
        job_feature = dict.fromkeys(
            [
                "Contract To Fulltime",
                "Duration",
                "Estimated Job Duration",
                "Estimated Job Pay",
                "Experience Level", 
                "Fixed-price",
                "Project Type", 
                "Remote Type",
            ], None
        )
        for i in range(len(job_feature_elements)):
            job_feature_element_src = job_feature_elements[i].get_attribute("outerHTML")
            soup_jobfeature = BeautifulSoup(job_feature_element_src, "html.parser")
            desc_text = soup_jobfeature.find("strong", {"data-v-ad039828": ""})
            description = soup_jobfeature.find("div", {"class": "description"})
            if description:
                description = description.text.strip()
            else:
                description = ""
            if description in ["Project Type", "Experience Level", "Duration", "Fixed-price"]:
                job_feature[description] = desc_text.text.strip()
            elif "This job has the potential to turn into a full time role" in description:
                job_feature["Contract To Fulltime"] = True
            else:
                icon_name = soup_jobfeature.find("div", {"class": "air3-icon md"})["data-cy"]
                if icon_name == "clock-hourly":
                    job_feature["Estimated Job Duration"] = desc_text.text.strip()
                elif icon_name == "clock-timelog":
                    pay_elems = soup_jobfeature.find_all("p", {"class": "m-0"})
                    pay_lower = pay_elems[0].find("strong", {"data-v-ad039828": ""}).text.strip()
                    pay_upper = pay_elems[-1].find("strong", {"data-v-ad039828": ""}).text.strip()
                    job_feature["Estimated Job Pay"] = f"{pay_lower} ~ {pay_upper}"
                elif icon_name == "local":
                    job_feature["Remote Type"] = desc_text.text.strip()
                else:
                    logging.warning(f"met unexpected description case, description as {description}, url {detail_url}")
        job_desc["job_feature"] = job_feature
        job_status_elements = soup_wholepage.find_all("li", {"class": "ca-item"})
        job_status = {}
        for job_status_element in job_status_elements:
            key = job_status_element.find("span", {"class": "title"})
            if not key:
                key = job_status_element.find("div", {"class": "title"})
            val = job_status_element.find("span", {"class": "value"})
            if not val:
                val = job_status_element.find("div", {"class": "value"})
            job_status[key.text.strip()[:-1]] = val.text.strip()
        job_desc["job_status"] = job_status
        logging.info(f"Scrape job {job_desc}")
        # TODO: design concurrent writeback interface in case of huge scraping amount required
        scraped_ls.append(json.dumps(job_desc))
    
    def _handle_job_list_page(self, pagenum, scraped_ls, init_lock, page_empty_marker):
        driver = None
        disp = None
        try:
            with init_lock:
                if self.use_vdisplay:
                    disp = Display(visible=0, size=(1920, 1080))
                    disp.start()
                option = Options()
                if "Linux" in platform.system():
                    option.add_argument("--disable-dev-shm-usage")
                driver = undetected_chromedriver.Chrome(
                    headless=False, 
                    driver_executable_path=self.webdriver_dir,
                    browser_executable_path=self.browser_dir,
                    use_subprocess=False, 
                    options=option
                )
            target_url = self.init_url + f"&page={pagenum}"
            driver.get(target_url)
            job_cards_elem = []
            job_href_elem = []
            for i in range(self.inner_retry_times):
                try:
                    WebDriverWait(driver, self.pageload_timeout * (2 ** i)).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="card-list-container"]|//*[@class="up-job-list"]')))
                    self._random_sleep()
                    job_cards_elem = driver.find_elements(By.XPATH, '//div[@class="d-flex job-tile-header"]')
                    job_href_elem = driver.find_elements(By.XPATH, '//a[@class="up-n-link"]')
                    if len(job_cards_elem) > 0 or len(job_href_elem) > 0:
                        break
                except TimeoutException:
                    if "There are no results that match your search." in driver.page_source \
                        and "Please try adjusting your search keywords or filters." in driver.page_source:
                        page_empty_marker.value = 1
                        raise PageEmptyException
                    else:
                        driver.refresh()
                except:
                    raise
            else:
                raise RetryLimitExceedException

            job_detail_urls = []
            if len(job_href_elem) > 0:
                for elem in job_href_elem:
                    job_detail_urls.append(elem.get_attribute('href'))
            else:
                for job in job_cards_elem:
                    driver.execute_script("arguments[0].click();", job)
                    self._random_sleep()
                    detail_elem = WebDriverWait(driver, self.pageload_timeout).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="up-n-link air3-btn air3-btn-link d-none d-md-flex"]')))
                    job_detail_urls.append(detail_elem[0].get_attribute('href'))
                    close_btn = driver.find_element(By.XPATH, '//button[@class="air3-slider-prev-btn air3-slider-close-desktop"]')
                    driver.execute_script("arguments[0].click();", close_btn)
                    self._random_sleep()
            logging.info(f"_handle_job_list_page got job_detail_urls as {job_detail_urls}")
            for url in job_detail_urls:
                self._handle_job_detail_page(driver, url, scraped_ls)
                if len(scraped_ls) > self.total_job_scrape:
                    break
        except:
            logging.error(f"_handle_job_list_page met exception {traceback.format_exc()}")
            raise
        finally:
            if hasattr(driver, "quit"):
                driver.quit()
            if hasattr(disp, "stop"):
                disp.stop()

    def _init_concurrency(self):
        if len(self.page_empty_markers) > 0:
            self.page_empty_markers.clear()
        for i in range(self.concurrency_factor):
            self.page_empty_markers.append(Value(c_int, 0))
            p = Process(target=self._handle_job_list_page, args=(i + self.assigned_pagenum + 1, self.scraped_job_ls, self.init_lock, self.page_empty_markers[i]))
            p.start()
            self.ps.append(p)
        self.assigned_pagenum += self.concurrency_factor
    
    def do(self):
        self._init_concurrency()
        scrape_start_time = time.time()
        while True:
            alldone = True
            for p in self.ps:
                if p.is_alive():
                    alldone = False
            scraped_n = len(self.scraped_job_ls)
            if scraped_n >= self.total_job_scrape:
                break
            if alldone:
                all_pages_empty = True
                for val in self.page_empty_markers:
                    if val.value == 0:
                        all_pages_empty = False
                if all_pages_empty:
                    logging.warning(f"Given total job to scrape {self.total_job_scrape} is fewer than jobs available, scraped count: {len(self.scraped_job_ls)}")
                    break
                if scraped_n < self.total_job_scrape:
                    self._init_concurrency()
            logging.info(f"upwork scraper scraping, current scraped num {scraped_n}")
            time.sleep(1)
        res_l = []
        for e in self.scraped_job_ls:
            if len(res_l) < self.total_job_scrape:
                res_l.append(json.loads(e))
        res = {
            "scrape_start_ts": scrape_start_time,
            "jobs": res_l
        }
        # TODO: design dynamic final result writeback interface
        with open(self.output_dir, "w") as f:
            json.dump(res, f)
        logging.info(f"waiting for subprocess gracefully quit...")
        time.sleep(5)
        for p in self.ps:
            try:
                p.join(timeout=1)
            except:
                pass
    
    def do_sync(self):
        scrape_start_time = time.time()
        while len(self.scraped_job_ls) < self.total_job_scrape:
            self._handle_job_list_page(self.assigned_pagenum + 1, self.scraped_job_ls, self.init_lock)
            scraped_n = len(self.scraped_job_ls)
            logging.info(f"upwork scraper scraping, current scraped num {scraped_n}")
            self.assigned_pagenum += 1
            time.sleep(1)
        res_l = []
        for e in self.scraped_job_ls:
            res_l.append(json.loads(e))
        res = {
            "scrape_start_time": scrape_start_time,
            "jobs": res_l
        }
        with open(self.output_dir, "w") as f:
            json.dump(res, f)
