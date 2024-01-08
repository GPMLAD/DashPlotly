from scripts.data_manipulation import writeFiles, merge_files , update_file
from scripts.web_scraping import news_scrapper, stocks_scrapper
from scripts.dashboard import draw

if __name__ == "__main__":
    #writeFiles()
    #merge_files()
    new_data = stocks_scrapper()
    update_file(new_data)
    #news = news_scrapper()
    #draw(news)