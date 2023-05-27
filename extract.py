import json
import re
import numpy as np
import pandas as pd
from datetime import datetime
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
import warnings

# Set this 1 if using own network
TIMEDELAY = 2
NUMBER_OF_WEBPAGES = 10
warnings.filterwarnings("ignore")

def scrape_data(url):
    driver = webdriver.Chrome('chromedriver.exe')
    time.sleep(1)
    driver.get(url)

    time.sleep(TIMEDELAY)
    page_title = driver.title
    print("Scraping reviews for: {}".format(page_title))

    time.sleep(1)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.PAGE_DOWN)

    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)

    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)

    sel = Selector(text=driver.page_source)
    review_counts = sel.css('.lister .header span::text').extract_first()

    if not review_counts:
        driver.quit()
        return None

    review_counts = review_counts.replace(',', '').split(' ')[0]

    if review_counts == '0':
        driver.quit()
        return None

    more_review_pages = int(int(review_counts) / 25)
    print('Review Counts: {}'.format(review_counts))

    for i in tqdm(range(more_review_pages)):
        try:
            css_selector = 'load-more-trigger'
            driver.find_element(By.ID, css_selector).click()
            time.sleep(2)
        except:
            pass

    rating_list = []
    review_date_list = []
    review_title_list = []
    author_list = []
    review_list = []
    review_url_list = []
    error_url_list = []
    error_msg_list = []
    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')

    for d in tqdm(reviews):
        try:
            sel2 = Selector(text=d.get_attribute('innerHTML'))
            try:
                rating = sel2.css('.rating-other-user-rating span::text').extract_first()
                if rating is not None:
                    rating = int(rating)
                    if rating < 5:
                        new_rating = 0
                    elif rating > 5:
                        new_rating = 1
                    else:
                        continue  # Skip rating 5
            except:
                rating = np.NaN
                continue  # Skip if rating is not found

            try:
                review = sel2.css('.text.show-more__control::text').extract_first()
            except:
                review = np.NaN
            try:
                review_date = sel2.css('.review-date::text').extract_first()
            except:
                review_date = np.NaN
            try:
                author = sel2.css('.display-name-link a::text').extract_first()
            except:
                author = np.NaN
            try:
                review_title = sel2.css('a.title::text').extract_first()
            except:
                review_title = np.NaN
            try:
                review_url = sel2.css('a.title::attr(href)').extract_first()
            except:
                review_url = np.NaN
            rating_list.append(rating)
            review_date_list.append(review_date)
            review_title_list.append(review_title)
            author_list.append(author)
            review_list.append(review)
            review_url_list.append(review_url)
        except Exception as e:
            error_url_list.append(url)
            error_msg_list.append(str(e))

    driver.quit()

    review_df = pd.DataFrame({
        'Review_Date': review_date_list,
        'Author': author_list,
        'Rating': rating_list,
        'Review_Title': review_title_list,
        'Review': review_list,
        'Review_Url': review_url_list
    })

    # Create a new column 'new_rating' based on the conditions
    review_df['new_rating'] = np.where(review_df['Rating'] < 5, 0, 1)

    return review_df


dfs = []
error_urls = []
error_msgs = []

for count in tqdm(range(NUMBER_OF_WEBPAGES)):
    url = 'https://www.imdb.com/title/tt{:07d}/reviews/?ref_=tt_ov_rt'.format(count)
    try:
        df = scrape_data(url)
        if df is not None:
            dfs.append(df)
    except Exception as e:
        error_urls.append(url)
        error_msgs.append(str(e))

if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)

    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

    combined_df.to_csv('combined_reviews_{}.csv'.format(current_time), index=False)

    if error_urls:
        error_data = pd.DataFrame({'URL': error_urls, 'Error': error_msgs})
        error_data.to_csv('scraping_errors_{}.csv'.format(current_time), index=False)

    print(combined_df)
else:
    print("No valid data was scraped.")
