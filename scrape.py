import bs4, requests
from bs4 import BeautifulSoup

# Customizable Inputs
job = 'Software Engineer Intern'
location = '94555'

# Setup
job = job.replace(' ','+')
url = 'https://www.indeed.com/jobs?q={}&l={}'.format(job, location)
page = requests.get(url)
soup = bs4.BeautifulSoup(page.text, features="html.parser")

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
    links.append(combined_link)

    print(title.text.strip())
    print(company.text.strip())
    print(location.text.strip())
    print(combined_link)
    print("------")