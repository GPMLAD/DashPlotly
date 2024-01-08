from scripts.data_manipulation import writeFiles, merge_files , update_file
from scripts.web_scraping import news_scrapper, stocks_scrapper
from scripts.dashboard import draw
import schedule
import time
import threading

"""

def teste2():
    news = news_scrapper()
    print("Deu certo" if news else "Deu errado")

def teste():
    news = news_scrapper()
    print("Deu certo" if news else "Deu errado")
    schedule.every(10).seconds.do(teste2)

    while True:
        schedule.run_pending()
        time.sleep(1)

"""

def job():
    global news
    news = news_scrapper()
    new_data = stocks_scrapper()
    update_file(new_data)
    merge_files()
    print("Data updated.")

def run_dash():
    # Inicialização dos dados e do gráfico
    #writeFiles()
    merge_files()
    news = news_scrapper()
    draw(news)

if __name__ == "__main__":
    # Inicia a thread do Dash
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.start()

    # Schedule para a função job
    schedule.every(15).seconds.do(job)

    while True:
        print("Entrou")
        schedule.run_pending()
        time.sleep(5)
