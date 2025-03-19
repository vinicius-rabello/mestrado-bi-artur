import pandas as pd
import sqlite3
import time

# configurar pandas para printar todas as colunas
pd.set_option('display.max_columns', None)

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

# função para printar entrada do recibo

colunas_recibo = ['NomeRecibos', 'MunicipioRecibo',
                  'FreguesiaRecibo', 'DistritoRecibo', 'LocalizacaoRecibo', 'AnoRecibo', 'IdRecibo']
colunas_censo = ['NomeCenso', 'MunicipioCenso', 'DistritoCenso',
                 'AnoCenso', 'Semelhanca', 'IdCenso']
colunas_censo_total = ['Dia', 'Mês', 'Ano', 'Pasta', 'Doc', 'Município', 'Distrito', 'Quart',
                       'CodTipo', 'Id', 'Fogo', 'Número', 'Relação', 'Sexo', 'Raça',
                       'Condição', 'Idade', 'Est civil', 'Alfab', 'Nac', 'Ocup', 'Nome', 'id']

# horario que começou a ser feita as mudanças para ser o nome do arquivo de log
log_date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def printar_recibo(entrada_recibo):
    for coluna, valor in zip(colunas_recibo, entrada_recibo):
        print(f'{coluna}: {valor}')

# função para printar candidatos


def printar_candidato(entrada_candidato):
    for coluna, valor in zip(colunas_censo, entrada_candidato):
        print(f'{coluna}: {valor}')

# query para pegar todos os moradores de uma casa


def query_endereco(id):
    endereco = cursor.execute(
        f"SELECT Município, Distrito, Quart, Fogo FROM Censo38 WHERE Id = {id}").fetchall()
    municipio = endereco[0][0]
    distrito = endereco[0][1]
    quart = endereco[0][2]
    fogo = endereco[0][3]
    endereco = cursor.execute(f"SELECT * FROM Censo38 \
                     WHERE Município = '{municipio}' AND Distrito = '{distrito}' \
                     AND Quart = '{quart}' AND Fogo = '{fogo}'").fetchall()
    return endereco


def printar_endereco(endereco):
    moradores = []
    for morador in endereco:
        moradores.append(morador)
    print(pd.DataFrame(data=moradores, columns=colunas_censo_total))
    print('\n')


# pegando as tabelas a serem usadas
possiveis_matches_path = 'database/tables/possiveis_matches_arrecadador_38.xlsx'
possiveis_matches = pd.read_excel(possiveis_matches_path)
recibos = pd.read_excel('database/tables/Recibos.xlsx')
recibos_novo = recibos.copy()

# número de possíveis matches
n_entradas = possiveis_matches.shape[0]

i = 3300 - 1498 # 3300 - numero que parou

# perguntar se quer pular correspondencias


def pular_matches():
    print('='*148)
    escolha = input(
        "\nVocê deseja pular as sugestões para matches com correspondências já existentes? Digite 'S' para sim ou 'N' para não: ").lower()
    if escolha == 's':
        return True
    else:
        return False


pular_matches = pular_matches()

# iteraremos sobre cada possível match
while i < n_entradas:
    match = possiveis_matches.loc[i]  # pegando match
    entrada_recibo = match[colunas_recibo]
    # quantos elementos até próximo MatchId = 0
    # número de candidatos
    n_candidatos = list(possiveis_matches['MatchId'].loc[i+1:]).index(0) + 1

    # pular matches já feitos
    if pular_matches:
        if match['ExisteCorrespondencia']:  # se já existe correspondencia, pule
            i += n_candidatos
            continue

    if match['Descartado']:  # se match ja foi descartado anteriormente, pule
        i += n_candidatos
        continue

    if entrada_recibo['NomeRecibos'] == 'Camillo Antonio de Carvalho':
        i += n_candidatos
        continue

    if entrada_recibo['NomeRecibos'] == 'Joaquim Jose dos Santos':
        i += n_candidatos
        continue

    if entrada_recibo['NomeRecibos'] == 'João Jose da Silva':
        i += n_candidatos
        continue

    if entrada_recibo['NomeRecibos'] == 'Valerianno Antonio Mascarenhas':
        i += n_candidatos
        continue

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
        print('\nDigite o número do candidato escolhido: (0 para não escolher nenhum e 999 para descartar este arrecadador.)\n')
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
            i += n_candidatos  # proximo match
            escolhido = True
        elif escolha == 999:
            print('='*148)
            print('\nTem certeza que quer descartar esse arrecadador?\n')
            print('='*148)
            confirmacao = input(
                "\nDigite 'S' para sim ou 'N' para não: ").lower()
            print('')
            if confirmacao == 's':
                # descarta esse match para proximos usos desse script
                possiveis_matches.loc[i, 'Descartado'] = 1
                possiveis_matches.to_excel(
                    possiveis_matches_path, index=False)  # atualizar na planilha
                
                # logar descarte
                with open(f'logs/{log_date}.txt', 'a') as f:
                        f.write(f"{entrada_recibo['NomeRecibos']} | {
                                entrada_recibo['IdRecibo']} DESCARTADO\n")

                i += n_candidatos  # proximo match
                escolhido = True
            else:
                mostrar_candidatos()
                continue
        else:
            # checar se número escolhido é válido
            try:
                # confirmar escolha
                try:
                    candidato = candidatos.loc[i + escolha - 1][colunas_censo]
                    endereco = query_endereco(candidato['IdCenso'])
                except:
                    pass
                printar_endereco(endereco)
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

                    # alterar na base de dados

                    connection.execute("BEGIN")
                    cursor.execute(f"UPDATE Recibos SET IdArrecadador38 = {candidato['IdCenso']} WHERE Arrecadador = '{
                                   entrada_recibo["NomeRecibos"]}' AND id = '{entrada_recibo["IdRecibo"]}'")
                    connection.commit()

                    print('Alterações feitas!')

                    # logar mudança

                    with open(f'logs/{log_date}.txt', 'a') as f:
                        f.write(f"{entrada_recibo['NomeRecibos']} | {
                                entrada_recibo['IdRecibo']} ---> IdCenso: {candidato['IdCenso']} (Candidato {escolha})\n")

                    i += n_candidatos
                    escolhido = True
                else:
                    mostrar_candidatos()
                    continue
            except Exception as err:
                print('Valor inserido é inválido! Escolha novamente.')
                print(err)
                continue
    continue

print('Você terminou.\n')
print('='*148)
