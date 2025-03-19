import pandas as pd
import sqlite3
from tqdm import tqdm
import numpy as np

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

colunas = cursor.execute(
    "SELECT name FROM pragma_table_info('Censo31');").fetchall()
colunas = [coluna[0] for coluna in colunas]

# pegando as colunas da db
df = cursor.execute(
    "SELECT * FROM Censo31 \
    WHERE Ocup = 39 AND Nome NOT LIKE '%Padre%' AND Nome NOT LIKE '%Rever%' AND Nome NOT LIKE '%Vigár%'").fetchall()

df = pd.DataFrame(data=df, columns=colunas)
df.to_excel('database/tables/dizimeiros.xlsx', index=False)