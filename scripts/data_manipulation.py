import os
import csv
import pandas as pd

def scrap_line_data (line, arr, ticker):
    data_value = f'{line[2:6]}-{line[6:8]}-{line[8:10]}'
    open_value = float(line[56:69])/100
    high_value = float(line[69:82])/100
    low_value = float(line[82:95])/100
    close_value = float(line[108:121])/100
    arr.append([ticker,data_value, open_value,high_value,low_value,close_value])

def writeFiles():
    data_files = ['COTAHIST_A2023.TXT', 'COTAHIST_A2024.TXT']
    tickers = ["PETR4 ", "CEAB3 ", "WEGE3 "]

    for file in data_files:
        caminho_arquivo = os.path.join('data', file)

        with open(caminho_arquivo, 'r') as arquivo:
            lines = arquivo.readlines()

            for ticker in tickers:
                file_name = os.path.join('data', f'{ticker[0:5]}.csv')
                data = []
                file_exists = os.path.isfile(file_name)

                for line in lines:
                    if line[12:18] == ticker:
                        scrap_line_data(line, data, ticker[0:5])

                with open(file_name, 'a', newline='') as arquivo_csv:
                    escritor_csv = csv.writer(arquivo_csv)

                    if not file_exists:
                        escritor_csv.writerow(['ticker', 'date', 'open', 'high', 'low', 'close'])

                    escritor_csv.writerows(data)

def merge_files():
    data_folder = 'data'
    output_file = os.path.join(data_folder, 'merged_data.csv')
    merged_data = pd.DataFrame()

    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(data_folder, filename)
            df = pd.read_csv(filepath)
            merged_data = pd.concat([merged_data, df], ignore_index=True)

    # Salvar o arquivo combinado
    merged_data.to_csv(output_file, index=False)
