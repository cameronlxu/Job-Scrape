import bs4, requests
from bs4 import BeautifulSoup

# Customizable Inputs
job = 'Software Engineer Intern'
location = '94555'

# Setup
job = job.replace(' ','+')
url = requests.get('https://www.indeed.com/jobs?q={}&l={}'.format(job, location))
soup = bs4.BeautifulSoup(url.text, features="html.parser")

# Parse
results = soup.find(id='resultsCol')
job_elems = results.find_all('div', class_="jobsearch-SerpJobCard unifiedRow row result")

for job_elem in job_elems:
    title = job_elem.find('h2', class_='title')
    company = job_elem.find('span', class_='company')
    location = job_elem.find('span', class_='location accessible-contrast-color-location')   
    if None in (title, company, location):
        continue
    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
    print("------")