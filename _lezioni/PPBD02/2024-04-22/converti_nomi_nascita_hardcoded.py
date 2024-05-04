import sys
import os
from datetime import date

def check_file(input_file, ouptut_file):
    if not os.path.exists(input_file):
        print('ERRORE: Il file di input non esiste!')
        return False
    
    dir_string = os.path.dirname(ouptut_file)

    if not os.path.exists(dir_string):
        print('ERRORE: La cartella di ouptut non esiste!')
        return False

    return True


def converti_file(input_path, output_path):
    anno_corrente = date.today().year
    report = {}
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


# Ottiene il percorso assoluto dello script corrente
script_path = os.path.abspath(__file__)

# Ottiene la directory in cui risiede lo script
script_dir = os.path.dirname(script_path)

# Costruisce un percorso assoluto alla directory dello script
input_absolute_path = os.path.join(script_dir, 'input.txt')
output_absolute_path = os.path.join(script_dir, 'output.csv')

converti_file(input_absolute_path, output_absolute_path)

print('SUCCESSO: Il file è stato creato correttamente alla '
        f'posizione {output_absolute_path}'
)

