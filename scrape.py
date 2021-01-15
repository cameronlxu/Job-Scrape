import bs4, requests, os, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gui import UI


def main() -> None:
    """
        Setup & retrieve the necessary tools to start the program.
    """
    # Use GUI for customizable inputs
    inputs = UI()
    job = inputs[0]
    location = inputs[1]
    num_pages = inputs[2]

    # Setup
    url = 'https://www.indeed.com/jobs?q={}&l={}'.format(job.replace(' ','+'), location)
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, features="html.parser")

    # Selenium Setup, uses chrome version 87
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")
    chrome_options = Options()
    chrome_options.add_argument("--headless")   # Browser stays closed
    browser = webdriver.Chrome(executable_path = DRIVER_BIN, options = chrome_options)
    browser.get(url)
    time.sleep(5)

    # Save all data to an list with format: [company, title, location, link]
    data = []

    # Start parsing the home page
    parseIndeed(browser, soup, num_pages-1, 1, data)


def parseIndeed(browser, soup, num_pages, counter, data) -> None:
    """
        Navigates through websites and parses the HTML. 

        Parameters
        ----------
        browser   : selenium obj
            Navigate through the website
        soup      : beautifulsoup obj
            Parse through browser page HTML code 
        num_pages : int
            Number of pages left to navigate
        counter   : int
            How many pages navigated so far
        data      : list
            List containing all data
    """
    # Close any pop-ups that may appear
    try:
        browser.find_element_by_class_name('popover-x-button-close').click()
        print('cleared pop-up')
    except:
        print('no pop-up')

    # Zone in on results column
    results = soup.find(id='resultsCol')
    job_elems = results.find_all('div', class_="jobsearch-SerpJobCard unifiedRow row result")

    for job_elem in job_elems:
        # Retrieve general job information
        title = job_elem.find('h2', class_='title').find_all('a')   # Only look at 'a'. Some jobs show as a "new" listing, filter out "new" text
        company = job_elem.find('span', class_='company')
        location = job_elem.find('span', class_='location accessible-contrast-color-location')   
        if None in (title, company, location):
            continue

        # Retrieve the links to each job
        address = job_elem.find('a')['href']
        combined_link = "https://www.indeed.com" + address

        # Go to detailed job pages and scrape the job apply link
        browser.get(combined_link)
        time.sleep(3)   # give browser 3 seconds to load the page
        detail_soup = bs4.BeautifulSoup(browser.page_source, features='html.parser')
        job_path = detail_soup.find(id='viewJobButtonLinkContainer')

        # Format each index's data
        to_add = [company.text.strip(), title[0].text.strip(), location.text.strip()]

        # Some jobs can be applied directly on indeed, determine this then save link
        if job_path is None:
            to_add.append(str(combined_link))
        else:
            company_path = job_path.find('a')['href']
            to_add.append(company_path)

        # Add to full data list
        data.append(to_add)

    # Write data to CSV File
    write(data)

    # Check if there are more pages to parse
    if num_pages != 0:
        next_page = check(soup, num_pages, counter)

        # If no next page, complete program. Else decrement/increment counters
        if next_page == None:
            finish()
        else:
            num_pages -= 1
            counter += 1

        # If there is a next page, navigate to the next one
        browser.get(next_page)
        time.sleep(2)
        next_soup = bs4.BeautifulSoup(browser.page_source, features='html.parser')
        parseIndeed(browser, next_soup, num_pages-1, counter+1, data)
    else:
        # Program completed
        finish()


def write(data) -> None:
    """
        Write data to CSV file. Create new file if it doesn't exist.
    """
    fields = ['Company', "Title", "Location", "Link"]
    filename = "job-scrape-output.csv"
    
    # Creates new CSV file in same directory, iterate through data list
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        for job in data:
            csvwriter.writerow(job)


def check(soup, num_pages, counter) -> str:
    """
        Returns the link to the next page if it exists, if not returns None.
    """
    page_links = soup.find('div', class_='pagination').find_all('a')
    next_page = None
    for paging in page_links:
        # Skip past the first page, the aria-label is string 'Previous'
        if paging['aria-label'] == 'Previous':
            continue

        # Check if we found the next page's link
        if int(paging['aria-label']) == counter + 1:
            next_page = "https://indeed.com" + str(paging['href'])
            break
    return next_page


def finish() -> None:
    """
        Print that the program has completed. 
    """
    print("Program finished, check CSV file")
    quit()
    

if __name__ == "__main__":
    main()