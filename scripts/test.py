import pandas as pd
import sqlite3

colunas_censo_total = pd.read_excel('database/tables/Censo31.xlsx').columns
print(colunas_censo_total)