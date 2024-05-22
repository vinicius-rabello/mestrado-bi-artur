import pandas as pd
from sqlalchemy import create_engine
import sqlite3


def convert_to_db(path, table_name):
    extension = path.split('.')[-1]
    try:
        if extension == 'xlsx': # check if its a excel file
            df = pd.read_excel(path)
        #elif extension == 'mdb': # check if its a access file
        #    data = 
    except:
        print(f'{path} is of invalid type.')
        return None
    
    engine = create_engine('sqlite:///C:/Users/vinic/Documents/mestrado-bi/database.db', echo=False) # creating a sql engine
    df.to_sql(table_name, con = engine, if_exists = 'replace', index = False) # loading data in .db
    

convert_to_db('tabela.xlsx', 'tabela')