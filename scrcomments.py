import requests
from bs4 import BeautifulSoup
import re

def scrapecomments(url):
    sanitized_file_name = re.sub(r'[^a-zA-Z0-9.-]', '_', url)
    file_path = 'video_comments/' + sanitized_file_name + '.txt'      
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    print("here2")
    with open(file_path, 'w') as f:
            f.write("externe")
            f.close
    div0=soup.find('div',class_='style-scope ytd-app')
    print(div0)
    comments = div0.find('h2', class_='style-scope ytd-comments-header-renderer')
    print(comments)
    for comment in comments:
        print("here3")
        commenter_name = comment.find('a', class_='yt-simple-endpoint').text.strip()
        comment_content = comment.find('span', class_='style-scope yt-formatted-string').text.strip()
        with open(file_path, 'w') as f:
            f.write("interne\n")
            f.write('Commenter name:', commenter_name)
        print('Comment content:', comment_content)
        print('---')

