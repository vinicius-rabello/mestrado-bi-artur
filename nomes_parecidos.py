import pandas as pd
import sqlite3
import re
import difflib
from tqdm import tqdm


def padronizar_nomes(nome):
    if nome:  # checando se o nome existe
        # usando regex para remover caracteres especiais
        return re.sub(r'[^a-zA-Z]', '', nome)
    else:
        return ''  # caso não exista retorna string vazia


# conectando na base de dados
connection = sqlite3.connect('database/database.db')
cursor = connection.cursor()

# pegando todos os nomes

nomes_recibos = cursor.execute("SELECT DISTINCT Produtor FROM Recibos;").fetchall()
nomes_censo = cursor.execute("SELECT DISTINCT Nome FROM Censo31;").fetchall()

# padronizando os nomes

nomes_recibos = [padronizar_nomes(
    nome[0]).lower() for nome in nomes_recibos]
nomes_censo = [padronizar_nomes(
    nome[0]).lower() for nome in nomes_censo]


def comparar_nomes(nome1, nome2):
    seq = difflib.SequenceMatcher(None, nome1, nome2)
    sim = seq.ratio()
    return sim


possiveis_matches = []
for produtor in tqdm(nomes_recibos):
    for nome in tqdm(nomes_censo):
        # calcular a similaridade entre nomes
        sim = comparar_nomes(produtor, nome)
        if sim >= 0.7:
            possiveis_matches.append([produtor, nome, sim])

df = pd.DataFrame(data = possiveis_matches, columns = ['Nome Recibos', 'Nome Censo', 'Semelhança'])
df.to_excel('possiveis_matches.xlsx', index=False)