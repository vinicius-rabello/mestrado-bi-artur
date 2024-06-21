import pandas as pd
import sqlite3
from tqdm import tqdm
import numpy as np

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

# pegando as colunas da db
colunas = cursor.execute(
    "SELECT name FROM pragma_table_info('Censo31');").fetchall()
colunas = [coluna[0] for coluna in colunas]

## trocando a nacionalidade
join_tables = cursor.execute("SELECT * FROM Censo31 A \
                              LEFT JOIN Nacionalidade31 B \
                              ON A.Nac = B.Cod_nacionalidade").fetchall()

df = pd.DataFrame(join_tables, columns=colunas +
                  ['Cod_nacionalidade', 'Nacionalidade']) # juntandos as tabelas
df['Nac'] = df['Nacionalidade'] # trocando os valores
df['Nac'] = df['Nac'].fillna(value = 'brasileiro') # associando cada valor nulo a brasileiro
df.drop(columns=['Cod_nacionalidade', 'Nacionalidade'], inplace=True) # dropando colunas redundantes

## trocando as raças
join_tables = cursor.execute("SELECT * FROM Censo31 A \
                              LEFT JOIN Raca31 B \
                              ON A.Raça = B.Cod_raça").fetchall()
temp = pd.DataFrame(join_tables, columns=colunas +
                  ['Cod_raça', 'Raça2']) # juntandos as tabelas
df['Raça'] = temp['Raça2'] # trocando os valores

## trocando as condições
join_tables = cursor.execute("SELECT * FROM Censo31 A \
                              LEFT JOIN Condicao31 B \
                              ON A.Condição = B.Cod_condição").fetchall()
temp = pd.DataFrame(join_tables, columns=colunas +
                  ['Cod_condição', 'Condição2']) # juntandos as tabelas
df['Condição'] = temp['Condição2'] # trocando os valores

df.to_excel('database/tables/Censo31_.xlsx', index = False) # salvando