import pandas as pd
import sqlite3
import re
import difflib
from tqdm import tqdm


def padronizar(str):
    if str:  # checando se o nome existe
        # usando regex para remover caracteres especiais
        return re.sub(r'[^a-zA-Z]', '', str.lower())
    else:
        return ''  # caso não exista retorna string vazia


# conectando na base de dados
connection = sqlite3.connect('database/database.db')
cursor = connection.cursor()

# pegando todos os nomes

entradas_recibos = cursor.execute(
    "SELECT DISTINCT Produtor, Município, Distrito, id FROM Recibos;").fetchall()

entradas_censo31 = cursor.execute(
    "SELECT DISTINCT Nome, Município, Distrito, Ano, ID FROM Censo31;").fetchall()

# entradas_censo38 = cursor.execute(
#     "SELECT DISTINCT Nome, Município, Distrito, Ano FROM Censo38;").fetchall()

# entradas_censos = [entradas_censo31, entradas_censo38]


def comparar_nomes(nome1, nome2):
    seq = difflib.SequenceMatcher(None, nome1, nome2)
    sim = seq.ratio()
    return sim


def gerar_possiveis_matches():
    possiveis_matches = []
    for entrada_recibo in tqdm(entradas_recibos):
        match_id = 0
        produtor = entrada_recibo[0]
        municipio_recibo = entrada_recibo[1]
        distrito_recibo = entrada_recibo[2]
        id_recibo = entrada_recibo[3]
        if not produtor:
            continue
        # for entradas_censo in entradas_censos:
        for entrada_censo in tqdm(entradas_censo31):
            nome = entrada_censo[0]
            municipio_censo = entrada_censo[1]
            distrito_censo = entrada_censo[2]
            ano = '18' + str(entrada_censo[3])
            id_censo = entrada_censo[4]

            if not nome:
                continue
            # checando se distritos existem e são diferentes
            if distrito_censo and distrito_recibo and distrito_censo != distrito_recibo:
                continue
            # checando se municípios existem e são diferentes
            if municipio_censo and municipio_recibo and municipio_censo != municipio_recibo:
                continue
            # calcular a similaridade entre nomes
            try:
                sim = comparar_nomes(produtor, nome)
            except:
                print(f'Erro comparando nomes:\
                      \n entrada_recibo = {entrada_recibo}\
                      \n entrada_censo = {entrada_censo}\n')
                continue
            if sim >= 0.8:
                possiveis_matches.append(
                    [produtor, nome, municipio_censo, municipio_recibo,
                     distrito_censo, distrito_recibo, match_id, ano, sim, id_recibo, id_censo])
                match_id += 1

    df = pd.DataFrame(data=possiveis_matches, columns=[
        'NomeRecibos', 'NomeCenso', 'MunicipioRecibo', 'MunicipioCenso',
        'DistritoRecibo', 'DistritoCenso', 'MatchId', 'Ano', 'Semelhanca', 'IdRecibo', 'IdCenso'])
    df.to_excel('database/tables/possiveis_matches.xlsx', index=False)


gerar_possiveis_matches()
