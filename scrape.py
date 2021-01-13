import bs4, requests, os, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Customizable Inputs
job = 'Software Engineer Intern'
location = '94555'

def main():
    # Setup
    url = 'https://www.indeed.com/jobs?q={}&l={}'.format(job.replace(' ','+'), location)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, features="html.parser")

    # Selenium Setup, uses chrome version 87
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    chrome_options = Options()
    chrome_options.add_argument("--headless")   # Browser stays closed
    browser = webdriver.Chrome(executable_path = DRIVER_BIN, options=chrome_options)

    # Start parsing the home page
    parseHome(browser, soup)

def parseHome(browser, soup):
    # Zone in on results column
    results = soup.find(id='resultsCol')
    job_elems = results.find_all('div', class_="jobsearch-SerpJobCard unifiedRow row result")
    
    # Save all data to an list with format: [company, title, location, link]
    data = []

    for job_elem in job_elems:
        title = job_elem.find('h2', class_='title')
        company = job_elem.find('span', class_='company')
        location = job_elem.find('span', class_='location accessible-contrast-color-location')   
        if None in (title, company, location):
            continue

        # Retrieve the links to each job
        address = job_elem.find('a')['href']
        combined_link = "https://www.indeed.com" + address

        # Go to detailed job pages and scrape the job apply link
        browser.get(combined_link)
        time.sleep(1)   # give browser 1 second to load the page
        detail_soup = bs4.BeautifulSoup(browser.page_source, features='html.parser')
        job_path = detail_soup.find(id='viewJobButtonLinkContainer')

        # Format each index's data
        to_add = [company.text.strip(), title.text.strip(), location.text.strip()]

        # Some jobs can be applied directly on indeed, determine this then save link
        if job_path is None:
            to_add.append(str(combined_link))
        else:
            company_path = job_path.find('a')['href']
            to_add.append(company_path)

        # Add to full data list
        data.append(to_add)
        print(to_add)


if __name__ == "__main__":
    main()