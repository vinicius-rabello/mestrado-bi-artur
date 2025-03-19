import pandas as pd

df = pd.read_excel('database/tables/Recibos.xlsx')
df_novo = pd.read_excel('database/tables/recibos-atualizada.xlsx')

colunas = df.columns.tolist()
colunas_novo = df_novo.columns.tolist()

colunas_iguais = [col for col in colunas if col in colunas_novo]

df = df.sort_values(by='id')
df_novo = df_novo.sort_values(by='id')

df = df.reset_index(drop=True)
df_novo = df_novo.reset_index(drop=True)

df[colunas_iguais] = df_novo[colunas_iguais]
df.to_excel('database/tables/Recibos_teste.xlsx')

# comparacao = df == df_novo

# erros = comparacao.apply(lambda x: (x == True).sum())
# erros_df = pd.DataFrame(
#     erros, columns=['número de erros'], index=comparacao.columns.tolist())

# comparacao.to_excel('comparacao.xlsx', index=False)