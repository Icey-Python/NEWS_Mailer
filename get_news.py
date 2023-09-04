from bs4 import BeautifulSoup
import requests
import threading
import json
from concurrent.futures import ThreadPoolExecutor

url = "https://www.the-star.co.ke/news/"
endpoints_news = [
  "realtime/","world/","africa/","twitter-space/","fact-checker/"
]
article_links = []
the_star_news = []

def get_endpoint_to_url(endpoint:str):
  url = "https://www.the-star.co.ke/news/" +endpoint
  raw_data = requests.get(url)
  
  parsed_data = BeautifulSoup(raw_data.content, 'html.parser')
  #find all news articles
  articles = parsed_data.find_all('div', {'class': 'section-article'})

  #get the whole story link
  for article in articles:
    article_anchor_link = article.find('a')
    article_full_link = article_anchor_link.get('href')
  
    article_links.append(article_full_link)


def scrape_article_content(url: str):
  data = requests.get(url)
  if data.status_code == 200:
    article_content = BeautifulSoup(data.content, 'html.parser')

  #article title and subtitle
    title = article_content.find('h1', {
        'class': 'article-title-primary'
    }).get_text()
    sub_title = article_content.find('h3', {
        'class': 'article-title-tertiary'
    }).get_text()
    #getting artcle summary
    article_intro = article_content.find(
        'div', {'class': 'article-intro-container'})
    #news content
    try:
      full_news_content = article_content.find('div', {
          'class': 'article-widget-text'
      }).get_text()
    except AttributeError:
      full_news_content = ''

    try:
      #getting the image
      article_image = article_content.find('a', {
          'class': 'image'
      }).get('href')

      #getting the text from the image
      article_image_text = article_content.find('div', {
          'class': 'image-text'
      }).get_text()
    except AttributeError:
      article_image = ''
      article_image_text = ''

    #handling NoneType error
    if article_intro is None:
      article_intro = ""
    else:
      article_intro = article_intro.get_text()
    if article_content == '' or full_news_content =='':
      pass
    else:
      the_star_news.append({
          "title":
          title,
          "sub_title":
          sub_title,
          "summary":
          article_intro,
          "content":
          full_news_content,
          "image":
          f"https:{article_image}",
          "image_text":
          article_image_text,
          "source_link":
          "https://www.the-star.co.ke/publication/custom/static/logo.png",
          "category":url
      })
    
# Create a ThreadPoolExecutor with a specified number of threads (e.g., 4)
with ThreadPoolExecutor(max_workers=3) as executor:
    # Use the executor to concurrently scrape the article content for each endpoint
    futures = [executor.submit(scrape_article_content, f"https://www.the-star.co.ke/{i}") for i in article_links]

    # Wait for all tasks to complete
    for future in futures:
        future.result()


with open("scrapped_news.json","w") as file:
  json.dump(the_star_news,file)

print("done")

# import make_pdf



