#!/usr/bin/env python
# coding: utf-8
#importing libraries
import pandas as pd
#BeautifulSoup - Library that allows us to scrap content from a webpage

from bs4 import BeautifulSoup as bs

#Python Module for browser interactions
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

import time

def scrape():
    mars_output = mars_mission()

    #return mars_output 
    return convert_dict_to_list(mars_output)

#converting to list

def convert_dict_to_list(d):
    l = []
    for k, v in d.items():
        l.append({k: v})

    return l

#Window Users - chromedriver.exe file in the same location as this .ipynb file, or need to provide the path to the executable

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)
    
    #browser = Browser('chrome', **executable_path,headless=False)
    #12-WebScraping-and-NoSQL\web-scraping-challenge\Mission to Mars


def mars_mission():

    #Empty dictionary to store all scraping resutls

    mars_details = {}

    #1) scrapping for latest Mars news from NASA 

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    #browser = init_browser()
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path,headless=False)

    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup=bs(html,'html.parser')
    


    all_titles = soup.find_all('div',class_="list_text")

    news_title = all_titles[0].a.text
    print(f"Title : {news_title}")

    news_p=all_titles[0].find('div',class_="article_teaser_body").text
    print(f"First Paragraph : {news_p}")

    mars_details["point1"] = news_title
    mars_details["point2"] = news_p

    
    #2) scrapping the latest image url for .jpg image

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser = init_browser()
    browser.visit(image_url)

    time.sleep(1)

    image_html = browser.html
    soup = bs(image_html,'html.parser')

    jpg_url = soup.find_all('ul',class_='articles')[0].find('a',class_="fancybox").get('data-fancybox-href')
    #print(jpg_url)

    base_url = "https://www.jpl.nasa.gov"

    featured_image_url = base_url + jpg_url

    print(f"JPG Url :- {featured_image_url}")

    mars_details["point3"] = featured_image_url

    browser = init_browser()
    browser.visit(featured_image_url)

    time.sleep(0.5)


    #3) Scraping for Mars weather from twitter 

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser = init_browser()
    browser.visit(weather_url)

    time.sleep(1)

    weather_html = browser.html
    soup=bs(weather_html,'html.parser')

    # getting latest tweet for mars weather

    all_tweets = soup.find_all('div',class_="js-tweet-text-container")

    a = all_tweets[0].find('p')
    mainstrng = str(a)
    #type(mainstrng)

    b = all_tweets[0].find('a')
    sub = str(b)
    #type(sub)

    result = mainstrng.replace(sub,'')

    mars_weather = bs(result).body.p.text.strip()
    print(mars_weather)

    mars_details["point4"] = mars_weather

    #Latest tweet from another class below
    first_tweet = soup.find_all('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0]


    sub = str(first_tweet.find('a'))
    mainstrng = str(first_tweet)

    import re
    res = re.sub(sub, '',mainstrng) 
    mars_weather = bs(res).body.p.text.strip()
    print(mars_weather)

    #4) scraping for Mars facts 

    table_url = "https://space-facts.com/mars/"

    #browser = init_browser()
    #browser.visit(table_url)

    #Pandas read_html scrapes tabular data from the page

    tables = pd.read_html(table_url)

    #print(len(tables))

    details = tables[0]
    details.columns = ["Dimension","Value"]
    #details

    #pandas to_html generates html table from data frame

    details_table = details.to_html()
    #details_table

    details_table.replace('\n','')

    details.to_html('details.html',index=False)

    #!explorer details.html(index=False)

    mars_details["point5"] = 'details.html'

    #5) scraping for Mars hemispheres

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = init_browser()
    browser.visit(hemispheres_url)
    time.sleep(1)

    hemispheres_html = browser.html
    soup = bs(hemispheres_html,'html.parser')

    #soup.prettify()

    details = soup.find_all('div',class_="description")
    #details

    # create a dictionary for each book and append it to the books list

    hemisphere_image_urls = []

    for d in details:
        title = d.find('h3').text.strip()
        #print(d.find('h3'))

        base_url = "https://astrogeology.usgs.gov/"
        enhanced_url = base_url + d.a['href']
        browser.visit(enhanced_url)
        time.sleep(1)
        browser2_html = browser.html
        browser2_soup = bs(browser2_html,'html.parser')
        browser2_soup.find_all('div',class_="wide-image-wrapper")
        img_url = browser2_soup.find_all('div',class_="wide-image-wrapper")[0].find_all('li')[0].a['href']
        #print(img_url)
        hemisphere_image_urls.append({'title':title,'img_url':img_url})
    
    
    #hemisphere_image_urls
    
    mars_details["point6"] = hemisphere_image_urls

    print(mars_details)

    return mars_details
          









































                                                            