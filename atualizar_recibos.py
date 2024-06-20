import pandas as pd
import sqlite3

conn = sqlite3.connect('database/test.db')
# pegando a coluna IdProdutor da base de dados
coluna_id_produtor = pd.read_sql(f'SELECT IdProdutor FROM Recibos', conn)[
    'IdProdutor'].tolist()
# lendo a planilha recibos
recibos = pd.read_excel('database/tables/Recibos.xlsx')

# atualizando a coluna id produtor
recibos['IdProdutor'] = coluna_id_produtor
recibos.to_excel('database/tables/Recibos.xlsx',
                 sheet_name='Tabela', index=False)
