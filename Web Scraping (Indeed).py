import requests
from bs4 import BeautifulSoup
import csv

# Get user input
skill = input('Enter your Skill: ').strip()
place = input('Enter the location: ').strip()
no_of_pages = int(input('Enter the # of pages to scrape: '))

indeed_posts = []

for page in range(no_of_pages):
    url = f'https://www.indeed.com/jobs?q={skill}&l={place}&start={page * 10}'
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    outer_most_point = soup.find('div', attrs={'id': 'mosaic-provider-jobcards'})
    
    if not outer_most_point:
        print(f"No job cards found on page {page + 1}. Skipping...")
        continue
    
    job_list = outer_most_point.find('ul')
    
    if not job_list:
        print(f"No job list found on page {page + 1}. Skipping...")
        continue
    
    for job_card in job_list.find_all('li'):
        job_title_elem = job_card.find('h2', {'class': 'jobTitle jobTitle-color-purple jobTitle-newJob'})
        job_title = job_title_elem.find('a').text if job_title_elem else 'No title'

        company_elem = job_card.find('span', {'class': 'companyName'})
        company = company_elem.text if company_elem else 'No company'

        link_elem = job_card.find('a', {'class': 'jcs-JobTitle'})
        link = "https://www.indeed.co.in" + link_elem['href'] if link_elem else 'No link'

        salary_elem = job_card.find('div', {'class': 'attribute_snippet'})
        salary = salary_elem.text if salary_elem else 'No Salary'

        post_date_elem = job_card.find('span', attrs={'class': 'date'})
        post_date = post_date_elem.text if post_date_elem else 'No date'

        indeed_posts.append([company, job_title, link, salary, post_date])

# Writing the collected data to a CSV file
indeed_spec = ['Company', 'Job', 'Link', 'Salary', 'Job_Posted_Date']

with open('indeed-jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(indeed_spec)
    writer.writerows(indeed_posts)

print("Job data has been written to indeed-jobs.csv")
