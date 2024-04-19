# Numero di voti per ciascuna materia
qta_voti = 5

# Chiede all'utente di inserire i dati dell'alunno
nome_alunno = input("Inserisci nome e cognome dell'alunno: ")
classe_alunno = input("Inserisci la classe dell'alunno: ")

# Dizionario per registrare i voti di ciascuna materia
voti_per_materia = {
    'Matematica': [],
    'Italiano': [],
    'Inglese': [],
    'Storia': [],
    # 'Scienze': []
}

# Chiede all'utente di inserire i voti per ogni materia
for materia in voti_per_materia:
    print(f'Inserisci {qta_voti} voti per la materia "{materia}": ')
    for n in range(qta_voti):
        voto = int(input(f"Voto {n+1}: "))
        voti_per_materia[materia].append(voto)

# Calcola la media per ogni materia e la media globale
somma_medie = 0
print(f"\nRisultati per l'alunno {nome_alunno} della classe {classe_alunno}:")
for materia, voti in voti_per_materia.items():
    media_materia = sum(voti) / len(voti)
    print(f"Media per {materia}: {media_materia:.2f}")
    somma_medie += media_materia

media_globale = round(somma_medie / len(voti_per_materia))
print(f"Media globale dell'alunno: {media_globale}")

# Trova il voto più alto e il più basso
tutti_i_voti = [voto for voti in voti_per_materia.values() for voto in voti]
voto_piu_alto = max(tutti_i_voti)
voto_piu_basso = min(tutti_i_voti)

print(f"Il voto più alto dell'alunno: {voto_piu_alto}")
print(f"Il voto più basso dell'alunno: {voto_piu_basso}")
