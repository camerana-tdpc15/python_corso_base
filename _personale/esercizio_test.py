nome =input ('Inserisci il nome: ')
classeAlunno = input ('Inserisci la classe del alunno: ')

#info da GPT

# Crea una lista vuota
lista_materie = []

# Utilizza un ciclo while per chiedere all'utente di inserire 4 oggetti
while len(lista_materie) < 2:
    materia = input("Inserisci una materia: ")
    lista_materie.append(materia)
# Stampa la lista
#print("La tua lista contiene:", lista_materie)



#fatto in aula con prof

voti_materia =[]

for mat in lista_materie:
    print(mat)
    voti = []
    for idx in range (3):
        voto =int (input(f'voti {idx + 1}: '))
        voti.append(voto)
    voti_materia.append(voti)


                #180424 ALLE  01.00
#print(f'\n{voti_materia},\n{lista_materie}')
#                #CON IA
#somma_voti = sum(voti_materia.values())
#media_voti = somma_voti / len(voti_materia)

#print(f"\nVoti dello studente {nome}:")
#for materia, voto in voti_materia.items():
#    print(f"{materia}: {voto}")





                #130424 ALLE 1.20
dict_from_list = dict(zip(lista_materie , voti_materia))
# print (dict_from_list)
print(f"RESULTATI PER L'ALUNNO {nome} DELLA CLASSE{classeAlunno}\n")




for key,values in dict_from_list.items():
    average =sum(values) /len(values)
    print(f'MEDIA PER {key} = {average:.2f}\n')

# Calcola la somma di tutti i valori nel dizionario
# media_globale = sum(sum(values) for values in dict_from_list.values())

# Stampa la somma totale
# print(f"La media globale dell'alunno {nome} è: {media_totale} / {len(dict_from_list.values)}")

# average = sum(media_globale) / len(media_globale)

# Stampa la media
# print(f"La media di tutti i valori nel dizionario è: {average:.2f}")

# Calcola la somma di tutti i valori
total_sum = sum(sum(values) for values in dict_from_list.values())

# Calcola la media di tutti i valori
all_values = [value for values in dict_from_list.values() for value in values]
average = sum(all_values) / len(all_values)
min_value = min(all_values)
max_value = max(all_values)


print(f"IL VOTO PIU BASSO E: {min_value}\n")
print(f"IL VOTO PIU ALTO E: {max_value}\n")

# Stampa i risultati
# print(f"La somma di tutti i valori nel dizionario è: {total_sum}")
print(f"LA MEDIA GLOBALE DELL'ALUNNO {nome} E: {average:.2f}\n")

voto_piu_alto = {key: max(values) for key, values in dict_from_list.items()}

# Stampa i valori massimi per ciascuna chiave
for key, value in voto_piu_alto.items():
    print(f"IL VOTO PIU ALTO PER '{key}' E : {value}\n")

voto_piu_basso = {key: min(values) for key, values in dict_from_list.items()}

# Stampa i valori massimi per ciascuna chiave
for key, value in voto_piu_basso.items():
    print(f"IL VOTO PIU BASSO PER '{key}' E: {value}\n")








# chiave_max = max(dict_from_list, values=lambda key: dict_from_list[values])

# chiave_min = min(dict_from_list, values=lambda values: dict_from_list[values])



#for key in dict_from_list:
#  somma_voti = sum(dict_from_list.values())





#print (type(dict_from_list))
#print (dict_from_list)

                #180424 ALLE 12.00(ALTE PROVE PER)
#for x, obj in dict_from_list.items():
#    print(x)
#    
#    for y in obj:
#        print(y + ':', obj[y])


#   QUESTO SOPRA NON LO CAPITO



#  total = 0

#  for value in dict_from_list.values ():
#      total += value
#   print(f"La somma dei valori nel dizionario è: {total}")

#for key in dict_from_list.items():
#    print sum(dict_from_list.keys)
    