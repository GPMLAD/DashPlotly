import requests
from bs4 import BeautifulSoup

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

                # Adicionar dados ao dicionário
                company_data.append({
                    'type': news_type.lstrip(),
                    'title': news_title.lstrip(),
                    'link': link
                })

            # Adicionar dados ao dicionário principal
            companies_data[ticker] = company_data

        else:
            print(f'Falha na solicitação para {ticker}. Código de status: {response.status_code}')

    return companies_data

# Chamar a função
dados_noticias = news_scrapper()

# print(dados_noticias["PETR4"][0]["link"])
