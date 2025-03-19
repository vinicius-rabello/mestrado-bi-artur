import pandas as pd
import sqlite3
from tqdm import tqdm

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

query_distinct_municipios = """
SELECT DISTINCT Município FROM Censo38
"""

municipios = cursor.execute(query_distinct_municipios).fetchall()

dfs = {}
for municipio in tqdm(municipios):
    query = f"""
        with with_preto_africano AS (
        SELECT
            CASE
                WHEN Raça = 1 THEN 1
                WHEN Raça = 3 THEN 2
                WHEN Raça = 2 THEN 3
                WHEN Raça = 4 THEN 4
            END AS raca_id,
            Raça,
            Sexo,
            Condição 
        FROM Censo38
        WHERE Município = '{municipio[0]}'
    ), agg AS (
        SELECT
            raca_id,
            Raça,
            Sexo,
            SUM(CASE WHEN Condição = 1 THEN 1 ELSE 0 END) AS Livres,
            SUM(CASE WHEN Condição = 2 THEN 1 ELSE 0 END) AS Escravos,
            COUNT(*) AS Total
        FROM with_preto_africano
        WHERE Raça IN (1, 2, 3, 4)
        GROUP BY raca_id, Raça, Sexo
    ), agg_homem AS (
        SELECT * FROM agg
        WHERE Sexo = 1
    ), agg_mulher AS (
        SELECT * FROM agg
        WHERE Sexo = 2
    ), agg_total AS (
        SELECT
            'Total' AS Raça,
            100*CAST(SUM(CASE WHEN Condição = 1 AND Sexo = 1 THEN 1 ELSE 0 END) AS REAL)
            /SUM(CASE WHEN Condição = 1 AND Sexo = 2 THEN 1 ELSE 0 END) AS Livres,
            100*CAST(SUM(CASE WHEN Condição = 2 AND Sexo = 1 THEN 1 ELSE 0 END) AS REAL)
            /SUM(CASE WHEN Condição = 2 AND Sexo = 2 THEN 1 ELSE 0 END) AS Escravos,
            100*CAST(SUM(CASE WHEN Sexo = 1 THEN 1 ELSE 0 END) AS REAL)
            /SUM(CASE WHEN Sexo = 2 THEN 1 ELSE 0 END) AS Total
        FROM with_preto_africano
    )
    , agg_final AS (
        SELECT 
            A.Raça,
            100*CAST(A.Livres AS REAL)/B.Livres AS Livres,
            100*CAST(A.Escravos AS REAL)/B.Escravos AS Escravos,
            100*CAST(A.Total AS REAL)/B.Total AS Total
        FROM agg_homem A
        LEFT JOIN agg_mulher B
        ON A.Raça = B.Raça
        ORDER BY A.raca_id
    ), final AS (
        SELECT
            CASE
                WHEN Raça = 1 THEN 'Brancos'
                WHEN Raça = 3 THEN 'Crioulos'
                WHEN Raça = 2 THEN 'Africanos/Pretos'
                WHEN Raça = 4 THEN 'Pardos'
                ELSE Raça
            END AS Raça,
            Livres,
            Escravos,
            Total
        FROM agg_final
        UNION ALL
        SELECT * FROM agg_total
    )
    SELECT * FROM final
    """

    table = cursor.execute(query).fetchall()
    df = pd.DataFrame(data=table, columns = [
        "Raça",
        "Livres",
        "Escravos",
        "Total"
    ])
    dfs[municipio[0]] = df

with pd.ExcelWriter("novas_tabelas/tabela_razao_sexo_38.xlsx", engine="xlsxwriter") as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)