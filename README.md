# upwork Scraper

An upwork website scraper powered by selenium and bs4 library written in Python.

## Depedency

### Python related

```bash
python3 -m pip install -r requirements.txt
```

### Selenium releated

Place chromedriver with suitable version into assets path, then change webdriver path specification under settings subsequently.

## Usage

### Windows

```bash
# assume below commands are executed under Windows powershell
$env:ENV = 'dev'
python3 main.py --main_category 'Web, Mobile & Software Dev' --sub_category 'All' --output out.json
```

### Linux

```bash
export ENV=prod
python3 main.py --main_category 'Web, Mobile & Software Dev' --sub_category 'All' --output out.json
```

## Data Samples

```json
{
    "scrape_start_time": 1703782341.7475863,
    "jobs": [
        {
            "title": "Website Developer - Wordpress Integration Specialist",
            "description": "Merge and integrate the functionalities of two separate websites into a single Wordpress-based platform.\n\u2022 Develop and design a cohesive, user-friendly website that highlights the combined features of both products.\n\u2022 Customize and optimize the Wordpress platform to meet specific project needs.\n\u2022 Implement responsive design and ensure the website\u2019s compatibility across various devices.\n\nRequirements:\n\n\u2022 Proficiency in Wordpress development and customization.\n\u2022 Extensive experience in website integration and migration.\n\u2022 Strong understanding of HTML, CSS, JavaScript, and other relevant web technologies.\n\u2022 Proven track record of successfully merging multiple websites into a unified platform.\n\u2022 Creative mindset with an eye for design and user experience.\n\u2022 Excellent problem-solving skills and attention to detail.\n\nPreferred Qualifications:\n\n\u2022 Familiarity with SEO best practices and website optimization techniques.\n\u2022 Experience with e-commerce integration within Wordpress.\n\u2022 Knowledge of UI/UX",
            "area_restriction": "Only freelancers located in the U.S. may apply.",
            "skill_and_expertise": [
                "UX & UI",
                "WooCommerce",
                "CSS",
                "WordPress",
                "HTML",
                "Website Customization",
                "Web Development",
                "Web Design",
                "WordPress Development",
                "Responsive Design"
            ],
            "Project Type": "One-time project",
            "Experience Level": "Intermediate",
            "Duration": null,
            "Contract To Fulltime": null,
            "Estimated Job Duration": null,
            "Estimated Job Pay": null,
            "Remote Type": "Remote Job",
            "Fixed-price": "$750.00",
            "Proposals": "10 to 15",
            "Last viewed by client": "7 minutes ago",
            "Interviewing": "0",
            "Invites sent": "0",
            "Unanswered invites": "0",
            "url": "https://www.upwork.com/jobs/Website-Developer-Wordpress-Integration-Specialist_~011167df9e81611550/"
        },
        {
            "title": "XLSM file to filter and calculate",
            "description": "The goal of this app will be to filter, add and display results. We need to have a user friendly interface. One of our current apps is an xlsm file.\nI paste a csv copy of the data in the same folder as the xlsm file. The user then opens the xlsm file and it auto displays the needed results without any user interaction.\nI would like something similar to this. I need it as user friendly as possible.\n\nIt will be used to add all the values in a category. It needs to round up to the nearest quarter or half depending on choice. Then add the values required to round to the master category for each item field.\n\nItem 1 Master Category = 9.2\nItem 1 Category 2 = 1.4\nSum               10.6\nValue needed to round to nearest quarter. In the above case will need .15.\n10.6 + .15 =  10.75\nOnce the needed amount is calculated \u201cin the above case .15\u201d it needs to be added to the master category.\nIn this case it would be 9.35\n\nI can explain in more detail later.",
            "area_restriction": "Only freelancers located in the U.S. may apply.",
            "skill_and_expertise": [
                "Microsoft Excel"
            ],
            "Project Type": "One-time project",
            "Experience Level": "Intermediate",
            "Duration": "< 1 month",
            "Contract To Fulltime": null,
            "Estimated Job Duration": "Less than 30 hrs/week",
            "Estimated Job Pay": "$40.00 ~ $120.00",
            "Remote Type": "Remote Job",
            "Proposals": "Less than 5",
            "Last viewed by client": "17 minutes ago",
            "Interviewing": "0",
            "Invites sent": "1",
            "Unanswered invites": "1",
            "url": "https://www.upwork.com/jobs/XLSM-file-filter-and-calculate_~01da9aa3d14ac709d2/"
        },
        {
            "title": "Developer for Photo and Video Collection",
            "description": "We are seeking a talented Developer to join our team and play a crucial role in enhancing our photo and video collection capabilities.\n\nResponsibilities:\n\nAs a Developer for Photo and Video Collection, you will be at the forefront of creating a seamless web-based system that integrates with our existing management platform. Your primary responsibilities will include:\n\nDevelop an automated system to prompt customers via email, encouraging them to share their photos and videos within 30 minutes of their experience.\n\nImplement a user-friendly interface for customers to easily upload content to the relevant dropbox folder.\n\nUtilize API data from our reservation system to automatically send personalized \"Thank You\" emails to customers, along with a request to share their content on social media.\n\nImplement a system that organizes uploaded content into location-specific dropbox folders, titled appropriately and organized by date.\n\nDevelop a tagging mechanism for online posts using designated hashtags based on city, tour name, and brand.\n\nCreate an automated process to combine videos or stitch together photos, generating a compelling 10-second clip highlighting the customer's experience.\n\nQualifications:\n-Proven experience in web development, API integration, and database management.\n-Strong proficiency in relevant programming languages and frameworks.\n-Excellent problem-solving skills and attention to detail.\n-Familiarity with multimedia processing and social media integration is a plus.\n\nIf you are passionate about creating innovative solutions that enhance customer engagement and exposure, we invite you to submit your proposaal,",
            "area_restriction": "Only freelancers located in the U.S. may apply.",
            "skill_and_expertise": [
                "Web Development",
                "CSS",
                "Python",
                "MySQL",
                "PHP",
                "HTML",
                "API Integration",
                "JavaScript"
            ],
            "Project Type": "Complex project",
            "Experience Level": "Expert",
            "Duration": "3-6 months",
            "Contract To Fulltime": null,
            "Estimated Job Duration": "Less than 30 hrs/week",
            "Estimated Job Pay": "$40.00 ~ $50.00",
            "Remote Type": "Remote Job",
            "Proposals": "20 to 50",
            "Last viewed by client": "14 hours ago",
            "Interviewing": "8",
            "Invites sent": "23",
            "Unanswered invites": "14",
            "url": "https://www.upwork.com/jobs/Developer-for-Photo-and-Video-Collection_~013f1cba04a2dfb9cf/"
        },
        {
            "title": "Plan and build a responsive WordPress site for a marketing company and a Shopify store",
            "description": "Marketing Site\nPlan session to build wireframe with different entry points\nDetermine best wordpress template\nProvide design that reflects marketing goals\nSet up website and launch\nWe will provide copy\n\nShopify site is to test campaigns based designs\nConversion drivenn design\nEmail capturing\nEasy one-click check out",
            "area_restriction": "Only freelancers located in the U.S. may apply.",
            "skill_and_expertise": [
                "Web Development",
                "Web Design",
                "Graphic Design",
                "WordPress"
            ],
            "Project Type": "Ongoing project",
            "Experience Level": "Expert",
            "Duration": "3-6 months",
            "Contract To Fulltime": null,
            "Estimated Job Duration": "Not Sure",
            "Estimated Job Pay": "$35.00 ~ $45.00",
            "Remote Type": "Remote Job",
            "Proposals": "20 to 50",
            "Interviewing": "0",
            "Invites sent": "0",
            "Unanswered invites": "0",
            "url": "https://www.upwork.com/jobs/Plan-and-build-responsive-WordPress-site-for-marketing-company-and-Shopify-store_~015742c36c1997c5e1/"
        },
        {
            "title": "E-commerce",
            "description": "Need a photographer in Dallas, Texas area for upcoming products.",
            "area_restriction": "Only freelancers located in the U.S. may apply.",
            "skill_and_expertise": [
                "photographer",
                "Graphic Design",
                "Ecommerce Website"
            ],
            "Project Type": "One-time project",
            "Experience Level": "Intermediate",
            "Duration": "< 1 month",
            "Contract To Fulltime": null,
            "Estimated Job Duration": "Less than 30 hrs/week",
            "Estimated Job Pay": "$35.00 ~ $60.00",
            "Remote Type": "Remote Job",
            "Proposals": "Less than 5",
            "Interviewing": "0",
            "Invites sent": "0",
            "Unanswered invites": "0",
            "url": "https://www.upwork.com/jobs/commerce_~01bd2d0a6ac61cd75b/"
        }
    ]
}
```

## Platform Supporting Plan

- [x] Windows
- [x] Linux
