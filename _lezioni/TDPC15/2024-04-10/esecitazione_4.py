
num_voti = 2

# Chiedo all'utente di inserire il nome dell'alunno
# nome = input('.....')

# # Chiedo all'utente di inserire la classe dell'alunno
# classe = input('.....')

voti_per_materia = {
    'Matematica': [],
    'Italiano': []
}

for materia, voti in voti_per_materia.items():
    print(materia)
    print(voti)


# Chiedo di inserire i voti di "Matematica"
# print('Inserisci i voti per Matematica')
# voti_matematica = []
# # Per ciascun voto da inserire:
# for ... in range(num_voti):
#     # Chiedo di inserire il voto
#     voto = int(input('.....'))
#     voti_matematica.append(voto)


# Chiedo di inserire i voti di "......."
# Per ciascun voto da inserire:
    # Chiedo di inserire il voto

# Calcolo la media per ciascuna materia
# Ottengo la media per "Matematica"
# Ottengo la media per ".........."
# ...

# ------------------------------
    

materie = ['Matematica', 'Italiano']
voti_materia = [ ]
# voti_materia = [ [34, 34, 67, 78, 64], [34, 34, 67, 78, 64] ]

for materia in materie:
    voti = []
    # Per ciascun voto da inserire:
    for idx in range(num_voti):
        # Chiedo di inserire il voto
        voto = int(input(f'.....{idx+1}'))
        voti.append(voto)
    voti_materia.append(voti)
# ------------------------------


media_mat = sum([45, 67]) / len([45, 67])
minimo = min([45, 67])
massimo = max([45, 67])