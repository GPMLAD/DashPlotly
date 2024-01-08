from scripts.data_manipulation import writeFiles, merge_files
from scripts.web_scraping import news_scrapper
from scripts.dashboard import draw

if __name__ == "__main__":
    #writeFiles()
    #merge_files()
    news = news_scrapper()
    draw(news)