from scripts.data_manipulation import merge_files, update_file
from scripts.web_scraping import news_scrapper, stocks_scrapper
from scripts.dashboard import draw
import schedule
import time
import threading
import pandas as pd

df = None
news = None

def job():
    global df
    global news
    news = news_scrapper()
    new_data = stocks_scrapper()
    update_file(new_data)
    merge_files()
    df = pd.read_csv('data/merged_data.csv') 
    print("Data updated.")

def run_dash():
    global df
    merge_files()
    news = news_scrapper()
    df = pd.read_csv('data/merged_data.csv')
    draw(news,df)


    while True:
        schedule.run_pending()
        time.sleep(5)

def update_dataframe():
    global df
    df = pd.read_csv('data/merged_data.csv')
    print("DataFrame updated.")

if __name__ == "__main__":
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.start()

    schedule.every(15).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(5)
