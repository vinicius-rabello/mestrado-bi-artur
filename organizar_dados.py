import pandas as pd
import sqlite3
from tqdm import tqdm

# conectando na base de dados
connection = sqlite3.connect('database/database.db')
cursor = connection.cursor()

# pegando as colunas da db
colunas = cursor.execute(
    "SELECT name FROM pragma_table_info('Censo31');").fetchall()
colunas = [coluna[0] for coluna in colunas]

# trocando o código de distrito para o nome
municipio_distrito = cursor.execute(
    'SELECT Município, Distrito FROM Censo31').fetchall()

# pegando a tabela
data = cursor.execute(
    'SELECT * FROM Censo31').fetchall()

# trocando os códigos de distrito
coluna_distritos = []
for entrada in tqdm(municipio_distrito):
    cod_municipio, cod_distrito = str(entrada[0]), str(entrada[1])
    if len(cod_distrito) > 2:
        codigo = cod_distrito
    elif len(cod_municipio) == 2:
        if len(cod_distrito) == 2:
            codigo = cod_municipio + cod_distrito
        elif len(cod_distrito) == 1:
            codigo = cod_municipio + '0' + cod_distrito
        else:
            codigo = ''
    elif len(cod_municipio) == 1:
        if len(cod_distrito) == 2:
            codigo = cod_municipio + cod_distrito
        elif len(cod_distrito) == 1:
            codigo = cod_municipio + '0' + cod_distrito
        else:
            codigo = ''
    else:
        codigo = ''

    coluna_distritos.append(codigo)

df = pd.DataFrame(data=data, columns=colunas)
df['Distrito'] = coluna_distritos

# salvando mudanças na database
df.to_sql('Censo31', con=connection, if_exists='replace', index=False)
print('Códigos de Distrito atualizados na base de dados.')

# trocando o código de munícipio para o nome
join_tables = cursor.execute(
    'SELECT A.*, B.Município AS NomeMunicípio FROM Censo31 A LEFT JOIN Municipios31 B ON A.Município = B.Cod_Município').fetchall()

df = pd.DataFrame(data=join_tables, columns=colunas + ['municipio_nome'])
df['Município'] = df['municipio_nome']
df.drop(columns=['municipio_nome'], inplace=True)

# salvando mudanças na database
df.to_sql('Censo31', con=connection, if_exists='replace', index=False)
print('Nomes de Município atualizados na base de dados.')

# trocando o código de distrito para o nome
join_tables = cursor.execute(
    'SELECT A.*, B.Distrito AS NomeDistrito FROM Censo31 A LEFT JOIN Distrito31 B ON A.Distrito = B.CodDistrito').fetchall()

df = pd.DataFrame(data=join_tables, columns=colunas + ['distrito_nome'])
df['Distrito'] = df['distrito_nome']
df.drop(columns=['distrito_nome'], inplace=True)

# salvando mudanças na database
df.to_sql('Censo31', con=connection, if_exists='replace', index=False)
print('Nomes de Distritos atualizados na base de dados.')
