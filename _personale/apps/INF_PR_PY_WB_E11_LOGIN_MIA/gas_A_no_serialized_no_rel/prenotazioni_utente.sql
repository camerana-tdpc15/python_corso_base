SELECT
    p.id AS prenotazione_id,
    l.id AS lotto_id,
    pr.id AS prodotto_id,
    pd.id AS produttore_id,
    l.data_consegna,
    l.qta_unita_misura,
    l.qta_lotto,
    l.prezzo_unitario,
    l.sospeso,
    pr.nome AS prodotto_nome,
    pd.nome AS produttore_nome,
    pd.descrizione,
    pd.indirizzo,
    pd.telefono,
    pd.email
FROM prenotazioni p
JOIN lotti l ON p.lotto_id = l.id
JOIN prodotti pr ON l.prodotto_id = pr.id
JOIN produttori pd ON pr.produttore_id = pd.id
WHERE p.user_id = ?
ORDER BY l.data_consegna;
