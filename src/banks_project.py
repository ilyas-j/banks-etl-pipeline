# Code for ETL operations on Country-GDP data

# Importing the required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime 


def log_progress(message):
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("../logs/code_log.txt", "a") as log_file :
        log_file.write(f"{time_stamp}:{message}\n")

def extract(url, table_attribs):

    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')

    df = pd.DataFrame(columns=table_attribs)

    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')

    for row in rows:
        col = row.find_all('td')   

        if len(col) != 0:

            bank_name = col[1].text.strip()

            market_cap = col[2].text.strip()
            market_cap = float(market_cap[:-1])

            data_dict = {
                "Bank_name": bank_name,
                "MC_USD_Billion": market_cap
            }

            df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)

    return df

def transform(df, csv_path):
    exchange_df = pd.read_csv(csv_path)

    exchange_rate = exchange_df.set_index('Currency').to_dict()['Rate']

    gbp_rate = float(exchange_rate['GBP'])
    eur_rate = float(exchange_rate['EUR'])
    inr_rate = float(exchange_rate['INR'])

    df['MC_GBP_Billion'] = [np.round(x * gbp_rate, 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * eur_rate, 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * inr_rate, 2) for x in df['MC_USD_Billion']]
    return df

def load_to_csv(df, output_path):
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    print(pd.read_sql(query_statement, sql_connection))



url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = ["Bank_name", "MC_USD_Billion"]
db_name = '../output/Banks.db'
table_name = 'Largest_banks'
csv_path = '../data/exchange_rate.csv'
output_path = "../output/Largest_banks_data.csv"




query1 = "SELECT * FROM Largest_banks"
query2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
query3 = 'SELECT Bank_name from Largest_banks LIMIT 5'

log_progress("Preliminaries complete. Initiating ETL process")

df = extract(url, table_attribs)
log_progress("Data extraction complete. Initiating Transformation process")

df = transform(df, csv_path)
log_progress("Data transformation complete. Initiating Loading process")

load_to_csv(df, output_path)
log_progress("Data saved to CSV file")

conn = sqlite3.connect(db_name)
log_progress("SQL Connection initiated")

load_to_db(df, conn, table_name)
log_progress("Data loaded to Database as a table, Executing queries")

run_query(query1, conn)
run_query(query2, conn)
run_query(query3, conn)
log_progress("Process Complete")

conn.close()
log_progress("Server Connection closed")
