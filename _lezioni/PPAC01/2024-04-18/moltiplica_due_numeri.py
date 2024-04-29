import sys

# path_script = sys.argv[0]

if len(sys.argv) != 3:
    print('Il numero di parametri passati non è corretto. Devi passare due numeri.')
else:

    try:
        primo_numero = float(sys.argv[1])
    except ValueError:
        print('Hai inserito un valore che non può essere converito in float:', sys.argv[1])

    try:
        secondo_numero = float(sys.argv[2])
    except ValueError:
        print('Hai inserito un valore che non può essere converito in float:', sys.argv[2])


    risultato = primo_numero * secondo_numero

    print(f'Il risultato di {primo_numero} per {secondo_numero} è uguale a {risultato}')
