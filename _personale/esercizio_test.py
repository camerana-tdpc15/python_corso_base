nome =input ('Inserisci il nome: ')
classeAlunno = input ('Inserisci la classe del alunno: ')

#info da GPT

# Crea una lista vuota
lista_materie = []

# Utilizza un ciclo while per chiedere all'utente di inserire 4 oggetti
while len(lista_materie) < 4:
    materia = input("Inserisci una materia: ")
    lista_materie.append(materia)
# Stampa la lista
print("La tua lista contiene:", lista_materie)

#fatto in aula con prof

voti_materia =[]

for mat in lista_materie:
    print(mat)
    voti = []
    for idx in range (5):
        voto =int (input(f'voti {idx + 1}: '))
        voti.append(voto)
    voti_materia.append(voti)
# print(f'{voti_materia}  {lista_materie}')

                #130424 ALLE 1.20
dict_from_list = dict(zip(lista_materie , voti))
print (dict_from_list)

#  total = 0

#  for value in dict_from_list.values ():
#      total += value
#   print(f"La somma dei valori nel dizionario è: {total}")

    