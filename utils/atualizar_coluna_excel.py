import pandas as pd
import sqlite3

def atualizar_coluna_excel(db_path, excel_path, column):
    conn = sqlite3.connect(db_path)
    municipios = pd.read_sql(f'SELECT {column} FROM Recibos', conn)[column].tolist()
    df = pd.read_excel(excel_path)
    df['Município'] = municipios
    df.to_excel(excel_path, index=False)

atualizar_coluna_excel('database/test.db', 'database/tables/Recibos.xlsx', 'Município')