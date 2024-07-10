import pandas as pd
import sqlite3
import time

# convert table from db to excel sheet
def convert_to_excel(sheet_name, db_path, table_name):
    start_time = time.time()
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f'SELECT * FROM {table_name}', conn)
    df.to_excel(sheet_name, index=False)
    print(f'{table_name} foi transformado numa planilha de excel.')
    print(f'Levou {time.time() - start_time} segundos!')


convert_to_excel('database/tables/Recibos.xlsx',
                 'database/test.db', 'Recibos')
