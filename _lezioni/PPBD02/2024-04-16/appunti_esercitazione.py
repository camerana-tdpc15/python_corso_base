num_voti = 2

#_____________________________
# Caso 1: variabili "libere"
# (più ripetizioni di codice)

matematica = []
italiano = []
inglese = []
storia = []

print('Inserire i voti per Matematica')
for idx in range(2):
    voto = int(input(f'Voto {idx+1}: '))
    matematica.append(voto)

print('Inserire i voti per Italiano')
for idx in range(3):
    voto = int(input(f'Voto {idx+1}: '))
    italiano.append(voto)

print('Inserire i voti per Inglese')
for idx in range(3):
    voto = int(input(f'Voto {idx+1}: '))
    inglese.append(voto)

print('Inserire i voti per Storia')
for idx in range(3):
    voto = int(input(f'Voto {idx+1}: '))
    storia.append(voto)

#_______________________________
# Caso 2: liste
# Uso di clicli annidati

materie = ['Matematica', 'Italiano', 'Inglese', 'Storia']
voti = []
# voti = [[...], [...], [...], [...]]

#_______________________________
# Caso 3: dizionario
# Uso di clicli annidati

voti_per_materia = {
    'Matematica': [],
    'Italiano': [],
    'Inglese': [],
    'Storia': []
}

#________________________________

# Chiedere all'utente il Nome e Cognome dell'alunno
# Chiedere all'utente la classe dell'alunno

# Per Matematica:
# Per ciascuno dei 5 voti da chiedere:
for idx in range(num_voti):
    # Chiedi voto 1
    # Chiedi voto 2
    ...

# Calcolo della media per Matematica
# (somma di tutti i valori diviso il numero dei valori)

# Calcolo della media globale (la media delle medie)
# (la somma delle medie delle diverse materie diviso il numero di materie)

# Recupero il voto più alto
# (max) : elenco di valori come argomenti
#       : una lista di valori

# Recupero il voto più basso
# (min) : elenco di valori come argomenti
#       : una lista di valori

# es: min([34, 56, 4])

# ______________________________

lista_materie = ['Matematica', 'Italiano', 'Inglese', 'Storia']

voto_max = 0
voto_min = 101

# Per ciascuna materia
for mat in lista_materie:
    print('Inserisci i voti per', mat)
    # Per ciascuno dei 5 voti da chiedere:
    voti_input = []
    for idx in range(num_voti):
        # Chiedi voto idx + 1
        voto = int(input('...'))
        voti_input.append(voto)

        if voto > voto_max:
            voto_max = voto
        if voto < voto_min:
            voto_min = voto

    voti.append(voti_input)