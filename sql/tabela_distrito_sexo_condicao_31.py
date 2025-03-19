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
        WITH censo_municipio AS (
            SELECT * FROM Censo31_escravizados
            WHERE Município = '{municipio[0]}' AND Distrito IS NOT NULL
        ), com_fogo_id AS (
            SELECT 
                *,
                MIN(Id) OVER (
                    PARTITION BY Município, Distrito, Quart, Fogo
                    ORDER BY Id
                ) AS fogo_id
            FROM censo_municipio
            ORDER BY id
        ), final AS (
            SELECT
                Distrito,
                COUNT(DISTINCT fogo_id) AS 'Número de Domicílios',
                SUM(CASE WHEN Sexo = 1 THEN 1 ELSE 0 END) AS 'Homens',
                SUM(CASE WHEN Sexo = 2 THEN 1 ELSE 0 END) AS 'Mulheres',
                COUNT(*) AS 'Total',
                SUM(CASE WHEN Condição = 'livre' THEN 1 ELSE 0 END) AS 'Total Livres',
                SUM(CASE WHEN Condição = 'escravo' THEN 1 ELSE 0 END) AS 'Total Escravos'
            FROM com_fogo_id
            GROUP BY Distrito
        )
        SELECT * FROM final
    """

    table = cursor.execute(query).fetchall()
    df = pd.DataFrame(data=table, columns = [
        "Distrito",
        "Número de Domicílios",
        "Homens",
        "Mulheres",
        "Total",
        "Total Livres",
        "Total Escravos"
    ])
    dfs[municipio[0]] = df

with pd.ExcelWriter("novas_tabelas/tabela_distrito_sexo_condicao_31.xlsx", engine="xlsxwriter") as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)