import bs4, requests, os, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Customizable Inputs
job = 'Software Engineer Intern'
location = '94555'

# Setup
job = job.replace(' ','+')
url = 'https://www.indeed.com/jobs?q={}&l={}'.format(job, location)
page = requests.get(url)
soup = bs4.BeautifulSoup(page.text, features="html.parser")

# Selenium Setup, uses chrome version 87
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
chrome_options = Options()
chrome_options.add_argument("--headless")   # Browser stays closed
browser = webdriver.Chrome(executable_path = DRIVER_BIN, chrome_options=chrome_options)

# Parse
results = soup.find(id='resultsCol')
job_elems = results.find_all('div', class_="jobsearch-SerpJobCard unifiedRow row result")
links = []

for job_elem in job_elems:
    title = job_elem.find('h2', class_='title')
    company = job_elem.find('span', class_='company')
    location = job_elem.find('span', class_='location accessible-contrast-color-location')   
    if None in (title, company, location):
        continue

    # Retrieve the links to each job
    address = job_elem.find('a')['href']
    combined_link = "https://www.indeed.com" + address
    links.append(str(combined_link))

    # Go to detailed job pages and scrape the job apply link
    browser.get(combined_link)
    time.sleep(1)   # give browser 1 second to load the page
    detail_soup = bs4.BeautifulSoup(browser.page_source, features='html.parser')
    job_path = detail_soup.find(id='viewJobButtonLinkContainer')

    # Some jobs can be applied directly on indeed
    apply_on_indeed = False
    if job_path is None:
        apply_on_indeed = True
    else:
        company_path = job_path.find('a')['href']

    # Print data gathered
    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
    if apply_on_indeed is True:
        print("--- APPLY ON INDEED ---")
        print(combined_link)
    else:
        print("--- COMPANY LINK --- ")
        print(company_path)
    print("------")