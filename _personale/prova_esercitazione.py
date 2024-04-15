# Importazione librerie necessarie
import math

# Definizione funzione per calcolare la media
def calcola_media(voti):
  """
  Calcola la media di una lista di voti.

  Argomenti:
    voti: Lista di voti interi.

  Restituisce:
    La media aritmetica dei voti con due cifre decimali.
  """
  media = sum(voti) / len(voti)
  return round(media, 2)

# Richiesta dati all'utente
nome = input("Inserisci nome e cognome dell'alunno: ")
classe = input("Inserisci la classe dell'alunno: ")

# Creazione lista voti
voti_matematica = int(input("Inserisci il voto in Matematica (centesimi): "))
voti_italiano = int(input("Inserisci il voto in Italiano (centesimi): "))
voti_inglese = int(input("Inserisci il voto in Inglese (centesimi): "))
voti_storia = int(input("Inserisci il voto in Storia (centesimi): "))

# Creazione lista voti e dizionario materie
voti = [voti_matematica, voti_italiano, voti_inglese, voti_storia]
materie = {"Matematica": voti_matematica, "Italiano": voti_italiano, "Inglese": voti_inglese, "Storia": voti_storia}

# Calcolo e stampa media per ogni materia
for materia, voto in materie.items():
  media_materia = calcola_media([voto])
  print(f"Media {materia}: {media_materia:.2f}")

# Calcolo e stampa media globale
media_globale = calcola_media(voti)
print(f"Media Globale: {math.ceil(media_globale)}")

# Trovare e stampare voto massimo e minimo
voto_massimo = max(voti)
voto_minimo = min(voti)
print(f"Voto Massimo: {voto_massimo}")
print(f"Voto Minimo: {voto_minimo}")
