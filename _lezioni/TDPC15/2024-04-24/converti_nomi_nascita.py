from datetime import date
from collections import defaultdict

anno_corrente = date.today().year  # int

# ATTENZIONE: Qua, non possiamo più usare percorsi relatvi in modo "diretto"
#             come facciamo con i Notobook di Jupyter!
#             I percorsi relativi sono sempre riferiti rispetto alla Current
#             Working Directory (CWD), ovvero da dove viene eseguito lo script.
#             Se lo eseguiamo tramite il pulsante "Run" di Visual Studio Code,
#             il terminale viene avviato nella la root del nostro workspace e
#             dunque quella sarà la CWD.
percorso_file = './files_esercizi/nomi_data_nascita.txt'

# Inizializzo il defaultdict
report = defaultdict(lambda: [])  # Funzione anonima

# Apro manualmente il file
mio_file = open(percorso_file, 'r', encoding='utf-8')

for line in mio_file:
    lista_linea = line.split(':')
    nome = lista_linea[0]
    anno_nascita = int(lista_linea[1].strip())   # Attenzione al tipo di dato!!
    eta = anno_corrente - anno_nascita
    
    # Tento di fare l'append in modo diretto.
    # (se la chiave non esiste verrà creata con una lista vuota a cui appendo il nome)
    report[eta].append(nome)
    # report[eta] += [nome]

# Chiudo manualmente il file
mio_file.close()

out_file_path = './files_esercizi/outputs/nomi_eta.csv'

# Uso with ... as per gestire apertura e chiusura del file
with open(out_file_path, 'w', encoding='utf-8') as out_file:
    intestazione = 'Nome,Età\n'
    out_file.write(intestazione)
    for eta, lista_nomi in report.items():
        for nome in lista_nomi:
            # riga = nome + ',' + str(eta) + '\n'
            riga = f'{nome},{eta}\n'
            out_file.write(riga)

# Ora il file è chiuso

print('Il file è stato convertito e lo trovi alla posizione:', out_file_path)
