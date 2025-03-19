import pandas as pd
import numpy as np

df = pd.read_excel('./database/tables/Censo38.xlsx')
cod = pd.read_excel('./database/tables/municipios38.xlsx', header=None)
cod.columns = ['Municipio', 'Distrito', 'Codigo']

def set_casing(str_):
    words = str_.split(' ')
    new_str = ''
    for word in words:
        word = word.lower()
        word = word[0].upper() + word[1:]
        new_str += word + ' '
    return new_str.rstrip()

def set_codigos(row):
    cod_mun, cod_dist = row[['Município', 'Distrito']]
    cod_mun, cod_dist = str(cod_mun), str(cod_dist)
    if len(cod_dist) < 2:
        cod_dist = '0' + cod_dist

    codigo = str(cod_mun) + str(cod_dist)
    row['Município'] = float(codigo)
    row['Distrito'] = float(codigo)
    return row

cod['Municipio'] = cod['Municipio'].apply(lambda x: set_casing(str(x)))
cod.dropna(inplace=True)
cod.loc[cod['Municipio'] == 'Ninas Novas', 'Municipio'] = 'Minas Novas'
cod.loc[cod['Municipio'] == 'Ouro Ppreto', 'Municipio'] = 'Ouro Preto'
cod.to_excel('./database/tables/municipios38_.xlsx', index=False)

def get_municipio(codigo):
    try:
        return cod.loc[cod['Codigo'] == codigo]['Municipio'].tolist()[0]
    except:
        return None

def get_distrito(codigo):
    try:
        return cod.loc[cod['Codigo'] == codigo]['Distrito'].tolist()[0]
    except:
        return None

df = df.apply(lambda x: set_codigos(x), axis=1)
df['Município'] = df['Município'].apply(lambda x: get_municipio(x))
df['Distrito'] = df['Distrito'].apply(lambda x: get_distrito(x))
df.to_excel('./database/tables/censo38_corrigido.xlsx', index=False)