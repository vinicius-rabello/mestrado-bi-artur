import pandas as pd

df = pd.read_excel('database/tables/Censo31_esc.xlsx')
numero_escravizados = df['Num_Escravos'].tolist()
print(len(numero_escravizados))