from datetime import datetime
from models import db, Produttore, Prodotto, Lotto, User, Prenotazione

def init_db():

    db.create_all()

    if not User.query.first():

        # Inserisci dati iniziali nelle tabelle
        produttori = [
            Produttore(nome='Cascina della Civetta', descrizione='Produttore di olio e frutta secca', indirizzo='Via Cavour 12, Ugento (LE)', telefono='0172 123456', email='civetta@civetta.com'),
            Produttore(nome='Universo Bio', descrizione='Prodotti biologici', indirizzo='Via Garibaldi 2, Melle', telefono='011 9876543', email='info@unibio.it'),
            Produttore(nome='Fattoria del Sole', descrizione='Prodotti tipici', indirizzo='Via Roma 1, Cuneo', telefono='0171 987654', email='sole@gmail.com'),
            Produttore(nome='Azienda Agricola La Quiete', descrizione='Frutta e verdura', indirizzo='Via Torino 3, Alba', telefono='0173 987654', email='bioquiete@yahoo.it'),
        ]

        prodotti = [
            Prodotto(produttore_id=1, nome='Olio extravergine di oliva Bio'),
            Prodotto(produttore_id=1, nome='Mele Golden'),
            Prodotto(produttore_id=2, nome='Farina di grano tenero'),
            Prodotto(produttore_id=2, nome='Miele di acacia Bio'),
            Prodotto(produttore_id=3, nome='Riso Originario integrale'),
            Prodotto(produttore_id=3, nome='Formaggio Toma'),
            Prodotto(produttore_id=4, nome='Zucchine novelle'),
        ]

        lotti = [
            Lotto(prodotto_id=1, data_consegna=datetime.strptime('2024-06-27', '%Y-%m-%d'), qta_unita_misura='L', qta_lotto=100, prezzo_unitario=8.50, sospeso=False),
            Lotto(prodotto_id=1, data_consegna=datetime.strptime('2024-07-29', '%Y-%m-%d'), qta_unita_misura='L', qta_lotto=500, prezzo_unitario=8.50, sospeso=False),
            Lotto(prodotto_id=2, data_consegna=datetime.strptime('2024-07-28', '%Y-%m-%d'), qta_unita_misura='Kg', qta_lotto=200, prezzo_unitario=2.50, sospeso=True),
            Lotto(prodotto_id=2, data_consegna=datetime.strptime('2024-07-30', '%Y-%m-%d'), qta_unita_misura='Kg', qta_lotto=100, prezzo_unitario=2.50, sospeso=False),
            Lotto(prodotto_id=3, data_consegna=datetime.strptime('2024-07-27', '%Y-%m-%d'), qta_unita_misura='Kg', qta_lotto=100, prezzo_unitario=2.00, sospeso=False),
            Lotto(prodotto_id=3, data_consegna=datetime.strptime('2024-07-29', '%Y-%m-%d'), qta_unita_misura='Kg', qta_lotto=50, prezzo_unitario=2.00, sospeso=False),
            Lotto(prodotto_id=4, data_consegna=datetime.strptime('2024-07-28', '%Y-%m-%d'), qta_unita_misura='Kg', qta_lotto=200, prezzo_unitario=5.00, sospeso=True),
            Lotto(prodotto_id=4, data_consegna=datetime.strptime('2024-07-30', '%Y-%m-%d'), qta_unita_misura='Kg', qta_lotto=100, prezzo_unitario=5.00, sospeso=False),
            Lotto(prodotto_id=5, data_consegna=datetime.strptime('2024-07-27', '%Y-%m-%d'), qta_unita_misura='Kg', qta_lotto=100, prezzo_unitario=3.00, sospeso=False),
        ]

        users = [
            User(cognome='Rossi', nome='Paolo', telefono=   '3304953849', email='prossi@gmail.xxx', password='pwd123'),
            User(cognome='Bianchi', nome='John', telefono=  '3245903845', email='jhonb@ymail.yyy', password='pwd321'),
            User(cognome='Verdi', nome='Giuseppe', telefono='3456748567', email='g.verdi@live.zzz', password='pwd456'),
            User(cognome='Neri', nome='Francesca', telefono='3834565646', email='franeri@neri.xyz', password='pwd654'),
            User(cognome='Bruni', nome='Carla', telefono=   '3347866223', email='bc@brunimail.abc', password='pwd789'),
        ] 

        prenotazioni = [
            Prenotazione(user_id=1, lotto_id=1, qta=2),
            Prenotazione(user_id=2, lotto_id=2, qta=1),
            Prenotazione(user_id=3, lotto_id=3, qta=3),
            Prenotazione(user_id=4, lotto_id=4, qta=2),
            Prenotazione(user_id=5, lotto_id=5, qta=1),
            Prenotazione(user_id=1, lotto_id=6, qta=2),
            Prenotazione(user_id=2, lotto_id=7, qta=1),
            Prenotazione(user_id=3, lotto_id=8, qta=3),
            Prenotazione(user_id=4, lotto_id=9, qta=2),
        ]

        db.session.bulk_save_objects(produttori + prodotti + lotti + users + prenotazioni)
        db.session.commit()

if __name__ == '__main__':
    init_db()
