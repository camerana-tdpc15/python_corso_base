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

      




print('Inserisci 5 voti per la materia "Matematica"')

voti_matematica = inputVoti()

print(voti_matematica)
