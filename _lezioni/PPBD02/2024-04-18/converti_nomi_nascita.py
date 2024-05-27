import sys
from datetime import date

args = sys.argv

anno_corrente = date.today().year
report = {}
input_path = args[1]
output_path = args[2]

with open(input_path, mode='r', encoding='utf-8') as file_testo:
    list_lines = file_testo.readlines()

for line in list_lines:
    lista_oggetti = line.split(':')
    nome = lista_oggetti[0].strip()
    anno = int(lista_oggetti[1].strip())
    eta = anno_corrente - anno

    if eta not in report:  # se chiave non è presente
        report[eta] = [nome]
    else:  # se chiave è presente
        report[eta].append(nome)

with open(output_path, 'w', encoding='utf-8') as outupt_file:
    intestazione = 'nome;eta\n'
    outupt_file.write(intestazione)
    for eta in report:
        for nome in report[eta]:
            riga = f'{nome};{eta}\n'
            outupt_file.write(riga)

 
# py        .\converti_nomi_nascita.py   ../../../files_esercizi/nomi_data_nascita.txt   output_nomi.csv  
# COMANDO   SCRIPT (ARGOMENTO 1)         ARGOMENTO 2                                     ARGOMENTO 3DIR