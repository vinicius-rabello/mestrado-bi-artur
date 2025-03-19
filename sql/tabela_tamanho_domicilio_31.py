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
        WITH indicador_escravizados AS (
        SELECT
            *,
            CASE WHEN n_escravizados > 0 THEN "Com Escravos" WHEN n_escravizados = 0 THEN "Sem Escravos" ELSE NULL END AS possui_escravos
        FROM Censo31_escravizados
        WHERE Município = '{municipio[0]}' AND Relação = 100
    ), estatisticas AS (
        SELECT 
            possui_escravos,
            AVG(tamanho_plantel) AS media,
            MAX(tamanho_plantel) AS maximo,
            SUM(tamanho_plantel) AS total_pessoas,
            COUNT(*) AS n
        FROM indicador_escravizados
        GROUP BY possui_escravos
    ), final AS (
        SELECT 
            e.possui_escravos AS 'Domicílio com/sem escravos',
            e.media AS 'Média',
            SUM((i.tamanho_plantel - e.media) * (i.tamanho_plantel - e.media)) / (e.n - 1) AS 'Variância',
            e.maximo AS 'Tamanho Máximo do Domicílio',
            e.total_pessoas AS 'Total Pessoas',
            e.n AS 'Total Domicílios'
        FROM indicador_escravizados i
        JOIN estatisticas e ON i.possui_escravos = e.possui_escravos
        GROUP BY i.possui_escravos
    )
    SELECT * FROM final;
    """

    table = cursor.execute(query).fetchall()
    df = pd.DataFrame(data=table, columns = [
        "Domicílio com/sem escravos",
		"Média",
		"Variância",
		"Tamanho Máximo do Domicílio",
		"Total Pessoas",
        "Total Domicílios"
    ])
    df['Variância'] = df["Variância"].apply(lambda x: x**0.5)
    df.rename(columns={"Variância": "Desvio Padrão"}, inplace=True)
    dfs[municipio[0]] = df

with pd.ExcelWriter("novas_tabelas/tabela_tamanho_domicilio_31.xlsx", engine="xlsxwriter") as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)