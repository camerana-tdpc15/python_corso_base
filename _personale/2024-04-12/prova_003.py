num_voti = 5

def inputVoti():
    lista_generica = []
    conta = 1
    while len(lista_generica) < num_voti:
        info = input(f"inserisci voto {conta}: ")
        if info.isdigit():
            info = int(info)
            lista_generica.append(info)
            conta += 1
        else:
            print('ERRORE: Inserire solo valori numerici.')
    return lista_generica
    

test = True
while test:
    nome_alunno = input("Inserisci nome e cognome dell'alunno: ")
    if nome_alunno != "":
        test = False
    else:
         print('ERRORE: Inserire valori alfanumerici')

test = True
while test:
    classe_alunno = input("Inserisci la classe dell'alunno: ")
    if classe_alunno != "":
        test = False
    else:
         print('ERRORE: Inserire valori alfanumerici')

      


voto_massimo_generico = []
voto_minimo_generico = []

print('Inserisci 5 voti per la materia "Matematica"')
voti_matematica = inputVoti()
voto_max_matematica = max(voti_matematica)
voto_min_matematica = min(voti_matematica)
voto_massimo_generico.append(voto_max_matematica)
voto_minimo_generico.append(voto_min_matematica)


print('Inserisci 5 voti per la materia "Italiano"')
voti_italiano = inputVoti()
voto_max_italiano = max(voti_italiano)
voto_min_italiano = min(voti_italiano)
voto_massimo_generico.append(voto_max_italiano)
voto_minimo_generico.append(voto_min_italiano)



print('Inserisci 5 voti per la materia "Storia"')
voti_storia = inputVoti()
voto_max_storia = max(voti_storia)
voto_min_storia = min(voti_storia)
voto_massimo_generico.append(voto_max_storia)
voto_minimo_generico.append(voto_min_storia)



print('Inserisci 5 voti per la materia "Inglese"')
voti_inglese = inputVoti()
voto_max_inglese = max(voti_inglese)
voto_min_inglese = min(voti_inglese)
voto_massimo_generico.append(voto_max_inglese)
voto_minimo_generico.append(voto_min_inglese)

massimo_generico = max(voto_massimo_generico)
minimo_generico = min(voto_minimo_generico)



print(f"Risultati per l'alunno {nome_alunno} della classe {classe_alunno}")


def calcoloMedia(voti):
     media = sum(voti) / len(voti)
     return media

media_matematica = calcoloMedia(voti_matematica)

media_italiano = calcoloMedia(voti_italiano)

media_storia = calcoloMedia(voti_storia)

media_inglese = calcoloMedia(voti_inglese)

media_globale = (media_matematica + media_italiano + media_storia + media_inglese) / 4

print(f'Media per "Matematica": {media_matematica:.2f}')
print(f'Media per "Italiano": {media_italiano:.2f}')
print(f'Media per "Storia": {media_storia:.2f}')
print(f'Media per "Inglese": {media_inglese:.2f}')

print(f"Media globale dell'alunno: {media_globale:.0f}")

print(f"Il voto più alto dell'alunno: {massimo_generico:.0f}")

print(f"Il voto più basso dell'alunno: {minimo_generico:.0f}")



