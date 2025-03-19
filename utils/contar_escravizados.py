import pandas as pd
import sqlite3
from tqdm import tqdm

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

columns = ['ID', 'Dia', 'Mês', 'Ano', 'Município', 'Distrito', 'Quart', 'Fogo', 'Folha', 'Pasta',
           'Doc', 'Número', 'Relação', 'Sexo', 'Raça', 'Condição', 'Idade', 'Est civil', 'Ocup', 'Nac', 'Nome']\


def query_endereco(id):
    endereco = cursor.execute(
        f"SELECT Município, Distrito, Quart, Fogo FROM Censo31 WHERE Id = {id}").fetchall()
    municipio = endereco[0][0]
    distrito = endereco[0][1]
    quart = endereco[0][2]
    fogo = endereco[0][3]
    endereco = cursor.execute(f"SELECT * FROM Censo31 \
                     WHERE Município = '{municipio}' AND Distrito = '{distrito}' \
                     AND Quart = '{quart}' AND Fogo = '{fogo}'").fetchall()

    df = pd.DataFrame(data=endereco, columns=columns)
    return df

def get_numero(id):
    numero = df[df['ID']==id]['Número'].tolist()[0]
    return numero
    # numero = cursor.execute(
    #     f"SELECT Número FROM Censo31 WHERE Id = {id}").fetchall()
    # return numero[0][0]

def get_subalternos(id):
    # checar se é chefe do fogo
    if get_numero(id) == 1:
        # pegar todos os moradores até o próximo chefe
        endereco = query_endereco(id)
        endereco = endereco[endereco['ID']>id]
        prox_chefe = endereco[endereco['Número'] == 1]
        try:
            prox_chefe_idx =  prox_chefe['Número'].index[0]
            subalternos = endereco[endereco['ID'].isin(range(id-1,prox_chefe_idx-1))]#endereco[id-1:prox_chefe_idx - 1]
        except IndexError as e:
            subalternos = endereco[endereco['ID']>=id]
        return subalternos
    else:
        return None


def contar_escravizados(id):
    try:
        df = get_subalternos(id)
        df = df[df['Condição']=="escravo"]
        n_escravizados = df.shape[0]
    except Exception as e:
        return None
    return n_escravizados



df = pd.read_excel('database/tables/Censo31.xlsx')
coluna_escravos = []
for id in tqdm(range(df.shape[0])):
    coluna_escravos.append(contar_escravizados(id))

df['Num_Escravos'] = coluna_escravos
df.to_excel('database/tables/Censo31_esc.xlsx', index=False)