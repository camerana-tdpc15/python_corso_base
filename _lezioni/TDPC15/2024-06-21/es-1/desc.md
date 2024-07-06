Sia dato il seguente schema relazionale (le chiavi primarie sono sottolineate, gli attributi
opzionali sono indicati con “*”)

ORCHESTRA (CodO, NomeO, NomeDirettore, NumElementi)
SALA (CodS, NomeS, Città, Capienza)
CONCERTI (CodC, Data, CodO, CodS, PrezzoBiglietto)

a) Trovare il codice e il nome delle orchestre con più di 30 elementi che hanno tenuto concerti sia a
Torino, sia a Milano e non hanno mai tenuto concerti a Bologna.


Soluzione con operatori IN e NOT IN

SELECT O.CodO, NomeO
FROM ORCHESTRA O
WHERE NumElementi > 30
AND O.CodO IN ( SELECT CodO
 FROM SALA S, CONCERTI C
 WHERE Città = ‘Torino’ AND S.CodS=C.CodS)
AND O.CodO IN ( SELECT CodO
 FROM SALA S, CONCERTO C
 WHERE Città =’Milano’ AND S.CodS=C.CodS)
AND O.CodO NOT IN (SELECT CodO
 FROM SALA S, CONCERTO C
 WHERE Città = ‘Bologna’ AND S.CodS=C.CodS)

Soluzione con operatori EXISTS e NOT EXISTS

SELECT O.CodO, NomeO
FROM ORCHESTRA O
WHERE NumElementi > 30
AND EXISTS (SELECT *
FROM SALA SA, CONCERTI CA
WHERE Città = ‘Torino’ AND SA.CodS=CA.CodS
 AND CA.CodO = O.CodC) CONDIZIONE DI CORRELAZIONE
AND EXISTS (SELECT *
FROM SALA SB, CONCERTO CB
 WHERE Città =’Milano’ AND SB.CodS=CB.CodS
 AND CB.CodO = O.CodC) CONDIZIONE DI CORRELAZIONE
AND NOT EXISTS (SELECT *
 FROM SALA SC, CONCERTO CC
 WHERE Città = ‘Bologna’ AND SC.CodS=CC.CodS
 AND CC.CodO = O.CodC) CONDIZIONE DI CORRELAZIONE