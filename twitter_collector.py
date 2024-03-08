'''

Name: 
Email: 

'''

import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re
import time
import json
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv('email')
PASSWORD = os.getenv('password')
PHONE = os.getenv('phone')

def get_topic():
    # Get the topic from topic.txt
    dag_file_path = os.path.abspath(__file__)
    topic_file_path = os.path.join(os.path.dirname(dag_file_path), 'topic.txt')
    topic = ""
    with open(topic_file_path, 'r') as f:
        topic = f.read()
    return topic

def save_topic(topic, data):
    # Save the topic to {topic}.txt
    dag_file_path = os.path.abspath(__file__)
    topic_file_path = os.path.join(os.path.dirname(dag_file_path), f'{topic}.json')
    with open(topic_file_path, 'w') as f:
        json.dump(data, f)

def setup_driver():
    ## Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    # Set path to chrome/chromedriver as per your configuration
    homedir = os.path.expanduser("~")
    os.chmod(f"{homedir}/chrome-linux64/chrome", 755)
    chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
    os.chmod(f"{homedir}/chromedriver-linux64/chromedriver", 755)
    webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")

    # Choose Chrome Browser
    return Chrome(service=webdriver_service, options=chrome_options)

def run_etl():
    # open driver
    print("This might take a while if it's the first time you're running this. Please be patient.")
    # driver = Chrome('chromedriver')
    driver = setup_driver()
    driver.get('https://www.twitter.com/login')

    # target the input element with name attribute value of text
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="text"]')))
    username.send_keys(EMAIL)
    username.send_keys(Keys.ENTER)

    try:
        password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)
    except:
        phone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="text"]')))
        phone.send_keys(PHONE)
        phone.send_keys(Keys.ENTER)
        password = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password.send_keys(PASSWORD)
        password.send_keys(Keys.ENTER)

    time.sleep(3)
    # get the topic
    topic = get_topic()
    driver.get(f'https://www.twitter.com/search?q={topic}')

    # while length of tweets_collected is less than 100, scroll down
    tweets_collected = {}
    while len(tweets_collected) < 100:
        tweets_arr = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]')))
        for tweet in tweets_arr:
            # extract the tweet text
            tweet_text = WebDriverWait(tweet, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="tweetText"]'))).text
            
            # extract the tweet id
            tweet_id = ""
            tweets_a_tag_arr = WebDriverWait(tweet, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
            for tweet_a_tag in tweets_a_tag_arr:
                match = re.search(r'status/(\d+)', tweet_a_tag.get_attribute('href'))
                if match:
                    tweet_id = match.group(1)
                    break
            if not tweet_id:
                continue
            tweets_collected[tweet_id] = {"tweet_id": tweet_id, "tweet_text": tweet_text}

        driver.execute_script('arguments[0].scrollIntoView(true);', tweets_arr[-1])
        time.sleep(1)

    # close the driver
    driver.close()

    # dump the tweets_collected to a json file
    save_topic(topic, list(tweets_collected.values()))

if __name__ == "__main__":
    run_etl()