import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import pymongo

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    response = browser.html
    soup = bs(response, 'html.parser')

    article = soup.find("div", class_='list_text')
    news_title = article.find('div', class_='content_title').find('a').text
    news_p = article.find('div', class_='article_teaser_body').text

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    image_html = browser.html
    images_soup = bs(image_html, 'html.parser')
    
    images_url = images_soup.find_all('img')[3]["src"]
    base_url = 'https://www.jpl.nasa.gov'
    featured_image_url = base_url + images_url 
    
    fact_url = 'https://space-facts.com/mars/'
    fact_df = pd.read_html(fact_url)
    mars_fact_df = fact_df[2]
    mars_fact_df.columns = ["Description", "Data"]
    mars_html_table = mars_fact_df.to_html()
    mars_html_table.replace('\n', '')

    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeology_url)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')
    
    hemisphere = hemisphere_soup.find("div", class_='collapsible results')

    hemisphere_title = hemisphere.find("div", class_='description').h3.text
    base_link = 'https://astrogeology.usgs.gov'
    hemisphere_link = base_link + hemisphere.a['href']
    
    hemisphere_image_urls = []

    for i in hemisphere:
        hemisphere_title = hemisphere.find("div", class_='description').h3.text
    
        base_link = 'https://astrogeology.usgs.gov'
        hemisphere_link = hemisphere.a['href']
        browser.visit(base_link + hemisphere_link)
        
        hemisphere_image_html = browser.html
        hemisphere_image_soup = bs(hemisphere_image_html, 'html.parser')
        
        image_link = hemisphere_image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']
        
        image_dict = {}
        image_dict['title'] = hemisphere_title
        image_dict['img_url'] = hemisphere_link
        
        hemisphere_image_urls.append(image_dict)