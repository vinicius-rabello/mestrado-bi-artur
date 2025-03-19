WITH agg AS (
	SELECT 
		Raça,
		Sexo,
		COUNT(CASE WHEN Condição = 'livre' THEN 1 ELSE 0 END) AS Livres,
		COUNT(CASE WHEN Condição = 'escravo' THEN 1 ELSE 0 END) AS Escravos
	FROM Censo31
	WHERE Raça IN ('africano', 'branco', 'crioulo', 'preto', 'pardo')
	AND Município = 'Campanha'
	GROUP BY Raça, Sexo
),
SELECT * FROM agg