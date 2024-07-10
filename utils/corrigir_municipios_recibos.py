import pandas as pd

def corrigir_municipios(municipio):
    if municipio == 'São Jose Del Rei (Tiradentes)':
        return 'São José del Rei'
    elif municipio == 'São João del-Rei':
        return 'São João del Rei'
    elif municipio == 'Queluz (Conselheiro Lafaiete)':
        return 'Queluz'
    elif municipio == 'Itapecerica':
        return 'Tamanduá'
    else:
        return municipio

df = pd.read_excel('database/tables/Recibos.xlsx')
df['Município'] = df['Município'].apply(lambda x: corrigir_municipios(x))
df.to_excel('database/tables/Recibos.xlsx', index=False)