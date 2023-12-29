# upwork Scraper

An upwork website scraper powered by selenium and bs4 library written in Python.

## Depedency

### Python related

```bash
python3 -m pip install -r requirements.txt
```

### Selenium releated

Place chromedriver and chrome browser with suitable version into assets path, then change webdriver and chrome executable path specification under settings subsequently.

## Usage

### Windows

```bash
# assume below commands are executed under Windows powershell
$env:ENV = 'dev'
python3 main.py --main_category 'Web, Mobile & Software Dev' --output out.json
```

### Linux

```bash
export ENV=prod
python3 main.py --main_category 'Web, Mobile & Software Dev' --output out.json
```

## Data Samples

```json
{
    "scrape_start_ts": 1703867808.0236104,
    "jobs": [
        {
            "title": "E-commerce Consultant",
            "url": "https://www.upwork.com/jobs/commerce-Consultant_~01ed33641000a395d1/",
            "scraped_ts": 1703867829.0134757,
            "description": "Hands of Hope for Physical Therapy and Wellness is seeking a highly skilled and experienced E-commerce Consultant. As an E-commerce Consultant, you will play a crucial role in developing and implementing effective strategies to optimize our online presence and enhance our e-commerce operations. Your expertise will be instrumental in driving business growth and achieving our e-commerce objectives.",
            "area_restriction": "US Only",
            "skill_and_expertise": [
                "WooCommerce",
                "Ecommerce Website Development",
                "Shopify"
            ],
            "job_feature": {
                "Contract To Fulltime": true,
                "Duration": "3-6 months",
                "Estimated Job Duration": "Less than 30 hrs/week",
                "Estimated Job Pay": "$150.00 ~ $200.00",
                "Experience Level": "Expert",
                "Fixed-price": null,
                "Project Type": "Complex project",
                "Remote Type": "Remote Job"
            },
            "job_status": {
                "Proposals": "Less than 5",
                "Last viewed by client": "2 minutes ago",
                "Interviewing": "0",
                "Invites sent": "10",
                "Unanswered invites": "10"
            }
        },
        {
            "title": "Website Design and Improvement",
            "url": "https://www.upwork.com/jobs/Website-Design-and-Improvement_~013304a0e93f4708af/",
            "scraped_ts": 1703867830.7685492,
            "description": "We are looking for a skilled web designer to enhance and improve the appearance of our construction company website. The main goal is to create a user-friendly and visually appealing website that accurately represents our brand and services. The ideal candidate should have experience in the following areas:\n\n- Web design\n- Responsive design\n- Graphic design",
            "area_restriction": "US Only",
            "skill_and_expertise": [
                "Graphic Design",
                "Web Design",
                "Web Development",
                "Mockup",
                "WordPress"
            ],
            "job_feature": {
                "Contract To Fulltime": null,
                "Duration": "6+ months",
                "Estimated Job Duration": "Less than 30 hrs/week",
                "Estimated Job Pay": "$15.00 ~ $30.00",
                "Experience Level": "Intermediate",
                "Fixed-price": null,
                "Project Type": "Ongoing project",
                "Remote Type": "Remote Job"
            },
            "job_status": {
                "Proposals": "20 to 50",
                "Last viewed by client": "2 days ago",
                "Interviewing": "3",
                "Invites sent": "3",
                "Unanswered invites": "0"
            }
        },
        {
            "title": "RESTful API Integration With Woo Commerce",
            "url": "https://www.upwork.com/jobs/RESTful-API-Integration-With-Woo-Commerce_~016fbb07f06111f091/",
            "scraped_ts": 1703867833.5303104,
            "description": "Looking for someone to connect our vendor account with our woo commerce multi store wordpress site. Our vendor uses the RESTful API. See attached for more details on vendors API.\n\nThe end goal is to:\n\n- Automaticly update pricing\n- Automaticly update stock status\n\nWe would like to update all sites on our wordpress multisite network.\n\nIf we can get the vendors data to google sheets automatically that would be fine as an alternative solution.\n\nThanks in advance!",
            "area_restriction": "US Only",
            "skill_and_expertise": [
                "API Integration",
                "API",
                "WooCommerce"
            ],
            "job_feature": {
                "Contract To Fulltime": null,
                "Duration": "< 1 month",
                "Estimated Job Duration": "Less than 30 hrs/week",
                "Estimated Job Pay": "$50.00 ~ $75.00",
                "Experience Level": "Intermediate",
                "Fixed-price": null,
                "Project Type": "One-time project",
                "Remote Type": "Remote Job"
            },
            "job_status": {
                "Proposals": "20 to 50",
                "Last viewed by client": "3 days ago",
                "Hires": "1",
                "Interviewing": "0",
                "Invites sent": "0",
                "Unanswered invites": "0"
            }
        },
        {
            "title": "Wordpress designer needed for shamanic feminine design. Clean and elegant design",
            "url": "https://www.upwork.com/jobs/Wordpress-designer-needed-for-shamanic-feminine-design-Clean-and-elegant-design_~01c28b7f853f07f455/",
            "scraped_ts": 1703867657.6177545,
            "description": "I'm looking for a designer who can help bring my vision and website to life.\n\nI've already got a sense of working design.  Copy written for the pages.  Gorgeous photos to integrate and am seeking someone who can help glue it all together.\n\nMy ideal candidate is a woman who can translate the mystery, magic and essence of my vision into life.\n\nI like clean design. I've got so much brand wise completed so it would literally be putting things together in a cohesive way that looks visually stunning and high end.  \n\nScope is: full website with links to social and email list opt in and a landing page for a program as part of the website.  \n\nThis isn't a complicated site.  It is for a personal brand.  \n\nI need someone organized, communicative and creative/ artistic who knows wordpress and would enjoy working with a spiritual business and feel inspired by getting to use her creativity.\n\nThemes for the site are\nShamanic\nCrone\nArchetype\nMagic\nDark Feminine\nMysterious\nPowerful\nSovereign\n\nFunctionality: We need a password protected part of the site to hold our recordings of content where it's user friendly.\n\nWe plan to add an email capture as well and have pages that are for masterclasses we might offer to entice people to learn more - with that we would need lead captures.\n\nThe rest of the site would be driving people to book a call with me.\n\nMenu might be:\nHome Page\nBook a Call\nFree Resources\nMasterclasses\n(hidden page) Course Files",
            "area_restriction": "Global",
            "skill_and_expertise": [
                "Photo Editing",
                "Squarespace",
                "Visual Communication",
                "Adobe Photoshop",
                "Photo Manipulation",
                "Graphic Design"
            ],
            "job_feature": {
                "Contract To Fulltime": null,
                "Duration": null,
                "Estimated Job Duration": null,
                "Estimated Job Pay": null,
                "Experience Level": "Intermediate",
                "Fixed-price": "$500.00",
                "Project Type": "Ongoing project",
                "Remote Type": "Remote Job"
            },
            "job_status": {
                "Proposals": "Less than 5",
                "Interviewing": "0",
                "Invites sent": "0",
                "Unanswered invites": "0"
            }
        },
        {
            "title": "Website Audit",
            "url": "https://www.upwork.com/jobs/Website-Audit_~017e761a220ba01ff7/",
            "scraped_ts": 1703867661.8435965,
            "description": "SEO and speed analysis\nUsability and mobile compatibility check\nContent strategy evaluation\nVisual design review\nIn addition to the analysis, we expect:\n\nA detailed report highlighting issues and improvements\nRecommendations for visual and design enhancements\nCreation of a new design wireframe based on the suggestions",
            "area_restriction": "Global",
            "skill_and_expertise": [
                "UX & UI Design",
                "Landing Page",
                "Shopify",
                "SEO Audit",
                "Web Design",
                "SEO Competitor Analysis",
                "Technical SEO",
                "On-Page SEO",
                "Search Engine Optimization",
                "SEO Performance"
            ],
            "job_feature": {
                "Contract To Fulltime": null,
                "Duration": null,
                "Estimated Job Duration": null,
                "Estimated Job Pay": null,
                "Experience Level": "Expert",
                "Fixed-price": "$150.00",
                "Project Type": "One-time project",
                "Remote Type": "Remote Job"
            },
            "job_status": {
                "Proposals": "10 to 15",
                "Interviewing": "0",
                "Invites sent": "0",
                "Unanswered invites": "0"
            }
        }
    ]
}
```

## Platform Supporting Plan

- [x] Windows
- [x] Linux
