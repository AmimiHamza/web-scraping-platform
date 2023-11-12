from bs4 import BeautifulSoup
import requests



def scrapeallmovies(genre):
    url = f'https://www.rottentomatoes.com/browse/movies_in_theaters/sort:{genre}?page=4'
    print('hi')
    print(genre)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    with open(f"movies/{genre}.txt", "w") as f:
        spans = soup.find_all("div", class_="js-tile-link")
        index=1
        for the_span in spans:
            title = the_span.find("span", class_="p--small", attrs={"data-qa": "discovery-media-list-item-title"}).text.strip()
            date = the_span.find("span", class_="smaller", attrs={"data-qa": "discovery-media-list-item-start-date"}).text.strip()
            f.write(str(index)+')Title: ' + title + '\n')
            f.write('Date: ' + date + '\n')
            f.write('----------------------- \n')
            index+=1
            

        





