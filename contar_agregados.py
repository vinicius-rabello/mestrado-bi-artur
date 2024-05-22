import pandas as pd

df = pd.read_excel('Série Recibos.xlsx') # ler a planilha
df['Agregados'] = 0 # criar coluna de agregados com 0 em todas as fileiras

def contar_agregados(row):
    obs = str(row['Observações'])
    n_agregados = 0
    if 'Agregado:' in obs or 'Agregados:' in obs:
        agregados = obs.split('Testemunha:')[0] # ignorar o que vem a partir de Testemunha
        agregados = agregados.split(':')[-1] # extrair o que vem após os dois pontos
        agregados = agregados.replace(' e ', ', ') # organizar os delimitadores
        agregados = agregados.split("//")[0] # remover comentários
        agregados = agregados.split("/")[0]
        agregados = agregados.replace('Joaquim Teixeira Antonio Gonçalves Luis Antonio Joaquim das Almas', # lidar com caso especial
                                      'Joaquim Teixeira Antonio Gonçalves, Luis Antonio Joaquim das Almas')

        n_agregados = len(agregados.split(',')) # contar o número de agregados
    return n_agregados

df['Agregados'] = df.apply(lambda x: contar_agregados(x), axis = 1)
df.to_excel('tabela.xlsx', index = False)