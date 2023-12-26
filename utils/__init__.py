import settings

UPWORK_MAIN_CATEGORY_TO_UID = {
    "Web, Mobile & Software Dev": "531770282580668418",
}


UPWORK_SUB_CATEGORY_TO_UID = {
    "All": "",
}


class CategoryNotFoundError(Exception):
    pass

class RetryLimitExceedException(Exception):
    pass


def concat_upwork_initial_url(main_category, sub_category):
    if main_category.startswith("'"):
        main_category = main_category[1:-1]
        sub_category = sub_category[1:-1]
    if not main_category in UPWORK_MAIN_CATEGORY_TO_UID:
        raise CategoryNotFoundError(f"Main category not found, passed category: {main_category}")
    if not sub_category in UPWORK_SUB_CATEGORY_TO_UID:
        raise CategoryNotFoundError(f"Subcategory not found, passed category: {sub_category}")
    return f"https://www.upwork.com/nx/search/jobs?category2_uid={UPWORK_MAIN_CATEGORY_TO_UID[main_category]}&per_page={settings.UPOWORK_JOBS_ONE_PAGE}&sort=recency&subcategory2_uid={sub_category}"
