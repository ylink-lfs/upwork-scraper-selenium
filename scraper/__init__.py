import json
import logging
import random
import platform
import time
import traceback
import undetected_chromedriver

from bs4 import BeautifulSoup
from multiprocess import Process, Manager, Lock
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import RetryLimitExceedException


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
        self.assigned_pagenum = 0
        self.inner_retry_times = 3
    
    def _random_sleep(self):
        sleep_duration = random.uniform(self.min_sleep_sec, self.max_sleep_sec)
        time.sleep(sleep_duration)
    
    def _handle_job_detail_page(self, driver, detail_url, scraped_ls):
        job_desc = {}
        driver.get(detail_url)
        expertises = set()
        WebDriverWait(driver, self.pageload_timeout).until(EC.presence_of_all_elements_located((By.XPATH, "//section[@class='air3-card-section py-4x']")))
        self._random_sleep()

        title_element = driver.find_element(By.XPATH, "//h4[@class='m-0']")
        job_desc["title"] = title_element.text.strip()

        detail_element = driver.find_element(By.XPATH, "//p[@class='text-body-sm']")
        job_desc["description"] = detail_element.text.strip()

        area_restriction_element = driver.find_element(By.XPATH, "//span[@class='d-none d-md-inline']")
        job_desc["area_restriction"] = area_restriction_element.text.strip()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        skills = soup.find_all("span", {"class": "air3-badge air3-badge-highlight badge disabled"})
        for skill in skills:
            expertises.add(skill.text.strip())
        if '' in expertises:
            logging.warning(f"found empty str in expertise like {expertises}, original skills like {skills}, job_url {detail_url}")
        job_desc["skill_and_expertise"] = list(expertises)
        job_feature_elements = driver.find_elements(By.XPATH, "//li[@data-v-ad039828='']")
        job_desc.update(
            dict.fromkeys(
                [
                    "Project Type", 
                    "Experience Level", 
                    "Duration",
                    "Contract To Fulltime",
                    "Estimated Job Duration",
                    "Estimated Job Pay",
                    "Remote Type",
                ], None)
        )
        for i in range(len(job_feature_elements)):
            job_feature_element_src = job_feature_elements[i].get_attribute("outerHTML")
            sp = BeautifulSoup(job_feature_element_src, 'html.parser')
            desc_text = sp.find("strong", {"data-v-ad039828": ""})
            description = sp.find("div", {"class": "description"})
            if description:
                description = description.text.strip()
            else:
                description = ""
            if description in ["Project Type", "Experience Level", "Duration", "Fixed-price"]:
                job_desc[description] = desc_text.text.strip()
            elif "This job has the potential to turn into a full time role" in description:
                job_desc["Contract To Fulltime"] = True
            else:
                icon_name = sp.find("div", {"class": "air3-icon md"})["data-cy"]
                if icon_name == "clock-hourly":
                    job_desc["Estimated Job Duration"] = desc_text.text.strip()
                elif icon_name == "clock-timelog":
                    pay_elems = sp.find_all("p", {"class": "m-0"})
                    pay_lower = pay_elems[0].find("strong", {"data-v-ad039828": ""}).text.strip()
                    pay_upper = pay_elems[-1].find("strong", {"data-v-ad039828": ""}).text.strip()
                    job_desc["Estimated Job Pay"] = f"{pay_lower} ~ {pay_upper}"
                elif icon_name == "local":
                    job_desc["Remote Type"] = desc_text.text.strip()
                else:
                    logging.warning(f"met unexpected description case, description as {description}, url {detail_url}")
        job_status_elements = soup.find_all("li", {"class": "ca-item"})
        for job_status_element in job_status_elements:
            key = job_status_element.find("span", {"class": "title"})
            if not key:
                key = job_status_element.find("div", {"class": "title"})
            val = job_status_element.find("span", {"class": "value"})
            if not val:
                val = job_status_element.find("div", {"class": "value"})
            job_desc[key.text.strip()[:-1]] = val.text.strip()
        job_desc["url"] = detail_url
        logging.info(f"Scrape job {job_desc}")
        # TODO: design concurrent writeback interface in case of huge scraping amount required
        scraped_ls.append(json.dumps(job_desc))
    
    def _handle_job_list_page(self, pagenum, scraped_ls, init_lock):
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
                WebDriverWait(driver, self.pageload_timeout * (2 ** i)).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="card-list-container"]|//*[@class="up-job-list"]')))
                self._random_sleep()
                job_cards_elem = driver.find_elements(By.XPATH, '//div[@class="d-flex job-tile-header"]')
                job_href_elem = driver.find_elements(By.XPATH, '//a[@class="up-n-link"]')
                if len(job_cards_elem) > 0 or len(job_href_elem) > 0:
                    break
                driver.refresh()
            else:
                raise RetryLimitExceedException
            logging.info(f"job_cards_elem as {job_cards_elem}, length {len(job_cards_elem)}, job_href_elem as {job_href_elem}, length {len(job_href_elem)}")
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
        for i in range(self.concurrency_factor):
            p = Process(target=self._handle_job_list_page, args=(i + self.assigned_pagenum + 1, self.scraped_job_ls, self.init_lock,))
            p.start()
            self.ps.append(p)
            self.assigned_pagenum += 1
    
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
            if alldone and scraped_n < self.total_job_scrape:
                self._init_concurrency()
            logging.info(f"upwork scraper scraping, current scraped num {scraped_n}")
            time.sleep(1)
        res_l = []
        for e in self.scraped_job_ls:
            res_l.append(json.loads(e))
        res = {
            "scrape_start_time": scrape_start_time,
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
