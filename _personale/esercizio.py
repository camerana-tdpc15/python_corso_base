#creo funzione della media
def media(voti):
    num_voti = voti.__len__()
    media = float((sum(voti)) / num_voti) 
    return media

 # dichiaro variabili con input
alunno = input("Inserisci nome e cognome dell'alunno : " )
classe = input("inserisci la classe dell'allunno : ")

num_voti = 5
num_materie = 4

# dichiaro la variabile voti_matematica []
voti_matematica = []
voti_italiano = []
voti_inglese = []
voti_storia = []

voti_minimi = []
voti_massimi = []

#voglio far inserire 5 voti per matematica
for voto_matematica in range(num_voti) :
    voti_matematica.append(int(input("inserisci 5 voti per matematica ")))

# voglio far inserire 5 voti per italiano
for voto_italiano in range(num_voti) :
    voti_italiano.append(int(input("inserisci 5 voti per italiano ")))

# voglio far inserire 5 voti per inglese
for voto_inglese in range(num_voti) :
    voti_inglese.append(int(input("inserisci 5 voti per inglese ")))

# voglio far inserire 5 voti per storia
for voto_storia in range(num_voti) :
    voti_storia.append(int(input("inserisci 5 voti per storia ")))


# calcolo la media di matematica
media_matematica = media(voti_matematica)

# calcolo la media di italiano
media_italiano = media(voti_italiano)

# calcolo la media di inglese
media_inglese = media(voti_inglese)

# calcolo la media di storia
media_storia = media(voti_storia)


# calcolo la media globale dell'alunno
media_globale = round((media_inglese + media_storia + media_italiano + media_matematica) / num_materie)


# trovo il valore max di matematica
max_matematica = max(voti_matematica)

# trovo il valore max di italiano
max_italiano = max(voti_italiano)

# trovo il valore max di inglese
max_inglese = max(voti_inglese)

# trovo il valore max di storia
max_storia = max(voti_storia)


# trovo il valore max e min di matematica
max_matematica = max(voti_matematica)
min_matematica = min(voti_matematica)
#aggiungo i voti max e min di matematica
voti_minimi.append(min_matematica)
voti_massimi.append(max_matematica)

# trovo il valore max e min di italiano
max_italiano = max(voti_italiano)
min_italiano = min(voti_italiano)
#aggiungo i voti max e min di italiano
voti_minimi.append(min_italiano)
voti_massimi.append(max_italiano)

# trovo il valore max e min di inglese
max_inglese = max(voti_inglese)
min_inglese = min(voti_inglese)
#aggiungo i voti max e min di inglese
voti_minimi.append(min_inglese)
voti_massimi.append(max_inglese)

# trovo il valore max e min di storia
max_storia = max(voti_storia)
min_storia = min(voti_storia)
#aggiungo i voti max e min di storia
voti_minimi.append(min_storia)
voti_massimi.append(max_storia)


#trovo il voto più alto e quello più basso
voto_maggiore = max(voti_massimi)
voto_minore = min(voti_minimi)

print('-' * 100)
print(f"Risultati per l'alunno : {alunno} della classe {classe} :")
print(f"Media per Matematica : {media_matematica}")
print(f"Media per Italiano : {media_italiano}")
print(f"Media per Inglese : {media_inglese}")
print(f"Media per Storia : {media_storia}")
print(f"Media globale dell'alunno: {media_globale}")
print(f"il voto più alto dell'alunno è : {voto_maggiore}")
print(f"il voto più basso dell'alunno è : {voto_minore}")








