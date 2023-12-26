import importlib
import os


ENV = os.getenv("ENV", "")

# Path settings
SETTINGS_ROOT = os.path.dirname(os.path.realpath(__file__))
ENVS_ROOT = SETTINGS_ROOT
PROJECT_ROOT = os.path.dirname(SETTINGS_ROOT)
ASSETS_ROOT = os.path.join(PROJECT_ROOT, "assets")
WEBDRIVER_DIR = os.path.join(ASSETS_ROOT, "bin", "chromedriver.exe")

# Scrape behavoir settings
TOTAL_JOB_SCRAPE = 0
MIN_SLEEP_SEC = 0
MAX_SLEEP_SEC = 0
CONCURRENCY_FACTOR = 0
UPOWORK_JOBS_ONE_PAGE = 0
PAGELOAD_TIMEOUT = 0

ENVS = [os.path.splitext(filename)[0] for filename in os.listdir(ENVS_ROOT) if filename != "__init__.py"]
if ENV in ENVS:
    g = globals()
    current_settings = {}
    detailed_env = importlib.import_module(f'settings.{ENV}')
    current_settings.update({
        setting_k: setting_v
        for setting_k, setting_v in vars(detailed_env).items()
        if not setting_k.startswith('__')
    })
    g.update(current_settings)
else:
    raise NotImplementedError(f"Env {ENV} not implemented in settings")
