import requests
from bs4 import BeautifulSoup
import time

def get_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_content = []
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        article_content.append(p.get_text().strip())
    return '\n'.join(article_content)

def extract_articles(homepage_url):
    all_content=""
    response = requests.get(homepage_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = []
    links = soup.find_all('a', class_='article-link')
    for link in links:
        article_links.append(link['href'])
    for article_link in article_links:
        full_article_url = article_link
        if not full_article_url.startswith('http'):
            full_article_url = 'https://www.livescience.com' + article_link
        print(f"Fetching article from: {full_article_url}")
        article_content = get_article_content(full_article_url)
        #all_content=all_content.append(article_content)
        all_content += article_content + "\n\n"
        file_name=article_link.split('/')[-1].replace('-', '_') + '.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(article_content)
        print(f"Article content has been extracted for the url {file_name}")
        print("#" * 10)
        print(f"Article content saved as {file_name}")
        print("#" * 100)
        time.sleep(5)
    with open('all_content_in_one_file.txt', 'w', encoding='utf-8') as f:
        f.write(all_content)
    return "Article extraction has been completed successfully"

if __name__=="__main__":
    url= "https://www.livescience.com/"
    extract_articles(url)


