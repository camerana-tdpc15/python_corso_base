
from datetime import date
from collections import defaultdict

anno_corrente = date.today().year

percorso_file = './files_esercizi/nomi_data_nascita.txt'

report = defaultdict(lambda:[])

mio_file = open(percorso_file, 'r', encoding = 'utf-8')

for line in mio_file:
    lista_linea= line.split()
    nome = lista_linea[1]

    anno_nascita = int(lista_linea[1].strip())

    eta = anno_corrente - anno_nascita

    report[eta].append(nome)


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




