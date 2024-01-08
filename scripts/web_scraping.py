import requests
from bs4 import BeautifulSoup
from datetime import datetime

def news_scrapper():
    urls = {
        'PETR4': 'https://braziljournal.com/?s=petrobras',
        'CEAB3': 'https://braziljournal.com/?s=c%26a',
        'WEGE3': 'https://braziljournal.com/?s=weg'
    }

    companies_data = {}

    for ticker, url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all('figcaption', class_='boxarticle-infos')

            company_data = []
            for i in range(min(3, len(elements))):
                element = elements[i]

                news_type = element.select_one('p.boxarticle-infos-tag a').text
                news_title = element.select_one('h2.boxarticle-infos-title a').text
                link = element.select_one('h2.boxarticle-infos-title a')['href']

                company_data.append({
                    'type': news_type.lstrip(),
                    'title': news_title.lstrip(),
                    'link': link
                })

            companies_data[ticker] = company_data

        else:
            print(f'Falha na solicitação para {ticker}. Código de status: {response.status_code}')

    return companies_data

def stocks_scrapper():
    urls = {
        'PETR4': 'https://www.infomoney.com.br/cotacoes/b3/acao/petrobras-petr4/',
        'CEAB3': 'https://www.infomoney.com.br/cotacoes/b3/acao/cea-ceab3/',
        'WEGE3': 'https://www.infomoney.com.br/cotacoes/b3/acao/weg-wege3/'
    }

    today = datetime.now()

    year = today.year
    month = f'{today.month:02d}'
    day = f'{today.day:02d}'

    companies_data = {}

    for ticker, url in urls.items():
        response = requests.get(url)

        if response.status_code == 200:
            company_data = []
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select('table')[0]
            date_value = f'{year}-{month}-{day}'
            open_value = table.find_all('td')[3].text.strip().replace(',','.')
            high_value = soup.select_one('div.maximo p').text.strip().replace(',','.')
            low_value = soup.select_one('div.minimo p').text.strip().replace(',','.')
            close_value = soup.select_one('div.value p').text.strip().replace(',','.')

            company_data.append([ticker,date_value, open_value,high_value,low_value,close_value])

            companies_data[ticker] = company_data

        else:
            print(f'Falha na solicitação para {ticker}. Código de status: {response.status_code}')

    return companies_data
