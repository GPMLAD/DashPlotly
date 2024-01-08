import os
import csv
import pandas as pd

def scrap_line_data (line, arr, ticker):
    date_value = f'{line[2:6]}-{line[6:8]}-{line[8:10]}'
    open_value = float(line[56:69])/100
    high_value = float(line[69:82])/100
    low_value = float(line[82:95])/100
    close_value = float(line[108:121])/100
    arr.append([ticker,date_value, open_value,high_value,low_value,close_value])

def writeFiles():
    data_files = ['COTAHIST_A2023.TXT', 'COTAHIST_A2024.TXT']
    tickers = ["PETR4 ", "CEAB3 ", "WEGE3 "]

    for file in data_files:
        file_path = os.path.join('data', file)

        with open(file_path, 'r') as old_file:
            lines = old_file.readlines()

            for ticker in tickers:
                file_name = os.path.join('data', f'{ticker[0:5]}.csv')
                data = []
                file_exists = os.path.isfile(file_name)

                for line in lines:
                    if line[12:18] == ticker:
                        scrap_line_data(line, data, ticker[0:5])

                with open(file_name, 'a', newline='') as new_file:
                    writer = csv.writer(new_file)

                    if not file_exists:
                        writer.writerow(['ticker', 'date', 'open', 'high', 'low', 'close'])

                    writer.writerows(data)


import os
import pandas as pd

def update_file(new_data):
    folder_path = 'data'

    # Verificar se a pasta 'data' existe, senão, criar
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for ticker, data_list in new_data.items():
        # Construir o caminho do arquivo CSV correspondente ao ticker
        file_path = os.path.join(folder_path, f'{ticker}.csv')

        # Verificar se o arquivo já existe
        if os.path.exists(file_path):
            # Ler o arquivo CSV existente para verificar as datas já presentes
            with open(file_path, 'r') as file:
                existing_data = list(csv.DictReader(file))

            # Filtrar as datas já presentes
            existing_dates = set(row['date'] for row in existing_data)

            # Filtrar os novos dados, mantendo apenas os mais recentes
            filtered_new_data = [row for row in data_list if row[0] not in existing_dates]

            # Se houver dados para adicionar, atualizar o arquivo CSV
            if filtered_new_data:
                with open(file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    for row in filtered_new_data:
                        writer.writerow([ticker] + row)
        else:
            # Se o arquivo não existir, criar um novo com os novos dados
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ticker', 'date', 'open', 'high', 'low', 'close'])
                for row in data_list:
                    writer.writerow([ticker] + row)
            
def merge_files():
    # Lista dos tickers
    tickers = ["PETR4", "CEAB3", "WEGE3"]

    # Caminho do diretório de dados
    data_dir = 'data'

    # Lista para armazenar DataFrames dos arquivos de cada ticker
    dfs = []

    # Loop sobre os tickers
    for ticker in tickers:
        # Caminho do arquivo do ticker atual
        file_path = os.path.join(data_dir, f'{ticker}.csv')

        # Verifica se o arquivo existe
        if os.path.exists(file_path):
            # Carrega o DataFrame do arquivo do ticker
            df_ticker = pd.read_csv(file_path)

            # Adiciona o DataFrame à lista
            dfs.append(df_ticker)

    # Verifica se há DataFrames na lista
    if dfs:
        # Concatena os DataFrames
        merged_data = pd.concat(dfs, ignore_index=True)

        # Caminho do arquivo merged_data.csv
        merged_file_path = os.path.join(data_dir, 'merged_data.csv')

        # Salva o DataFrame concatenado no arquivo merged_data.csv
        merged_data.to_csv(merged_file_path, index=False)
        print(f'Successfully merged data to {merged_file_path}')
    else:
        print('No data to merge.')

# Chama a função merge_files
newData = {'PETR4': [['2024-01-08', '38.38', '38.39', '37.61', '38.19']], 'CEAB3': [['2024-01-08', '7.21', '7.61', '7.19', '7.57']], 'WEGE3': [['2024-01-08', '35.86', '36.30', '35.64', '35.95']]}

update_file(newData)