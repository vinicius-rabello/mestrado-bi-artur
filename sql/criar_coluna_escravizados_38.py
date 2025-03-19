import sqlite3

# conectando na base de dados
connection = sqlite3.connect('database/test.db')
cursor = connection.cursor()

drop_table_query = "DROP TABLE IF EXISTS Censo38_escravizados"
cursor.execute(drop_table_query)

create_table_query = "CREATE TABLE Censo38_escravizados AS SELECT *, NULL AS n_escravizados, NULL as tamanho_plantel FROM Censo38 WHERE 1 = 1"
cursor.execute(create_table_query)

escraizados_query = """
WITH donos AS (
    SELECT *, 
           CASE WHEN Relação = 1
                THEN id 
           END AS dono_id
    FROM Censo38
), marcados AS (
    SELECT *, 
           MAX(dono_id) OVER (
                PARTITION BY "ID Fogo"
                ORDER BY id
           ) AS dono_atual
    FROM donos
), contagem AS (
    SELECT
		dono_atual,
		SUM(CASE WHEN Condição = 2 THEN 1 ELSE 0 END) AS n_escravizados,
		COUNT(*) AS tamanho_plantel
    FROM marcados
    WHERE dono_atual IS NOT NULL
    GROUP BY dono_atual
)
UPDATE Censo38_escravizados
SET 
    n_escravizados = (
        SELECT n_escravizados FROM contagem 
        WHERE contagem.dono_atual = Censo38_escravizados.id
    ),
    tamanho_plantel = (
        SELECT tamanho_plantel FROM contagem 
        WHERE contagem.dono_atual = Censo38_escravizados.id
    )
WHERE Id IN (SELECT dono_atual FROM contagem);
"""

cursor.execute(escraizados_query)
connection.commit()
