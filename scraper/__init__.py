import copy
import json
import logging
import random
import sys
import time
import traceback
import undetected_chromedriver

from bs4 import BeautifulSoup
from multiprocess import Process, Manager, Lock
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from utils import RetryLimitExceedException


class UpworkJobScrapeManager:
    def __init__(self, initial_url, webdriver_dir, total_job_scrape, jobs_one_page, min_sleep_sec, max_sleep_sec, pageload_timeout, concurrency_factor, output_dir):
        self.min_sleep_sec = min_sleep_sec
        self.max_sleep_sec = max_sleep_sec
        self.pageload_timeout = pageload_timeout

        self.init_url = initial_url
        self.jobs_one_page = jobs_one_page
        self.total_job_scrape = total_job_scrape
        self.output_dir = output_dir

        self.webdriver_dir = webdriver_dir

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
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        skills = soup.find_all("span", {"class": "air3-badge air3-badge-highlight badge disabled"})
        for skill in skills:
            expertises.add(skill.text.strip())
        if '' in expertises:
            logging.warning(f"found empty str in expertise")
        job_desc["expertises"] = list(expertises)
        job_desc["url"] = detail_url
        logging.info(f"Scrape job {job_desc}")
        scraped_ls.append(json.dumps(job_desc))
    
    def _handle_job_list_page(self, pagenum, scraped_ls, init_lock):
        try:
            init_lock.acquire()
            driver_service = Service(executable_path=self.webdriver_dir, log_output=sys.stdout)
            driver = undetected_chromedriver.Chrome(headless=False, use_subprocess=False, service=driver_service)
            init_lock.release()
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
            driver.quit()

    def _init_concurrency(self):
        for i in range(self.concurrency_factor):
            p = Process(target=self._handle_job_list_page, args=(i + self.assigned_pagenum + 1, self.scraped_job_ls, self.init_lock,))
            p.start()
            self.ps.append(p)
            self.assigned_pagenum += 1
    
    def do(self):
        self._init_concurrency()
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
        with open(self.output_dir, "w") as f:
            json.dump(res_l, f)
        logging.info(f"waiting for subprocess gracefully quit...")
        time.sleep(5)
    
    def do_sync(self):
        while len(self.scraped_job_ls) < self.total_job_scrape:
            self._handle_job_list_page(self.assigned_pagenum + 1, self.scraped_job_ls, self.init_lock)
            scraped_n = len(self.scraped_job_ls)
            logging.info(f"upwork scraper scraping, current scraped num {scraped_n}")
            self.assigned_pagenum += 1
            time.sleep(1)
        res_l = []
        for e in self.scraped_job_ls:
            res_l.append(json.loads(e))
        with open(self.output_dir, "w") as f:
            json.dump(res_l, f)
