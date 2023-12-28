from settings import *

TOTAL_JOB_SCRAPE = int(os.getenv("TOTAL_JOB_SCRAPE", 500))
MIN_SLEEP_SEC = float(os.getenv("MIN_SLEEP_SEC", 1e-5))
MAX_SLEEP_SEC = int(os.getenv("MAX_SLEEP_SEC", 10))
WEBDRIVER_DIR = os.path.join(ASSETS_ROOT, "bin", "chromedriver")
BROWSER_DIR = os.path.join(ASSETS_ROOT, "chrome-linux64", "chrome")
CONCURRENCY_FACTOR = int(os.getenv("CONCURRENCY_FACTOR", 5))
UPOWORK_JOBS_ONE_PAGE = int(os.getenv("UPOWORK_JOBS_ONE_PAGE", 50))
PAGELOAD_TIMEOUT = int(os.getenv("PAGELOAD_TIMEOUT", 5))
USE_VDISPLAY = int(os.getenv("USE_VDISPLAY", 1))
