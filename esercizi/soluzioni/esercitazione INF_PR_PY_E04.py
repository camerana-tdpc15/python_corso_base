name = input("Inserisci nome e cognome dell'alunno: ")
classe = input("Inserisci la classe dell'alunno: ")

# Inizializzo le liste dei voti
voti_matematica = []
voti_italiano = []
voti_inglese = []
voti_storia = []
print('Inserisci 5 voti per la materia "Matematica":')
for i in range(5):
    while True:
        voto = int(input(f"Voto {i+1}: "))
        if voto < 0 or voto > 100:
            print("Il valore inserito non è valido! Inserisci un voto compreso tra 0 e 100.")
        else:
            voti_matematica.append(voto)
            break

print('Inserisci 5 voti per la materia "Italiano":')
for i in range(5):
    while True:
        voto = int(input(f"Voto {i+1}: "))
        if voto < 0 or voto > 100:
            print("Il valore inserito non è valido! Inserisci un voto compreso tra 0 e 100.")
        else:
            voti_italiano.append(voto)
            break

print('Inserisci 5 voti per la materia "Inglese":')
for i in range(5):
    while True:
        voto = int(input(f"Voto {i+1}: "))
        if voto < 0 or voto > 100:
            print("Il valore inserito non è valido! Inserisci un voto compreso tra 0 e 100.")
        else:
            voti_inglese.append(voto)
            break

print('Inserisci 5 voti per la materia "Storia":')
for i in range(5):
    while True:
        voto = int(input(f"Voto {i+1}: "))
        if voto < 0 or voto > 100:
            print("Il valore inserito non è valido! Inserisci un voto compreso tra 0 e 100.")
        else:
            voti_storia.append(voto)
            break
    
elenco_voti = (voti_matematica + voti_italiano + voti_inglese + voti_storia)

print("Risultati per l'alunno",name,"della classe",classe,":")
somma_voti_matematica = sum(voti_matematica)
media_matematica = somma_voti_matematica / len(voti_matematica)
print('Media per matematica:', format(media_matematica, '.2f'))

somma_voti_italiano = sum(voti_italiano)
media_italiano = somma_voti_italiano / len(voti_italiano)
print('Media per italiano:', format(media_italiano, '.2f'))

somma_voti_inglese = sum(voti_inglese)
media_inglese = somma_voti_inglese / len(voti_inglese)
print('Media per inglese:', format(media_inglese, '.2f'))

somma_voti_storia = sum(voti_storia)
media_storia = somma_voti_storia / len(voti_storia)
print('Media per storia:', format(media_storia, '.2f'))

media_globale = ((media_matematica+media_italiano+media_inglese+media_storia)/5)
print("Media globale dell'alunno:", round(media_globale))

voto_alto = max(elenco_voti)
print("Il voto più alto dell'alunno:", voto_alto)

voto_minimo = min(elenco_voti)
print("Il voto più basso dell'alunno:", voto_minimo)