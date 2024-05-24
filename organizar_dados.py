import pandas as pd
import sqlite3

# conectando na base de dados
connection = sqlite3.connect('database/database.db')
cursor = connection.cursor()

# pegando as colunas da db
colunas = cursor.execute(
    "SELECT name FROM pragma_table_info('Censo31');").fetchall()
colunas = [coluna[0] for coluna in colunas]

# trocando o código de munícipio para o nome
join_tables = cursor.execute(
    'SELECT A.*, B.Município AS NomeMunicípio FROM Censo31 A LEFT JOIN Municipios31 B ON A.Município = B.Cod_Município').fetchall()

df = pd.DataFrame(data=join_tables, columns=colunas + ['municipio_nome'])
df['Município'] = df['municipio_nome']
df.drop(columns = ['municipio_nome'], inplace = True)

# salvando mudanças na database
df.to_sql('Censo31',con=connection,if_exists='replace', index=False)
print('Mudanças salvas na base de dados.')