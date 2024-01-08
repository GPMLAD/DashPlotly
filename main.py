from scripts.data_manipulation import merge_files, update_file
from scripts.web_scraping import news_scrapper, stocks_scrapper
from scripts.dashboard import create_dash_app
import schedule
import time
import pandas as pd
import threading

df = pd.DataFrame()
news = []

def job():
    global df
    global news
    news = news_scrapper()
    new_data = stocks_scrapper()
    update_file(new_data)
    merge_files()
    df = pd.read_csv('data/merged_data.csv')
    print("Data updated.")

def run_dash(environ, start_response):
    global df
    merge_files()
    news = news_scrapper()
    df = pd.read_csv('data/merged_data.csv')
    
    app = create_dash_app(news, df)
    app.run_server(debug=False)

    while True:
        schedule.run_pending()
        time.sleep(5)

def update_dataframe():
    global df
    df = pd.read_csv('data/merged_data.csv')
    print("DataFrame updated.")

if __name__ == "__main__":
    schedule.every(15).seconds.do(job)

    dash_thread = threading.Thread(target=run_dash)
    dash_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(5)
