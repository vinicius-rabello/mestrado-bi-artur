import pandas as pd

df = pd.read_excel('database/tables/Recibos.xlsx')
df['IdArrecadador'] = None
df.to_excel('database/tables/Recibos.xlsx', index=False)