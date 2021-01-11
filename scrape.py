import bs4, requests
from bs4 import BeautifulSoup

# Customizable Inputs
job = 'Software Engineer Intern'
location = '95014'

# Setup
job = job.replace(' ','+')
url = requests.get('https://www.indeed.com/jobs?q={}&l={}'.format(job, location))
soup = bs4.BeautifulSoup(url.text, features="html.parser")