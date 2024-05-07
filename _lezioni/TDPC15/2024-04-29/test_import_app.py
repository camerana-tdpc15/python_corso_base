# Che cosa è __name__ ??

# Importo l'altro file dell'esperimento
import test_app

print('----------------------------------------------------------------------')
print('Questo è il valore di __name__ di test_import_app.py:', repr(__name__))
print('Questo è il tipo di __name__ di test_import_app.py:', type(__name__))

# Se questo file viene eseguito come script, allora il valore di __name__ sarà
# "__main__", il che indica che questo è lo script iniziale che è stato eseguito.

# Se questo file viene importato come modulo, allora il valore di __name__ sarà
# "test_import_app", ovvero il nome del modulo (che è il medesimo del file).
# Inoltre questo nome funge da "namespace", ovvero da spazio dei nomi per tutto
# ciò che esso contiene.