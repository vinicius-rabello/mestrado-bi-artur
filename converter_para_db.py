import pandas as pd
from sqlalchemy import create_engine
import time


def convert_to_db(path, table_name):
    start_time = time.time()
    extension = path.split('.')[-1]
    print(extension)
    try:
        if extension == 'xlsx':  # checando se é um arquivo excel
            print(f'Lendo {path}...')
            df = pd.read_excel(path)
            print(f'Terminou de ler {path}!')
        else:
            print(f'{path} é de um formato inválido.')
            return None
    except:
        print(f'Erro ao ler {path}')
        return None

    # criando uma engine de sql
    engine = create_engine(
        'sqlite:///C:/Users/vinic/Documents/mestrado-bi/database/test.db', echo=False)
    print(f'Carregando {table_name} na base de dados...')
    df.to_sql(table_name, con=engine, if_exists='replace',
              index=False)  # carregando dados na .db
    print(f'{table_name} foi carregado na base da dados.')
    print(f'Levou {time.time() - start_time} segundos!')


convert_to_db('database/tables/Censo31_powerbi.xlsx', 'Censo31')