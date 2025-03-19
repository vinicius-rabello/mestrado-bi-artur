import pandas as pd
import sqlite3
from tqdm import tqdm

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

query_distinct_municipios = """
SELECT DISTINCT Município FROM Censo31
"""

municipios = cursor.execute(query_distinct_municipios).fetchall()

dfs = {}
for municipio in tqdm(municipios):
    query = f"""
    WITH indicadores AS (
        SELECT
            CASE
                WHEN Raça = 'branco' THEN 1
                WHEN Raça = 'crioulo' THEN 2
                WHEN Raça = 'africano' THEN 3
                WHEN Raça = 'preto' THEN 3
                WHEN Raça = 'pardo' THEN 4
                ELSE 999 END AS race_id,
            Município,
            CASE
                WHEN Raça = 'branco' THEN 'Branco'
                WHEN Raça = 'crioulo' THEN 'Crioulo'
                WHEN Raça = 'africano' THEN 'Africano/Preto'
                WHEN Raça = 'preto' THEN 'Africano/Preto'
                WHEN Raça = 'pardo' THEN 'Pardo' 
                ELSE '' END AS Raça,
            CASE WHEN Sexo = 1 THEN 'Homem' WHEN Sexo = 2 THEN 'Mulher' ELSE '' END AS Sexo,
            CASE WHEN Condição = 'livre' THEN 1 ELSE 0 END AS indicador_livre,
            CASE WHEN Condição = 'escravo' THEN 1 ELSE 0 END AS indicador_escravo,
            CASE WHEN Condição = 'forro' THEN 1 ELSE 0 END AS indicador_forro
        FROM Censo31
    )
    SELECT Raça, Sexo, SUM(indicador_livre) AS 'Livres', SUM(indicador_escravo) AS 'Escravos',
            SUM(indicador_forro) AS 'Alforriados', COUNT(*) AS 'Total' FROM indicadores
    WHERE Município = '{municipio[0]}' AND Raça IN ('Branco', 'Africano/Preto', 'Pardo', 'Crioulo')
    GROUP BY race_id, Raça, Sexo
    ORDER BY race_id
    """

    table = cursor.execute(query).fetchall()
    df = pd.DataFrame(data=table, columns = ['Raça', 'Sexo', 'Livres', 'Escravos', 'Alforriados', 'Total'])
    dfs[municipio[0]] = df

with pd.ExcelWriter("novas_tabelas/tabela_raca_sexo_condicao_31.xlsx", engine="xlsxwriter") as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)