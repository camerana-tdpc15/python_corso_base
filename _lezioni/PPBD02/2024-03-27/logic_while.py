
def chiedi_continua():
    while True:
        risp = input('Vuoi continuare? Digita s/n e poi premi invio:')
        
        # Trasformo la risposta in minuscolo e prendo il primo carattere
        risp = risp.lower()[0] if risp != '' else None
        
        # Se l'utente ha risposto 's' o 'n'
        # if risp == 's' or risp == 'n':
        if risp in ['s', 'n']:
            # Restituisce l'input utente ed esce dal ciclo
            return risp
        # Se l'utente ha inserito un valore non valido
        else:
            # Non fa nulla (e dunque riparte il ciclo while)
            pass


while True:

    x = input('Prego, inserire un numero:')

    # Se x è un numero
    if x.replace('.', '').isdigit():  # Qua devo valutarlo senza il punto,
                                      # altrimenti non funziona con i float.
                                      # Nota che x non viene modificato.
        
        # Trasformo x in un float
        x = float(x)

        print(f'{x} > 0 and {x} < 100 :', x > 0 and x < 100)
        print(f'{x} > 0 or {x} < 100', x > 0 or x < 100)
        print(f'{x} > 0 or 100 < {x}', x > 0 or 100 < x)
        print(f'{x} > 0 and {x} < 100 or {x} == -1', x > 0 and x < 100 or x == -1)

        # Chiedo all'utente se vuole continuare e quindi
        # leggo un nuovo input dall'utente tramite una funzione ad hoc
        risp = chiedi_continua()
        
        # Se l'utente ha risposto 's'
        if risp == 's':
            # Non faccio nulla
            pass
        # Altrimenti, ha risposto di sicuro 'n' perché la funzione chiedi_continua
        # restituisce solo 's' o 'n'
        else:
            # Interrompo il ciclo while
            break

    else:
        print('Hai inserito un valore non valido: ', x)
        # print('Hai inserito un valore non valido: ' + x)
        # print(f'Hai inserito un valore non valido: {x}')
