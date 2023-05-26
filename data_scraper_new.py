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

warnings.filterwarnings("ignore")

# List of URLs
url_list = [
    'https://www.imdb.com/title/tt0241527/reviews?ref_=tt_sa_3',
    'https://www.imdb.com/title/tt6791350/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt7660850/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt5433140/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt10986410/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt6968614/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt14688458/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt16419074/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt27528139/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt14661396/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt6718170/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt2906216/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt13345606/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt4873118/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt14586350/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt14846026/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0413573/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0364845/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0203259/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0386676/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0137523/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0120737/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0133093/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0167260/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0167261/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0114369/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0172495/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0372784/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0120815/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0120689/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0209144/reviews/?ref_=tt_ov_rt',
    'https://www.imdb.com/title/tt0120338/reviews/?ref_=tt_ov_rt'
    # Add more URLs here
]

# Function to scrape data for a given URL
def scrape_data(url):
    driver = webdriver.Chrome('chromedriver.exe')
    time.sleep(1)
    driver.get(url)

    time.sleep(1)
    page_title = driver.title
    print("Scraping reviews for: {}".format(page_title))
    hyphen_index = page_title.find('-')
    extracted_title = page_title[:hyphen_index].strip()
    cleaned_title = re.sub(r'\s+', '_', extracted_title.lower())
    cleaned_title = re.sub(r'[^\w\s-]', '', cleaned_title)
    print("Cleaned title FOR TESTING: {}".format(cleaned_title))

    time.sleep(1)
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.PAGE_DOWN)

    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)

    time.sleep(1)
    body.send_keys(Keys.PAGE_DOWN)

    sel = Selector(text=driver.page_source)
    review_counts = sel.css('.lister .header span::text').extract_first().replace(',', '').split(' ')[0]
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
            error_msg_list.append(e)

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


# Scrape data for each URL and combine the results
dfs = []
for url in url_list:
    df = scrape_data(url)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# Get current date and time for the output filename
now = datetime.now()
current_time = now.strftime("%Y_%m_%d_%H_%M_%S")

# Save the combined dataframe to a CSV file
combined_df.to_csv('combined_reviews_{}.csv'.format(current_time), index=False)

print(combined_df)
