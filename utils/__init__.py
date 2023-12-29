import settings


UPWORK_MAIN_CATEGORY_TO_UID = {
    "All": "",
    "Accounting & Consulting": "531770282584862721",
    "Admin Support": "531770282580668416",
    "Customer Service": "531770282580668417",
    "Data Science & Analytics": "531770282580668420",
    "Design & Creative": "531770282580668421",
    "Engineering & Architecture": "531770282584862722",
    "IT & Networking": "531770282580668419",
    "Legal": "531770282584862723",
    "Sales & Marketing": "531770282580668422",
    "Translation": "531770282584862720",
    "Web, Mobile & Software Dev": "531770282580668418",
    "Writing": "531770282580668423",
}


class CategoryNotFoundError(Exception):
    pass


class RetryLimitExceedException(Exception):
    pass


def concat_upwork_initial_url(main_category):
    if main_category.startswith("'"):
        main_category = main_category[1:-1]
    if not main_category in UPWORK_MAIN_CATEGORY_TO_UID:
        raise CategoryNotFoundError(f"Main category not found, passed category: {main_category}")
    return f"https://www.upwork.com/nx/search/jobs?category2_uid={UPWORK_MAIN_CATEGORY_TO_UID[main_category]}&per_page={settings.UPOWORK_JOBS_ONE_PAGE}&sort=recency&subcategory2_uid="
