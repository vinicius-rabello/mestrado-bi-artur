import pandas as pd

df = pd.read_excel('database/tables/Recibos.xlsx')
try:
    _ = df['Produtor']
    print('wfsaomsa')
except:
    print(0)