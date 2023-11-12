from bs4 import BeautifulSoup
import requests



def scrapemovie(movie_name):
    url = f'https://www.rottentomatoes.com/search?search={movie_name}&'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies= soup.find_all('search-page-media-row')
    with open('movies/' + movie_name + '.txt', 'w') as f:
        index=1
        for movie in movies:
            print(index)
            year='invalide'
            title=movie.find("a", attrs={"data-qa": "info-name"}).text.strip() # u need to search by attribute 
            #movie_img=movie.find("a", attrs={"data-qa": "thumbnail-link"}).img['src']  # here i can use the same thing to scrape the img
            year = movie.get("releaseyear")#--------- if it is like an attribute in he tag , u have to use this insead
            cast = movie.get("cast")
            if year=='':
                year='indisponible'
            if cast=='':
                cast='indisponible'
            f.write(str(index)+')Title: ' + title + '\n')
            f.write('Year: ' + year + '\n')
            f.write('Cast: ' + cast + '\n')
            f.write('----------------------- \n')
            index+=1

        





