import argparse
import logging
import os
import traceback

import scraper
import settings
import utils


def check_environment():
    try:
        if not os.path.exists(settings.WEBDRIVER_DIR):
            raise FileNotFoundError(f"Webdriver not found at path {settings.WEBDRIVER_DIR}")
    except:
        logging.error(f"Check scraper depedency got exception as {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    try:
        logging.getLogger().setLevel(logging.INFO)
        parser = argparse.ArgumentParser(description="Scrape upwork recent development works and analyze technology trends.")
        parser.add_argument('--main_category', type=str, default="Web, Mobile & Software Dev", help="Target main category of upwork jobs")
        parser.add_argument('--output', type=str, default=os.path.join(settings.PROJECT_ROOT, "output.json"), help="Output path")
        args = parser.parse_args()
        check_environment()
        initial_url = utils.concat_upwork_initial_url(args.main_category)
        doer = scraper.UpworkJobScrapeManager(initial_url, settings.WEBDRIVER_DIR, settings.BROWSER_DIR, settings.USE_VDISPLAY, settings.TOTAL_JOB_SCRAPE, settings.UPOWORK_JOBS_ONE_PAGE, settings.MIN_SLEEP_SEC, settings.MAX_SLEEP_SEC, settings.PAGELOAD_TIMEOUT, settings.CONCURRENCY_FACTOR, args.output)
        doer.do()
        if not os.path.exists(args.output) or os.path.getsize(args.output) == 0:
            raise FileNotFoundError(args)
        logging.info(f"upwork scraper got result size {os.path.getsize(args.output)}")
    except:
        logging.error(f"main.py got exception as {traceback.format_exc()}")
        raise
