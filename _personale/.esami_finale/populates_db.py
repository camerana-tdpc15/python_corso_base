from datetime import datetime
from models import db, Locale, Replica, Evento, Utente, Prenotazione


def init_db():

    db.create_all()

    if not Utente.query.first():

        # Inserisci dati iniziali nelle tabelle
        locali = [
            Locale(nome_locale='Music Lounge', luogo='Ponte3-Piano2', posti=150),
            Locale(nome_locale='Teatro', luogo='Ponte8-Piano3', posti=350),
            Locale(nome_locale='Casin\u00f2', luogo='Ponte7-Piano4', posti=450),
            Locale(nome_locale='Piscina', luogo='Ponte5-Piano9', posti=150),

        ]

        repliche = [
            Replica(evento_id=1, data_ora=datetime.strptime('27-07-2024-20:30:00','%d-%m-%y %-H:%M:%S'),annulato=0),
            Replica(evento_id=1, data_ora=datetime.strptime('28-07-2024-20:30:00','%d-%m-%y %-H:%M:%S'),annulato=0),
            Replica(evento_id=1, data_ora=datetime.strptime('29-07-2024-20:30:00','%d-%m-%y %-H:%M:%S'),annulato=0),
            Replica(evento_id=2, data_ora=datetime.strptime('01-08-2024-20:30:00','%d-%m-%y %-H:%M:%S'),annulato=0),
            Replica(evento_id=3, data_ora=datetime.strptime('30-07-2024-21:00:00','%d-%m-%y %-H:%M:%S'),annulato=0),
            Replica(evento_id=3, data_ora=datetime.strptime('27-07-2024-21:00:00','%d-%m-%y %-H:%M:%S'),annulato=1),
         
        ]

        eventi = [
            Evento(locale_id=1,nome_evento='Concerto di Chopin',  sospeso=False),
            Evento(locale_id=1,nome_evento='Beethoven sul mare',  sospeso=False),
            Evento(locale_id=2,nome_evento='Il ventaglio - Goldoni',  sospeso=False),
            Evento(locale_id=4,nome_evento='Pool Brunch Party',  sospeso=False),

            
        ]

        utenti = [
            Utente(cognome='Cassini', nome='Antonio', telefono=   '3351122333', email='casi.anto@mail.com', password='Cassini77!'),
            Utente(cognome='Benedetti', nome='Bianca', telefono=  '3384455666', email='b.bianca@usrmail.it', password='benBianca44'),
            Utente(cognome='Siciliano', nome='Elena', telefono='3389988555', email='sic89@tel.com', password='sicEl55!'),
            Utente(cognome='Fornari', nome='Enrico', telefono='3335566223', email='for.enrico@mail.com', password='Enrico99.'),

        ] 

        prenotazioni = [
            Prenotazione(utenti_id=1, replica_id=4, quantita=2),
            Prenotazione(utenti_id=2, replica_id=2, quantita=5),
            Prenotazione(utenti_id=1, replica_id=2, quantita=2),
            Prenotazione(utenti_id=4, replica_id=4, quantita=2),
        ]

        db.session.bulk_save_objects(locali + repliche + eventi + utenti + prenotazioni)
        db.session.commit()

if __name__ == '__main__':
    init_db()
