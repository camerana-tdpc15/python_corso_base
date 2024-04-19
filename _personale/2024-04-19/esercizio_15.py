# scrivi qui

from datetime import date
import os

cwd = os.getcwd()
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)


# print("Current Work Directory: ", cwd)
# print("Script Path: ", script_path)
# print("Script Dir: ", script_dir)


# my_date = date(2024, 4, 10)
# my_date = date.fromisoformat('2024-04-10')
# my_date = date.today()


# print(my_date.day)
# print(my_date.month)
# print(my_date.year)

oggi = date.today()
anno_corrente = oggi.year


# print(anno_corrente)

report = {}

'''
import os
# Ottiene la Current Working Directory
cwd = os.getcwd()

# Ottiene il percorso assoluto dello script corrente
script_path = os.path.abspath(__file__)

# Ottiene la directory in cui risiede lo script
script_dir = os.path.dirname(script_path)

'''

nome_file = 'nomi_data_nascita.txt'

open_dir = script_dir + "\\" + nome_file

# print(open_dir)


file = open(open_dir, encoding='utf-8')

lista_report = []


for linee in file:
    linee = linee.rstrip('\n')
    linee = linee.strip()
    linee = linee.split(': ')
    # lista_linee.append(linee)
    # print(linee)
    # print(repr(linee))
    nome = linee[0]
    anno = int(linee[1])
    eta = anno_corrente - anno
    # print("Nome: ", nome)
    # print("Anno: ", anno)
    # print("Età: ", eta)


    if eta in report:
        lista_report = report[eta]
        lista_report.append(nome)
        report[eta] = lista_report
    else:
        lista_report = []
        lista_report.append(nome)
        report[eta] = lista_report

print(report)



file.close()

