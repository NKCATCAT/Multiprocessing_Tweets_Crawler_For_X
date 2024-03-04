#Packages
import time
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# Leave out long tweets (Long Tweets are saved in another container).
def filter_show_more(html):
    soup = BeautifulSoup(html, 'html.parser')
    tweet_texts = soup.find_all(attrs = {"data-testid": "tweet"})
    if len(tweet_texts) > 0:
        for tweet_text in tweet_texts:
            if tweet_text.find(attrs = {"data-testid": "tweet-text-show-more-link"}):
                tweet_text.decompose()
    return soup
# Click to show full text of long tweets.

def find_show_more_buttons(driver, page_sources_2):
    i = 0
    while True:
        try:
            show_more_buttons = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet-text-show-more-link"]')
            if i >= len(show_more_buttons) - 1:
                break
            show_more_button = show_more_buttons[i]
        except NoSuchElementException:
            logging.info("Info: No show more button found \nState: Query proceeded \nPage: The query page")
            break
        
        # Execute JavaScript to click the button
        try:
            driver.execute_script("arguments[0].click();", show_more_button)
        except:
            logging.error("Error: Cannot click the show more button \nState: Show more buttons detected \nPage: The tab page")
            print("Cannot click the show more button")
        time.sleep(6)

        show_more_page_source = driver.page_source
        page_sources_2.append(BeautifulSoup(show_more_page_source, 'html.parser'))

        driver.back()
        i += 1
    return driver, page_sources_2