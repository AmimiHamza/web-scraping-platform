import requests
from bs4 import BeautifulSoup
import pandas as pd
def scrapecrypto(p):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    base_url = "https://www.coingecko.com/"

    tables=[]

    for i in range(1,p+1):
        print('Processing page {0}'.format(i))
        params={
            'page':i
            }
        response = requests.get(base_url, headers=headers,params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        tables.append(pd.read_html(str(soup))[0])

    full_table=pd.concat(tables)
    full_table=full_table.loc[:, full_table.columns[1:-1]]
    output_file = "crypto/cryptosn.xlsx"
    full_table.to_excel(output_file,index=False)