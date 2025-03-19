import sqlite3
import pandas as pd

def get_fogo_from_id(id, censo):
    query = f"""
        WITH temp AS (
            SELECT Município, Distrito, Quart, Fogo 
            FROM Censo{censo}
            WHERE Id = {id}
        )
        SELECT B.Ano, B.Município, B.Distrito, B.Id, B.Idade, B.Ocup, B.Relação, B.Condição, B.Nome
        FROM temp A
        LEFT JOIN Censo{censo} B
        ON A.Município = B.Município
            AND (
                (A.Distrito = B.Distrito) OR 
                (B.Distrito IS NULL)
            )
            AND A.Quart = B.Quart
            AND A.Fogo = B.Fogo
        ORDER BY B.Id
    """
    return query

def display_match(cursor, match, current, total):
    id31, id38 = match
    
    query31 = get_fogo_from_id(id31, 31)
    query38 = get_fogo_from_id(id38, 38)
    
    data31 = cursor.execute(query31).fetchall()
    data38 = cursor.execute(query38).fetchall()
    
    df31 = pd.DataFrame(data=data31, columns=['Ano', 'Município', 'Distrito', 'Id', 'Idade', 'Ocup', 'Relação', 'Condição', 'Nome'])
    df38 = pd.DataFrame(data=data38, columns=['Ano', 'Município', 'Distrito', 'Id', 'Idade', 'Ocup', 'Relação', 'Condição', 'Nome'])
    
    separator = '=' * 80
    print(f"Match {current} de {total}")
    print(separator)
    print(f'Fogo no Censo 31: (id: {id31})')
    print(separator)
    print(df31)
    print(separator)
    print(f'Fogo no Censo 38: (id: {id38})')
    print(separator)
    print(df38)
    print(separator)
    
    while True:
        escolha = input("Digite 1 para continuar: ")
        if escolha == '1':
            return True
        print('Você precisa digitar 1 para continuar.')

def main():
    try:
        connection = sqlite3.connect('database/test.db')
        cursor = connection.cursor()

        query = """
        SELECT DISTINCT IdProdutor31, IdProdutor38 
        FROM Recibos
        WHERE IdProdutor31 IS NOT NULL AND IdProdutor38 IS NOT NULL
        """

        matches = cursor.execute(query).fetchall()
        total_matches = len(matches)

        for i, match in enumerate(matches, 1):
            if i > 43:
                display_match(cursor, match, i, total_matches)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()