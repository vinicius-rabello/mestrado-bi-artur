import pandas as pd
import sqlite3

conn = sqlite3.connect('database/test.db')
df = pd.read_sql(f'SELECT * FROM Recibos', conn)
df.to_excel("database/tables/teste_recibos_sql.xlsx", index=False)