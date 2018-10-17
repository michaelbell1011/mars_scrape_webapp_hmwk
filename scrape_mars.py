from splinter import Browser
from bs4 import BeautifulSoup
import time
import re
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    # open chrome web driver
    browser = init_browser()

    # create mars_data dict that we can insert into mongo
    mars_docs = {}

    ################################
    # get latest Mars news from NASA
    
    # visit NASA mars news website 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve first instance (not all (find_all)) of element that contains article text.
    top_headline = soup.find('div', class_='list_text')
    # save title and article body elements
    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='list_text').find('div', class_='article_teaser_body').get_text()
    # add elements to mars_data dict...
    mars_docs["news_title"] = news_title
    mars_docs["news_p"] = news_p

    #################################
    # get featured image from NASA

    # visit NASA Jet Propulsion Lab website to get featured image URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    # navigate to view featured image
    browser.click_link_by_partial_text('FULL IMAGE')
    # note the above page sometimes takes a long time to load and the 'more info' button isnt available
    time.sleep(15)
    browser.click_link_by_partial_text('more info')

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Save the image url to a variable called `img_url`
    # build out full url for image
    image_partial_url = soup.find("img", class_="main_image")["src"]
    featured_image_url = "https://www.jpl.nasa.gov"+image_partial_url
    # add element to mars_data dict...
    mars_docs["featured_image_url"] = featured_image_url


    ######################################
    # get latest Mars weather

    # visit mars weather twitter feed
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    # give browser enough time to load relevant tweet if not near top
    time.sleep(15)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # find and save first available tweet which begins with "Sol"; 
    # their reporting convention for weather updates
    mars_weather=soup.find(string=re.compile("Sol"))
    # add element to mars_data dict...
    mars_docs["mars_weather"] = mars_weather

    #########################################
    # get Mars facts table

    # vist source webpage
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    # use pandas to detect table on the page
    facts_table = pd.read_html(url)
    # convert to df and clean up
    facts_df = facts_table[0]
    facts_df.columns = ['Description', 'Value']
    facts_df.set_index("Description", inplace= True)
    # compile html for just table
    facts_html = facts_df.to_html()
    # add element to mars_data dict...
    mars_docs["facts_html"] = facts_html


    ###############################################
    # Get Mars Hemispheres images
    hemisphere_image_urls = []
    urls = []

    # visit USGS Astrogeology site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # get urls for available views
    items = soup.find_all('div', class_="description")
    for item in items:
        urls.append(item.a['href'])

    # iterate thru url locations and get image urls
    for i in urls:
        url = 'https://astrogeology.usgs.gov' + i
        browser.visit(url)
        # get new soup html
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # store in dict hemisphere name and image URL
        dict = {}
        title = soup.find('div', class_="content").find('h2').text
        partial_url = soup.find('img', class_="wide-image")["src"]
        img_url = 'https://astrogeology.usgs.gov' + partial_url
        dict["title"]= title
        dict["img_url"]= img_url
        hemisphere_image_urls.append(dict)

    # add element to mars_data dict...
    mars_docs["hemisphere_image_urls"] = hemisphere_image_urls

    #########################################################################
    # close chrome driver
    browser.quit()
    return mars_docs


# # helper function to build surf report
# def build_report(surf_report):
#     final_report = ""
#     for p in surf_report:
#         final_report += " " + p.get_text()
#         print(final_report)
#     return final_report
