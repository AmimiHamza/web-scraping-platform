import requests
from bs4 import BeautifulSoup
import re

def scrapeproduct(url):
    sanitized_file_name = re.sub(r'[^a-zA-Z0-9.-]', '_', url)
    file_path = 'products/' + sanitized_file_name + '.txt'

    with open(file_path, 'w') as f:
        print('hi')
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        div = soup.find('div', class_='row card _no-g -fg1 -pas')
        name = div.find('h1', class_='-fs20 -pts -pbxs').text.strip()
        print(name)
        price = div.find('div', class_='df -i-ctr -fw-w').span.text.strip()
        disponibility = 'Disponible'
        class_pattern = r'-df -i-ctr -fs12 -pbs -\w{3}$'  # Pattern to match class attribute ending with 3 characters
        for p in div.find_all('p'):
            class_attr = p.get('class')
            if class_attr and re.match(class_pattern, ' '.join(class_attr)):
                disponibility = p.text.strip()
                break
        rating = div.find(class_='stars _m _al').text.strip()
        sizes = [label.text.strip() for label in div.find_all('label', class_='vl')]

        f.write('Name: ' + name + '\n')
        f.write('Price: ' + price)
        f.write('\nRating: ' + rating)
        f.write('\nAvailability:  ' + disponibility)
        f.write('\nSizes: ')
        for size in sizes:
            f.write(size + '/')
        f.write('\n')

    print('file saved')