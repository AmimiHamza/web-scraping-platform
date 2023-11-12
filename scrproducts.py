from bs4 import BeautifulSoup
import requests

def scrapeproducts(product):
    page = 1
    index = 1
    product_listings = [1]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    
    with open('products/' + product + '.txt', 'w', encoding='utf-8') as f:
        while len(product_listings) != 0 and index < 201:
            url = f'https://www.jumia.ma/catalog/?q={product}&page={page}#catalog-listing'
            
            try:
                html_text = requests.get(url, headers=headers).text
                soup = BeautifulSoup(html_text, 'html.parser')
                product_listings = soup.find_all('article', class_='prd _fb col c-prd')
                
                if len(product_listings) != 0:
                    for prod in product_listings:
                        name = prod.find('h3', class_='name').text.strip()
                        price = prod.find('div', class_='prc').text.strip()
                        f.write(f"{index}) Name: {name}\n")
                        f.write(f"Price: {price}\n")
                        index += 1
                        print("Product scrapped:", index)
                    
                    page += 1
            except requests.exceptions.RequestException as e:
                print("An error occurred:", str(e))
        
        print('File saved')
