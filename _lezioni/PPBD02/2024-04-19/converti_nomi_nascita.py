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


args = sys.argv

anno_corrente = date.today().year
report = {}

if len(args) == 3:
    input_path = args[1]
    output_path = args[2]

    if check_file(input_path, output_path):
        converti_file(input_path, output_path)
        path_assoluto = os.path.abspath(output_path)
        print('SUCCESSO: Il file è stato creato correttamente alla '
              f'posizione {path_assoluto}'
        )

elif len(args) == 1:
    print('Non hai passato i 2 parametri necessari: il file di input '
          'e il file di output.')
elif len(args) == 2:
    print('Non hai passato il secondo parametro: il file di output.')
else:
    print('Hai inserito troppi parametri. Ne servono 2: '
          'il file di input e il file di output.')

