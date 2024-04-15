# richiesta dati alunno
alunno = input("Inserisci il nome e cognome dell'alunno: ")
classe = input("Inserisci la classe dell'alunno: ")

# creazione dizionario materie e voti
voti_per_materia = {
    "Matematica": [],
    "Italiano": [],
    "Inglese": [],
    "Storia": []
    }


# funzione per controllo immissione voti
def chiedi_voti(materia):
    while True:
        voto = int(input(f"{materia} voto {i+1}: "))
        if 0 <= voto <= 100:
            return voto
        else:
            print("Il voto deve essere compreso tra 0 e 100. Riprova.")

# funzione per calcolo media voti per materia
def calcola_media(voti):
    return sum(voti) / len(voti)

# inserimento voti materia
for materia in voti_per_materia:
    for i in range(5):
        voto = chiedi_voti(materia)
        voti_per_materia[materia].append(voto)

# calcolo delle medie
medie_per_materia = {}
for materia, voti in voti_per_materia.items():
    media = calcola_media(voti)
    medie_per_materia[materia] = format(media, '.2f')

voti_totali = [voto for lista_voti in voti_per_materia.values() for voto in lista_voti]
media_globale = round(calcola_media(voti_totali))

# ricerca voti massimo e minimo
voto_massimo = max(voti_totali)
voto_minimo = min(voti_totali)


# output di stampa
for materia, media in medie_per_materia.items():
    print(f"Media per {materia}: {media}")
    
print(f"Media globale dell'alunno: {media_globale}")

print(f"Voto più alto dell'alunno: {voto_massimo}")

print(f"Voto più basso dell'alunno: {voto_minimo}")



