import pandas as pd
import sqlite3

conn = sqlite3.connect('database/test.db')
ocupacoes = pd.read_sql("SELECT DISTINCT B.Ocup FROM Recibos A\
                          LEFT JOIN Censo31 B \
                          ON A.IdProdutor = B.Id \
                          WHERE A.IdProdutor NOT NULL", conn)

codes = ocupacoes['Ocup'].tolist()
df = pd.read_excel('database/tables/Ocupacao31.xlsx', header=None, names=['codigo', 'ocupacao'])
idx = []
for code in codes:
    temp = df.loc[df['codigo'] == code]
    print(f'Escolha qual a ocupação do código {code}:\n')
    for i in temp['codigo'].index.values.tolist():
        print(f'Para escolher {temp['ocupacao'].loc[i]} digite {i}')
    escolha = input('Digite o código: ')
    idx.append(escolha)

new_df = df.iloc[idx].to_excel('database/tables/ocupacoes_recibo.xlsx', index=False)
print(df.iloc[idx])