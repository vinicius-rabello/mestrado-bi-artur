import pandas as pd
import sqlite3
import difflib
from tqdm import tqdm

def comparar_nomes(nome1, nome2):
    seq = difflib.SequenceMatcher(None, nome1, nome2)
    sim = seq.ratio()
    return sim


def gerar_possiveis_matches(path, arrecadadores=False, municipio=None):
    # conectando na base de dados
    connection = sqlite3.connect('database/test.db')
    cursor = connection.cursor()

    # pegando todos os nomes
    if arrecadadores:
        entradas_recibos = cursor.execute(
            "SELECT DISTINCT Arrecadador, Município, Freguesia, Distrito, id, Data, IdProdutor, Localização FROM Recibos \
             WHERE Arrecadador NOT NULL;").fetchall()
    else:
        if municipio:
            entradas_recibos = cursor.execute(
                f"SELECT DISTINCT Produtor, Município, Freguesia, Distrito, id, Data, IdProdutor, Localização FROM Recibos \
                  WHERE Município = '{municipio}';").fetchall()
        else:
            entradas_recibos = cursor.execute(
                f"SELECT DISTINCT Produtor, Município, Freguesia, Distrito, id, Data, IdProdutor, Localização FROM Recibos;").fetchall()

    entradas_censo31 = cursor.execute(
        "SELECT DISTINCT Nome, Município, Distrito, Ano, ID FROM Censo31;").fetchall()

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
        localizacao_recibo = entrada_recibo[7]

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
            # checando se municípios existem e são diferentes
            if municipio_censo and municipio_recibo and municipio_censo != municipio_recibo:
                # checando se os municipios diferentes são Diamantina e Serro
                if set([municipio_censo, municipio_recibo]) == {'Serro', 'Diamantina'}:
                    pass
                # checando se os municipios diferentes são Vila do Príncipe e Serro
                elif set([municipio_censo, municipio_recibo]) == {'Serro', 'Vila do Príncipe'}:
                    pass
                # checando se os municipios diferentes são Curvelo e Sabará
                elif set([municipio_censo, municipio_recibo]) == {'Curvelo', 'Sabará'}:
                    pass
                # checando se os municipios diferentes são Baependi e Campanha
                elif set([municipio_censo, municipio_recibo]) == {'Baependi', 'Campanha'}:
                    pass
                # checando se os municipios diferentes são Mariana e Caeté
                elif set([municipio_censo, municipio_recibo]) == {'Mariana', 'Caeté'}:
                    pass
                else:
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
                    [produtor, nome, municipio_recibo, distrito_recibo, freguesia_recibo, localizacao_recibo,
                     municipio_censo, distrito_censo, ano_recibo, ano_censo, sim, id_recibo, id_censo, 0, correspondencia, 0])

        match_df = pd.DataFrame(data=possiveis_matches, columns=[
            'NomeRecibos', 'NomeCenso', 'MunicipioRecibo', 'DistritoRecibo', 'FreguesiaRecibo', 'LocalizacaoRecibo', 'MunicipioCenso',
            'DistritoCenso', 'AnoRecibo', 'AnoCenso', 'Semelhanca', 'IdRecibo', 'IdCenso', 'MatchId', 'ExisteCorrespondencia', 'Descartado'])
        match_df = match_df.sort_values(
            by=['Semelhanca'], ascending=False)  # ordenando por semelhanca
        match_df['MatchId'] = [k for k in range(
            len(possiveis_matches))]  # gerando os match ids
        matches_df.append(match_df)
    df = pd.concat(matches_df)
    df.to_excel(path, index=False)


gerar_possiveis_matches('database/tables/possiveis_matches_09-07.xlsx')
