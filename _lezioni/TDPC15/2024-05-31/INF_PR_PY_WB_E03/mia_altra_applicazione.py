# Provo a importare il modulo "app", che contiene l'applicazione Flask.
# Se in app.py è contenuta la condizione if __name__ == '__main__':
# e il server viene avviato dopo tale condizione, allora il server non 
# dovrebbe avviarsi quando eseguiamo questo script.
# In caso contrario il server si avvierebbe, e questo non è un comportamento
# auspicabile, dato che stiamo solo importando degli oggetti da quel modulo!

from app import home, number_range

...