import sqlite3

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

drop_table_query = "DROP TABLE IF EXISTS Censo31_escravizados"
cursor.execute(drop_table_query)

create_table_query = "CREATE TABLE Censo31_escravizados AS SELECT *, NULL AS n_escravizados, NULL AS tamanho_plantel FROM Censo31 WHERE 1 = 1"
cursor.execute(create_table_query)

escravizados_query = """
WITH donos AS (
    SELECT *, 
           CASE WHEN Relação = 100
                THEN Id 
           END AS dono_id
    FROM Censo31
), marcados AS (
    SELECT *, 
           MAX(dono_id) OVER (
                PARTITION BY Município, Distrito, Quart, Fogo
                ORDER BY Id
           ) AS dono_atual
    FROM donos
), contagem AS (
    SELECT
		dono_atual,
		SUM(CASE WHEN Condição = 'escravo' THEN 1 ELSE 0 END) AS n_escravizados,
		COUNT(*) AS tamanho_plantel
    FROM marcados
    WHERE dono_atual IS NOT NULL
    GROUP BY dono_atual
)
UPDATE Censo31_escravizados
SET
    n_escravizados = (
        SELECT n_escravizados FROM contagem 
        WHERE contagem.dono_atual = Censo31_escravizados.Id
    ),
    tamanho_plantel = (
        SELECT tamanho_plantel FROM contagem 
        WHERE contagem.dono_atual = Censo31_escravizados.Id
    )
WHERE Id IN (SELECT dono_atual FROM contagem);
"""

cursor.execute(escravizados_query)
connection.commit()
