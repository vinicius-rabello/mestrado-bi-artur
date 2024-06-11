import pandas as pd
import sqlite3
import re
import difflib
from tqdm import tqdm


# def padronizar(str):
#     if str:  # checando se o nome existe
#         # usando regex para remover caracteres especiais
#         return re.sub(r'[^a-zA-Z]', '', str.lower())
#     else:
#         return ''  # caso não exista retorna string vazia


# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

# pegando todos os nomes

entradas_recibos = cursor.execute(
    "SELECT DISTINCT Produtor, Município, Freguesia, Distrito, id, Data, IdProdutor FROM Recibos;").fetchall()

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
    matches_df = []
    for entrada_recibo in tqdm(entradas_recibos):
        # checando se já existe algum match com o censo
        if entrada_recibo[6]:
            correspondencia = 1
        else:
            correspondencia = 0

        produtor = entrada_recibo[0]
        municipio_recibo = entrada_recibo[1]
        freguesia_recibo = entrada_recibo[2]
        distrito_recibo = entrada_recibo[3]
        id_recibo = entrada_recibo[4]

        possiveis_matches = []
        try:
            ano_recibo = entrada_recibo[5].split('-')[0].replace('19', '18')
        except:
            ano_recibo = entrada_recibo[5]
        if not produtor:
            continue
        # for entradas_censo in entradas_censos:
        for entrada_censo in tqdm(entradas_censo31):
            nome = entrada_censo[0]
            municipio_censo = entrada_censo[1]
            distrito_censo = entrada_censo[2]
            ano_censo = '18' + str(entrada_censo[3])
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
                    [produtor, nome, municipio_recibo, distrito_recibo, freguesia_recibo, municipio_censo,
                     distrito_censo, ano_recibo, ano_censo, sim, id_recibo, id_censo, 0, correspondencia])

        match_df = pd.DataFrame(data=possiveis_matches, columns=[
            'NomeRecibos', 'NomeCenso', 'MunicipioRecibo', 'DistritoRecibo', 'FreguesiaRecibo', 'MunicipioCenso',
            'DistritoCenso', 'AnoRecibo', 'AnoCenso', 'Semelhanca', 'IdRecibo', 'IdCenso', 'MatchId', 'ExisteCorrespondencia'])
        match_df = match_df.sort_values(
            by=['Semelhanca'], ascending=False)  # ordenando por semelhanca
        match_df['MatchId'] = [k for k in range(
            len(possiveis_matches))]  # gerando os match ids
        matches_df.append(match_df)
    df = pd.concat(matches_df)
    df.to_excel('database/tables/possiveis_matches.xlsx', index=False)


gerar_possiveis_matches()
