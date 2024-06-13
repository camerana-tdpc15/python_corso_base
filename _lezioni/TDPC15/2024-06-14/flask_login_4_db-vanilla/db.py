import sys
import os
import csv
import sqlite3
from settings import DATABASE, USER_TABLE_NAME, USER_TABLE_CSV

# Per ora usiamo una lista di dizionari per simulare un database di film.
# @TODO: utilizzare anche qua una tabella del database, come per gli utenti.
FILMS = [
    {'title': 'Akira', 'image': 'akira.jpg'},
    {'title': 'Ghost in the Shell', 'image': 'gits.jpg'},
    {'title': 'Blade Runner', 'image': 'blade-runner.jpg'},
    {'title': 'Hackers', 'image': 'hackers.jpg'},
    {'title': 'Nirvana', 'image': 'nirvana.jpg'},
]

def get_user_password(username):
    """
    Cerca un utente nel database sulla base del suo username e restituisce
    la sua password se l'utente è presente, altrimenti `None`.
    
    :param username: Lo username dell'utente da cercare.
    :return: La password dell'utente se trovato, altrimenti None.
    """
    try:
        # Connessione al database
        conn = sqlite3.connect(DATABASE)
        # Creazione di un cursore
        cursor = conn.cursor()
        # Preparazione della query SQL
        query = f"SELECT PASSWORD FROM {USER_TABLE_NAME} WHERE LOGIN = ?"
        # Esecuzione della query
        cursor.execute(query, (username,))
        # Recupero del risultato
        result = cursor.fetchone()  # tuple es. ('password1',)
        # Chiusura della connessione
        conn.close()
        # Restituisce la password se l'utente è stato trovato
        if result:
            return result[0]
        else:
            return None

    except sqlite3.Error as err:
        print(f"Si è verificato un errore durante l'accesso al database: {err}")
        return None


def table_exists(cursor, table_name):
    """
    Controlla se una tabella esiste nel database.
    :param cursor: Il cursore per eseguire le query.
    :param table_name: Il nome della tabella da cercare.
    :return: True se la tabella esiste, False altrimenti.
    """
    cursor.execute('''
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?;
    ''', (table_name,))
    return cursor.fetchone() is not None


def _create_user_table(cursor):
    """
    Crea la tabella utente nel database.
    :param cursor: Il cursore per eseguire le query.
    """
    cursor.execute(f'''
        CREATE TABLE {USER_TABLE_NAME}
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        LOGIN TEXT NOT NULL UNIQUE,
        PASSWORD TEXT NOT NULL,
        NOME TEXT,
        COGNOME TEXT,
        INDIRIZZO TEXT,
        CITTA TEXT,
        TEL1 TEXT,
        TEL2 TEXT,
        EMAIL TEXT,
        DATANASCITA DATE,
        DATAREG DATE);
    ''')


def _init_user_table():
    """
    Inizializza la tabella degli utenti nel database e la popola con i dati
    contenuti nel file CSV `users.csv`.
    """
    # Verifica se il file CSV esiste
    if os.path.exists(USER_TABLE_CSV):
        # Usa un blocco try-except per gestire eventuali errori in modo controllato
        try:
            # Apre la connessione al DB
            conn = sqlite3.connect(DATABASE)
            # Apre un contesto sulla connessione
            with conn:
                # Crea un cursore per poter eseguire le query
                cursor = conn.cursor()

                # Se la tabella utente non esiste, la crea e la popola
                if not table_exists(cursor, USER_TABLE_NAME):

                    # Crea la tabella utente
                    _create_user_table(cursor)

                    # Apre il file CSV per la lettura
                    with open(USER_TABLE_CSV, 'r') as file:
                        # Utilizza csv.DictReader per leggere il file CSV.
                        # DictReader usa la prima riga del file come nomi delle
                        # chiavi del dizionario, che corrispondono alle colonne/campi.
                        csv_dict_reader = csv.DictReader(file)
                        
                        # Prepara la query SQL per l'inserimento dei dati 
                        user_query = f'''
                            INSERT INTO {USER_TABLE_NAME}
                            (LOGIN, PASSWORD, NOME, COGNOME, INDIRIZZO, CITTA, TEL1, TEL2, EMAIL, DATANASCITA, DATAREG)
                            VALUES (:LOGIN, :PASSWORD, :NOME, :COGNOME, :INDIRIZZO, :CITTA, :TEL1, :TEL2, :EMAIL, :DATANASCITA, :DATAREG);
                        '''

                        # Popola la tabella eseguendo la query per ogni riga del file CSV
                        cursor.executemany(user_query, csv_dict_reader)

                    print('La tabella utente è stata inizializzata e popolata con successo.')
                else:
                    print('La tabella utente esiste già. Non è necessario inizializzarla.')

                # Non è necessario fare commit e chiudere la connessione se
                # si usa `with` per gestire la connessione, ma è una buona prassi.
                conn.commit()
            conn.close()

        except sqlite3.Error as err:
            print(f'Si è verificato un errore del database: {err}')
            sys.exit(1)

        except Exception as err:
            print(f'Si è verificato un errore generico: {err}')
            sys.exit(1)

    else:
        print(f'Il file "{USER_TABLE_CSV}" non esiste. Verifica il percorso e riprova.')
        sys.exit(1)
