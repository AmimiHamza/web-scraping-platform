from bs4 import BeautifulSoup
import requests
import time
def scrapejobs(skill):
    page=1
    index=1
    job_listings=[1]
    while len(job_listings)!=0:
        print(len(job_listings))
        html_text=requests.get('https://www.receptix.uk/us/'+skill+'?page='+str(page)).text
        soup = BeautifulSoup(html_text, 'html.parser')
        job_listings = soup.find_all('div', class_='job-dsply-div')
        if len(job_listings)!=0:
            with open('jobs/'+skill+'.txt','a') as f:
                file.seek(0, 2)
                for job in job_listings:
                    title = job.find('p', class_='secondary-font-style').text.strip()
                    company = job.find('h4').text.strip()
                    location = job.find('p', class_='black-primary mb-0').text.strip()
                    f.write(str(index) +')Title: '+title+'\n')
                    f.write('Company name: '+company)
                    f.write ('\nLocation: '+location)
                    f.write('---\n')
                    index+=1
                    print("index:",index)
                page+=1
                print('page:',page)
    print('file saved')