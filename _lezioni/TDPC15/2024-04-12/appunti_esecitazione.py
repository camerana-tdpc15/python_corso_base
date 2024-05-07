
# Inizialmente possiamo provare scrivere l'algoritmo chiedendo solo
# 2 voti per materia
num_voti = 2

# ------------------------------

# Chiedo all'utente di inserire il nome dell'alunno
nome = input('.....')

# # Chiedo all'utente di inserire la classe dell'alunno
classe = input('.....')

# ------------------------------

# Chiedo di inserire i voti di "Matematica"
print('Inserisci i voti per Matematica')
voti_matematica = []
# Per ciascun voto da inserire:
for idx in range(num_voti):
    # Chiedo di inserire il voto
    voto = int(input(f'Voto {idx+1}: '))
    voti_matematica.append(voto)


# Chiedo di inserire i voti di "......."
# Per ciascun voto da inserire:
    # Chiedo di inserire il voto

# Calcolo la media per ciascuna materia
# Ottengo la media per "Matematica"
# Ottengo la media per ".........."
# ...

# ------------------------------

# USANDO DUE LISTE

materie = ['Matematica', 'Italiano']
voti_materia = [ ]
# voti_materia = [ [34, 34, 67, 78, 64], [34, 34, 67, 78, 64] ]

for materia in materie:
    voti = []
    # Per ciascun voto da inserire:
    for idx in range(num_voti):
        # Chiedo di inserire il voto
        voto = int(input(f'Voto {idx+1}: '))
        voti.append(voto)
    voti_materia.append(voti)
# ------------------------------

# USANDO UN DIZIONARIO

# Questa potrebbe essere una comoda struttura dati per memorizzare i
# voti per materia
voti_per_materia = {
    'Matematica': [],
    'Italiano': [],
    # ...
}

# Su un dizionario possiamo iterare per chiave e valore
for materia, voti in voti_per_materia.items():
    print(materia)
    print(voti)

# ------------------------------

# Possiamo concatenare una sola lista concatenando più liste
nuova_lista = [45, 67] + [45, 67]

# Possiamo farlo anche direttamente all'interno della chiamata a una funzione
sum([45, 67] + [45, 67])

# ------------------------------

# A sum, len, min e max possiamo passare degli iterabili
media_mat = sum([45, 67]) / len([45, 67])
minimo = min([45, 67])
massimo = max([45, 67])

