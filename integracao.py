import pandas as pd

# função para printar entrada do recibo


def printar_recibo(entrada_recibo):
    colunas = ['NomeRecibos', 'MunicipioRecibo',
               'DistritoRecibo', 'Ano', 'IdRecibo']
    for coluna, valor in zip(colunas, entrada_recibo):
        print(f'{coluna}: {valor}')

# função para printar candidatos


def printar_candidato(entrada_candidato):
    colunas = ['NomeCenso', 'MunicipioCenso',
               'DistritoCenso', 'Ano', 'Semelhanca', 'IdCenso']
    for coluna, valor in zip(colunas, entrada_candidato):
        print(f'{coluna}: {valor}')


# pegando as tabelas a serem usadas
possiveis_matches = pd.read_excel('database/tables/possiveis_matches.xlsx')
recibos = pd.read_excel('database/tables/Recibos.xlsx')
recibos_novo = recibos.copy()

# número de possíveis matches
n_entradas = possiveis_matches.shape[0]

i = 0
# iteraremos sobre cada possível match
while i < n_entradas:
    match = possiveis_matches.loc[i]  # pegando match
    entrada_recibo = match[[
        # definindo colunas relacionadas ao recibo
        'NomeRecibos', 'MunicipioRecibo', 'DistritoRecibo', 'Ano', 'IdRecibo']]
    # quantos elementos até próximo MatchId = 0
    # número de candidatos
    n_candidatos = list(possiveis_matches['MatchId'].loc[i+1:]).index(0) + 1

    # display
    print('='*148)
    print(f'\nExistem {n_candidatos} possíveis matches para {
          entrada_recibo['NomeRecibos']}:')

    print('\nRecibo: \n')
    printar_recibo(entrada_recibo)
    print('\nCandidatos:')

    # iterando sobre os candidatos possíveis para entrada de recibo
    candidatos = possiveis_matches.loc[i: i + n_candidatos - 1]

    # display
    for j in range(n_candidatos):
        candidato = candidatos.loc[i + j][[
            'NomeCenso', 'MunicipioCenso', 'DistritoCenso', 'Ano', 'Semelhanca', 'IdCenso']]
        print(f'\nCandidato {j + 1}: \n')
        printar_candidato(candidato)

    # selecionando candidato ideal
    while True:
        print('\nDigite o número do candidato escolhido: (0 para não escolher nenhum)\n')
        escolha = input('')
        print('\n')

        # checando se é int
        try:
            escolha = int(escolha)
        except ValueError:
            print('Valor inserido é inválido!')
            continue
        # se 0 for escolhido continue para próximo nome
        if escolha == 0:
            i += n_candidatos
            break
        else:
            try:
                print(f'O candidato {escolha} foi escolhido!')
                candidato = candidatos.loc[i + escolha - 1]
                printar_candidato(candidato)
                break
            except ValueError:
                print('Valor inserido é inválido!')
                continue
    continue