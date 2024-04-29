#DOMANDA PROF: DEVO IMPORTARE LA DEFAULTDICT? chiedo perchè non ho bene compreso e questo l'ho spudoratamente copiato
from collections import defaultdict
# 1. ottendo la "data" o la "data e ora"
#   dal modulo 'datetime' importo la data
from datetime import date

# 2. estraggo l'anno corrente dalla funzione 'today()' di date
anno_corrente = date.today().year

# 3. creo dizionario che mi servirà come contenitore
report = {}

# 4. Percorso relativo al file che si trova nella medesima cartella in cui mi trovo io
mio_file = "C:\\nomi_data_nascita.txt"

# 5. Accedo al file
file = open(mio_file, "r" , encoding="utf-8")

# 6. Per ciascuna riga del file di TESTO con ciclo FOR:
for riga in mio_file:
    # uso split() per eliminare i ':'
    lista_linea = riga.split(":")
    # ottengo nome
    nome = lista_linea[0]
    # ottengo anno_nascita pulendo da i vari spazi e a capo usando strip()
    anno_nascita = int(lista_linea[1].strip())
    # ottengo eta
    eta = anno_corrente - anno_nascita

# 7. Controllo se l'eta (che è la chiave) è presente nel dizionario    
#    Se la chiave con l'età è presente l'appendo
    if eta in report:
        report[eta].append(nome)    
        # Se la chiave con l'età NON è presente creo la lista con quel'eta come chiave e nome come unico elemento
    else:
        report[eta] = [nome]
# 8. Chiudo il file
file.close()
# 9. uso il context manager (whit...open...as) per assegnare ad ogni chiave(eta) i suoi valori(nomi)
with open("nomi_eta.csv", "w", encoding="utf-8") as out_file :
    # metto l'intestazione io a mano
    intestazione = "Nome , eta\n"
    #scrivo l'intestazione nel file
    out_file.write(intestazione)
    # per ogni eta e lista_nomi nel dizionario 'report
    for eta, lista_nomi in report.items():
        # e per ogni nome nella lista_nomi
        for nome in lista_nomi:
            # creo la riga 
            riga = f"{nome} , {eta}"
            # scrivo la riga nrl file out_file
            out_file.write(riga)
