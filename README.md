# mars_scrape_webapp_hmwk

This bottcamp homework assignment design a flask application that scrapes Mars data from various websites, save into a mongo db, and render saved data on a new webpage witha  button to refraesh the data.

To run this webapp, first have "mongod" running locally in the background. Then, run app.py, and open the populated URL in a web browser.

Note: I had to put in time.sleep(15) for a couple of the web-scraping pages so the data loads in time, so my web app takes like 45 seconds to load completely.
