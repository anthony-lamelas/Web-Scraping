import csv
import requests
from bs4 import BeautifulSoup

# Open file for writing CSV
with open('linkedin-jobs.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    
    # Write header row to the CSV file
    writer.writerow(['Title', 'Company', 'Location', 'Apply'])

    def linkedin_scraper(webpage, page_number):
        # Construct the URL for the current page
        next_page = webpage + '&pageNum=' + str(page_number)
        print(f'Scraping page: {next_page}')
        
        # Send a GET request to fetch the webpage content
        response = requests.get(next_page)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all job cards on the page
        jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        
        # Loop through each job card and extract relevant details
        for job in jobs:
            try:
                
                job_title = job.find('h3', class_='base-search-card__title').text.strip()
                job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
                job_location = job.find('span', class_='job-search-card__location').text.strip()
                job_link = job.find('a', class_='base-card__full-link')['href']

                
                writer.writerow([job_title, job_company, job_location, job_link])
                print(f'Job saved: {job_title}')
            except AttributeError:
                print('Failed to parse job details.')

        print('Data updated')

        # Check if the "Next" button exists to proceed to the next page
        next_button = soup.find('button', {'aria-label': 'Next'})
        if next_button and 'disabled' not in next_button.attrs:
            page_number += 1
            linkedin_scraper(webpage, page_number)
        else:
            print('No more pages to scrape.')
            return

    url = 'https://www.linkedin.com/jobs/search?keywords=&location=United%20States&geoId=103644278&f_JT=F&f_E=4%2C5&f_PP=105858804%2C102394087%2C102844048&f_TPR=&f_WT=2'
    
    linkedin_scraper(url, 0)
