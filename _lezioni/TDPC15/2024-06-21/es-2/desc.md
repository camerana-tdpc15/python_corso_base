Sia dato il seguente schema relazionale (le chiavi primarie sono sottolineate, gli attributi
opzionali sono indicati con “*”)

STUDENTE (MatrS, NomeS, Città)
CORSO (CodC, NomeC, MatrD)
DOCENTE (MatrD, NomeD)
ESAME (CodC, MatrS, Data, Voto)

a) Per ogni studente, visualizzare la matricola e il voto massimo, minimo e medio conseguito negli
esami
SELECT MatrS, MAX (Voto), MIN(Voto), AVG (Voto)
FROM ESAME E
GROUP BY MatrS

b) Per ogni studente, visualizzare la matricola, il nome e il voto massimo, minimo e medio conseguito
negli esami
SELECT S.MatrS, NomeS, MAX (Voto), MIN(Voto), AVG (Voto)
FROM ESAME E, STUDENTE S
WHERE S.MatrS = E.MatrS
GROUP BY S.MatrS, NomeS

c) Per ogni studente che ha una media voti superiore al 28, visualizzare la matricola, il nome e il voto
massimo, minimo e medio conseguito negli esami
SELECT S.MatrS, NomeS, MAX (Voto), MIN(Voto), AVG (Voto)
FROM ESAME E, STUDENTE S
WHERE S.MatrS = E.MatrS
GROUP BY S.MatrS, NomeS
HAVING AVG(Voto) > 28

d) Per ogni studente della città di Torino che ha una media voti superiore al 28 e ha sostenuto esami
in almeno 10 date diverse, visualizzare la matricola, il nome e il voto massimo, minimo e medio
conseguito negli esami
SELECT S.MatrS, NomeS, MAX (Voto), MIN(Voto), AVG (Voto)
FROM ESAME E, STUDENTE S
WHERE S.MatrS = E.MatrS and Città = ‘Torino’
GROUP BY S.MatrS, NomeS
HAVING AVG(Voto) > 28 AND COUNT(DISTINCT Data)>10