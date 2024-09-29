from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def get_article_content(driver, url):
    driver.get(url)
    article_content = []
    paragraphs = driver.find_elements(By.TAG_NAME, 'p')
    for p in paragraphs:
        article_content.append(p.text.strip())
    return '\n'.join(article_content)

def extract_articles(homepage_url):
    options = Options()
    options.headless = True
    service = Service('driver path here') 

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(homepage_url)
    
    all_content = ""
    article_links = driver.find_elements(By.CSS_SELECTOR, 'a.article-link')
    for link in article_links:
        article_link = link.get_attribute('href')
        full_article_url = article_link if article_link.startswith('http') else f'https://www.livescience.com{article_link}'
        print(f"Fetching article from: {full_article_url}")
        article_content = get_article_content(driver, full_article_url)
        all_content += article_content + "\n\n"
        
        file_name = article_link.split('/')[-1].replace('-', '_') + '.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(article_content)
        print(f"Article content has been extracted for the url {file_name}")
        print("#" * 10)
        print(f"Article content saved as {file_name}")
        print("#" * 100)
        time.sleep(5)

    driver.quit()

    with open('all_content_in_one_file.txt', 'w', encoding='utf-8') as f:
        f.write(all_content)

    return "Article extraction has been completed successfully"

if __name__=="__main__":
    url = "https://www.livescience.com/"
    extract_articles(url)
