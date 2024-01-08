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

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for ticker, data_list in new_data.items():
        file_path = os.path.join(folder_path, f'{ticker}.csv')

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = list(csv.DictReader(file))

            existing_dates_indices = {row['date']: index for index, row in enumerate(existing_data)}

            for new_row in data_list:
                date = new_row[0]
                if date in existing_dates_indices:
                    existing_data[existing_dates_indices[date]] = {'ticker': ticker, 'date': date, 'open': new_row[1], 'high': new_row[2], 'low': new_row[3], 'close': new_row[4]}
                else:
                    existing_data.append({'ticker': ticker, 'date': date, 'open': new_row[1], 'high': new_row[2], 'low': new_row[3], 'close': new_row[4]})

            with open(file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['ticker', 'date', 'open', 'high', 'low', 'close'])
                writer.writeheader()
                writer.writerows(existing_data)
        else:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ticker', 'date', 'open', 'high', 'low', 'close'])
                writer.writerows([[ticker] + row for row in data_list])

            
def merge_files():
    tickers = ["PETR4", "CEAB3", "WEGE3"]
    data_dir = 'data'
    dfs = []

    for ticker in tickers:
        file_path = os.path.join(data_dir, f'{ticker}.csv')

        if os.path.exists(file_path):
            df_ticker = pd.read_csv(file_path)

            dfs.append(df_ticker)

    if dfs:
        merged_data = pd.concat(dfs, ignore_index=True)

        merged_file_path = os.path.join(data_dir, 'merged_data.csv')
        
        merged_data.to_csv(merged_file_path, index=False)
        
    else:
        print('No data to merge.')
