import pandas as pd
import time

# função para printar entrada do recibo

colunas_recibo = ['NomeRecibos', 'MunicipioRecibo',
                  'DistritoRecibo', 'Ano', 'IdRecibo']
colunas_censo = ['NomeCenso', 'MunicipioCenso',
                 'DistritoCenso', 'Ano', 'Semelhanca', 'IdCenso']

# horario que começou a ser feita as mudanças para ser o nome do arquivo de log
log_date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def printar_recibo(entrada_recibo):
    for coluna, valor in zip(colunas_recibo, entrada_recibo):
        print(f'{coluna}: {valor}')

# função para printar candidatos


def printar_candidato(entrada_candidato):
    for coluna, valor in zip(colunas_censo, entrada_candidato):
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
    entrada_recibo = match[colunas_recibo]
    # quantos elementos até próximo MatchId = 0
    # número de candidatos
    n_candidatos = list(possiveis_matches['MatchId'].loc[i+1:]).index(0) + 1
    candidatos = possiveis_matches.loc[i: i + n_candidatos - 1]

    print('='*148)
    print(f'\nFaltam {n_entradas - i} de {n_entradas} entradas na planilha.\n')

    def mostrar_candidatos():
        # display
        print('='*148)
        print(f'\nExistem {n_candidatos} possíveis matches para {
            entrada_recibo['NomeRecibos']}:')

        print('\nRecibo: \n')
        printar_recibo(entrada_recibo)
        print('\nCandidatos:')

        # iterando sobre os candidatos possíveis para entrada de recibo
        # display
        for j in range(n_candidatos):
            candidato = candidatos.loc[i + j][colunas_censo]
            print(f'\nCandidato {j + 1}: \n')
            printar_candidato(candidato)

    mostrar_candidatos()
    # selecionando candidato ideal
    escolhido = False
    while not escolhido:
        print('='*148)
        print('\nDigite o número do candidato escolhido: (0 para não escolher nenhum)\n')
        escolha = input('')
        print('')

        # checando se é int
        try:
            escolha = int(escolha)
        except ValueError:
            print('Valor inserido é inválido! Escolha novamente.')
            continue
        # se 0 for escolhido continue para próximo nome
        if escolha == 0:
            i += n_candidatos
            escolhido = True
        else:
            # checar se número escolhido é válido
            try:
                # confirmar escolha
                candidato = candidatos.loc[i + escolha - 1][colunas_censo]

                print('='*148)
                print('Confirma essa mudança?')
                print('='*148 + '\n\nRecibo: \n')
                printar_recibo(entrada_recibo)
                print('='*148 + '\n\nCenso: \n')
                printar_candidato(candidato)
                print('='*148)
                confirmacao = input(
                    "\nDigite 'S' para sim ou 'N' para não: ").lower()
                print('')
                if confirmacao == 's':
                    print('\n' + '='*148)
                    print('\nEscolha confirmada!\n')

                    # logar mudança

                    with open(f'logs/{log_date}.txt', 'a') as f:
                        f.write(f"{entrada_recibo['NomeRecibos']} | {entrada_recibo['IdRecibo']} ---> IdCenso: {candidato['IdCenso']} (Candidato {escolha})\n")

                    i += n_candidatos
                    escolhido = True
                else:
                    mostrar_candidatos()
                    continue
            except:
                print('Valor inserido é inválido! Escolha novamente.')
                continue
    continue
