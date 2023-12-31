import platform

from settings import *

TOTAL_JOB_SCRAPE = 15
MIN_SLEEP_SEC = 0
MAX_SLEEP_SEC = 1
WEBDRIVER_DIR = os.path.join(ASSETS_ROOT, "bin", "chromedriver" + ".exe" if "Windows" in platform.system() else "")
BROWSER_DIR = None
CONCURRENCY_FACTOR = 2
UPOWORK_JOBS_ONE_PAGE = 15
PAGELOAD_TIMEOUT = 10
USE_VDISPLAY = 0
