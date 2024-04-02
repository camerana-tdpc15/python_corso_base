import os

# La cartella, nel terminale, in cui si trova l'utente quando esegue lo script,
# può non essere la stessa in cui si trova lo script. Ad esempio, se lo script
# viene indicato con il suo percorso assoluto o relativo.
# Es. py C:\Users\Utente\Documents\script.py
user_dir = os.path.abspath('.')

# In questo modo invece si ottiene il percorso assoluto dello script
# ATTENZIONE: Su Jupyter Notebook, __file__ non è definito, quindi non funziona.
script_path = os.path.abspath(__file__)

# Da questo si può ottenere la cartella in cui si trova lo script
script_dir = os.path.dirname(script_path)

print(f'{user_dir=}')
print(f'{script_path=}')
print(f'{script_dir=}')
