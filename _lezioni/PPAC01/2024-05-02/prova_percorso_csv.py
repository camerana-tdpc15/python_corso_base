import csv
import os

r"""
Scopo di questo esempio è far vedere come raggiungere un file in base alla
posizione dello script anziché in base alla Current Working Directory (CWD), la
quale è di default la cartella in cui ci troviamo nel teminale nel momento in
cui abbiamo eseguito lo script, dato che lo script non è detto che si trovi
nella medesima cartella in cui ci troviamo nel terminale.
Ad esempio:

/  # Root del disco
│
└── Repositories/
    │
    └── PPAC01/  # Root del Workspace di VS Code (se eseguo da qua, sarà la CWD)
        │
        └── _lezioni/
            │
            └── PPAC01/
                │
                └── 2024-05-02/
                    │
                    ├── prova_percorso_csv.py  # Questo è il nostro script.
                    │
                    └── botteghe-storiche.csv  # Questo è il file che voglio aprire.

Per esempio, se noi siamo nella root del workspace ed eseguiamo questo script
nel seguente modo:

C:\Repositories\PPAC01\> py _lezioni\PPAC01\2024-05-02\prova_percorso_csv.py

...la Current Working Directory (CWD) sarà C:\Repositories\PPAC01\ 

In questo caso, non possiamo riferirci al file che vogliamo aprire, semplicemente
come "botteghe-storiche.csv", perché esso non si trova nella CWD.

Ci sono vari modi per ovviare a questo problema, io vi consiglio questo che segue,
perché funziona sempre, in ogni caso, indipendentemente dal sistema operativo.

In pratica otteniamo il percorso a questo file di script, e poi ragioniamo
relativamente alla cartella in cui si trova lo script.

"""

# Ottiene il percorso assoluto a QUESTO FILE di script
script_path = os.path.abspath(__file__)

# Ottiene la directory in cui risiede lo script
script_dir = os.path.dirname(script_path)

# Costruisce un percorso assoluto al file che voglio raggiungere, combinando
# la directory dello script con il percorso relativo al file.
file_absolute_path = os.path.join(script_dir, 'botteghe-storiche.csv')

# Stampa i vari oggetti per vedere cosa contengono
print('----------------------------')
print('__file__:', __file__)
print('CWD:', os.getcwd())
print('file_absolute_path:', file_absolute_path)

# Potremmo anche scrivere direttamente dei percorsi assoluti come literal, ma è
# sconsigliato perché se spostiamo la cartella del nostro progetto dovremmo
# correggere i percorsi! Inoltre, la lettera di unità (es. C:\) non è compatibile
# con sistemi Linux o macOS.

# Percorso assoluto, con '/' slash come per gli URL web (unix-like), che è il
# modo CONSIGLIATO per scrivere i percorsi:
# file_absolute_path = 'C:/Repositories/PPBC02/_lezioni/PPAC01/2024-05-02_/botteghe-storiche.csv'

# Percorso assoluto con il '\\' doppio backslash (escaped), SOLO SU WINDOWS:
# file_absolute_path = 'C:\\Repositories\\PPBC02\\_lezioni\\PPAC01\\2024-05-02_\\botteghe-storiche.csv'

# Percorso assoluto con il '\' singolo backslash (non escaped) in rawstring,
# usando una `r` prima della stringa, per evitare di usare il doppio backslash '\\':
# file_absolute_path = r'C:\Repositories\PPBC02\_lezioni\PPAC01\2024-05-02_\botteghe-storiche.csv'

with open(file_absolute_path, 'r', encoding='utf-8') as file_in:
    file_reader = csv.DictReader(file_in, delimiter=",")
    for linea in file_reader:
        if linea['ID'] in ['45', '64']:  # filtro
            print('----------------------------')
            print('ID:', linea['ID'])
            print('Ragione sociale:', linea['Ragione sociale'])
            print('Cap:', linea['Cap'])
