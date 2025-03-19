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
    WITH censo_municipio AS (
        SELECT * FROM Censo38_escravizados
        WHERE Município = '{municipio[0]}'
    ), total_nums AS (
        SELECT
            COUNT(DISTINCT("ID Fogo")) AS num_domicilios,
            SUM(n_escravizados) AS total_escravizados
        FROM censo_municipio
        WHERE n_escravizados > 0
    ), with_qual_n_esc AS (
        SELECT
            *,
            CASE WHEN n_escravizados >= 22 THEN '22+' ELSE CAST(n_escravizados AS TEXT) END AS n_escravizados_str,
            CASE WHEN n_escravizados >= 22 THEN 22 ELSE n_escravizados END AS n_escravizados_trunc
        FROM censo_municipio
        WHERE n_escravizados > 0
    ), com_porcentagens AS (
        SELECT
            A.n_escravizados_trunc,
            A.n_escravizados_str AS 'Número de Escravos Possuídos',
            COUNT(*) AS 'Número de Domicílios',
            SUM(A.n_escravizados) AS 'Total de Escravos Possuídos',
            ROUND(100*CAST(count(*) AS REAL)/B.num_domicilios, 1) AS 'Porcentagem de Domicílios',
            ROUND(100*CAST(SUM(A.n_escravizados) AS REAL)/B.total_escravizados, 1) AS 'Porcentagem de Escravos'
        FROM with_qual_n_esc A
        JOIN total_nums B ON 1=1
        GROUP BY n_escravizados_str
        ORDER BY n_escravizados
    ), final AS (
        SELECT
            "Número de Escravos Possuídos",
            "Número de Domicílios",
            "Total de Escravos Possuídos",
            "Porcentagem de Domicílios",
            "Porcentagem de Escravos",
            MIN(ROUND(SUM("Porcentagem de Domicílios") OVER (
                ORDER BY n_escravizados_trunc ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 1), 100.0) AS 'Porcentagem Acumulada de Domicílios',
            MIN(ROUND(SUM("Porcentagem de Escravos") OVER (
                ORDER BY n_escravizados_trunc ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 1), 100.0) AS 'Porcentagem Acumulada de Escravos'
        FROM com_porcentagens
    )
    SELECT * FROM final
    """

    table = cursor.execute(query).fetchall()
    df = pd.DataFrame(data=table, columns = [
        "Número de Escravos Possuídos",
		"Número de Domicílios",
		"Total de Escravos Possuídos",
		"Porcentagem de Domicílios",
		"Porcentagem de Escravos",
        "Porcentagem Acumulada de Domicílios",
        "Porcentagem Acumulada de Escravos"
    ])
    dfs[municipio[0]] = df

with pd.ExcelWriter("novas_tabelas/tabela_porcentagens_domicilios_escravos_38.xlsx", engine="xlsxwriter") as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)