from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



def scrape():
    browser = init_browser()
    mars_data = {}

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    header = soup.find('div', class_='content_title')
    title = header.find().text
    article = soup.find('div', class_='rollover_description_inner').text
    mars_data["headline"] = title
    mars_data["article"] = article

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(2)
    browser.click_link_by_partial_text('FULL')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    img_url = jpl_soup.find('img', class_='main_image')
    src_url = img_url.get('src')
    full_url = "https://www.jpl.nasa.gov" + src_url
    mars_data["jpl_image"] = full_url

    twitter = "https://twitter.com/marswxreport?lang=en"
    twitter_request = requests.get(twitter)
    twitter_soup = BeautifulSoup(twitter_request.text, 'html.parser')
    tweet = twitter_soup.find('div', class_="js-tweet-text-container")
    mars_weather = tweet.text
    mars_data["weather"] = mars_weather

    facts_url = 'https://space-facts.com/mars/'
    facts = pd.read_html(facts_url)
    df = facts[0]
    df=df.rename(columns={0:"Description", 1:"Value"})
    html_table = df.to_html(index=False)
    html_table.replace('\n', '')
    df.to_html('table.html')
    mars_data["facts"] = html_table

    hemispheres_url = 'https://astrogeology.usgs.gov'
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []


    for item in items:
        title = item.find('h3').text.strip(' Enhanced')
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(hemispheres_url + partial_img_url)
        time.sleep(10)
        partial_img_html = browser.html
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        img_url = hemispheres_url + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    mars_data["hemispheres"] = hemisphere_image_urls     

    browser.quit()
    
    return mars_data


