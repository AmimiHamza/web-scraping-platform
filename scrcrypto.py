# from bs4 import BeautifulSoup
# import requests
# import time
# from datetime import datetime
# def scrapecrypto():
#     current_datetime = datetime.now()
#     filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S.txt")
#     with open(filename, 'w') as file:
#         html_text=requests.get('https://www.coingecko.com/').text
#         soup = BeautifulSoup(html_text, 'html.parser')
#         print(soup)
        # table=soup.find('table',class_='sort table mb-0 text-sm text-lg-normal table-scrollable')
        # tbody=table.find('tbody',attrs={"data-target": "currencies.contentBox"})
        # rows = tbody.find_all('tr')
        # for tr in rows:
        #     price_element = tr.find('td', class_='td-price')
        #     price = price_element.find('span').text.strip()
        #     print("Price:", price)

        #     if len(job_listings)!=0:   
        #             for job in job_listings:
        #                 title = job.find('p', class_='secondary-font-style').text.strip()
        #                 company = job.find('h4').text.strip()
        #                 location = job.find('p', class_='black-primary mb-0').text.strip()
        #                 f.write(str(index) +')Title: '+title+'\n')
        #                 f.write('Company name: '+company)
        #                 f.write ('\nLocation: '+location)
        #                 f.write('\n')
        #                 index+=1
        #                 print("job scrapped:",index)
        #             page+=1
        # print('file saved')
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd

def scrapecrypto():
    current_datetime = datetime.now()
    filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S.txt")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (without opening a browser window)
    
    with webdriver.Chrome(options=options) as driver:
        driver.get("https://www.coingecko.com/")
        
        # Wait for the page to load (you can adjust the sleep time if needed)
        time.sleep(5)
        
        with open('crypto/'+filename, 'w') as file:
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            file.write(str(soup))     
            print(pd.read_html(str(soup)))
            # Continue with your scraping code...
            # Rest of your scraping code...
            # file.write(...)
    
    print('File saved:', filename)



