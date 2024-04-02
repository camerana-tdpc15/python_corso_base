from pathlib import Path

# La cartella in cui si trova l'utente quando esegue lo script nel terminale
# viene chiamata "working directory" (cartella di lavoro).
# La working directory può non essere la stessa in cui si trova lo script,
# infatti, se indichiamo lo script con il suo percorso assoluto o relativo,
# al momento dell'esecuzione potremmo trovarci anche in un'altra cartella.
# Ad es. se lo eseguiamo così: $ py C:\Users\Utente\Documents\script.py
user_dir = Path.cwd()
# Oppure:
# user_dir = Path('.').resolve()

# In questo modo invece si ottiene il percorso assoluto dello script
# ATTENZIONE: Su Jupyter Notebook, __file__ non è definito, quindi non funziona.
script_path = Path(__file__).resolve()

# Da questo si può ottenere la cartella in cui si trova lo script
script_dir = script_path.parent

print('---------------------------------')
print(f'{user_dir=}')
print(f'{__file__=}')
print(f'{script_path=}')
print(f'{script_dir=}')
print('---------------------------------')
