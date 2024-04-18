# Inizializza un dizionario vuoto per i voti
voti_studente = {}

# Chiedi all'utente di inserire il nome dello studente
nome_studente = input("Inserisci il nome dello studente: ")

# Chiedi all'utente di inserire 5 materie e i voti corrispondenti
for _ in range(5):
    materia = input("Inserisci il nome di una materia: ")
    voto = int(input(f"Inserisci il voto per {materia}: "))
    voti_studente[materia] = voto

# Calcola la somma dei voti
somma_voti = sum(voti_studente.values())

# Calcola la media dei voti
media_voti = somma_voti / len(voti_studente)

# Stampa i risultati
print(f"\nVoti dello studente {nome_studente}:")
for materia, voto in voti_studente.items():
    print(f"{materia}: {voto}")

print(f"\nLa somma dei voti è: {somma_voti}")
print(f"La media dei voti è: {media_voti:.2f}")