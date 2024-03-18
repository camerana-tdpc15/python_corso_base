

#esercizio 01

#Scrivi un programma che chieda due numeri all'utente tramite 
#la funzione input e mostri il più grande tra i due utilizzando la funzione print.
#Per quanto Python disponga di una funzione max(), siete invitati ad utilizzare le 
#istruzioni istruzioni if, elif ed else per la scrittura dell'algoritmo.

#Ecco qui

#a=int(input('Inserisce un numero'))
#b=int(input('Inserisce un numero'))
#if a==b:
#    print('I numeri sono uguali')
#elif a>b:
#    print('Il numero piu grande e'+str (a))
#else:
#    print('Il numero piu grande e '+str (b))


#Esercizio 02
#Scrivi un programma che chieda tre numeri a, b, c all'utente e mostri il più grande tra loro.

a=int(input('Inserisci primo numero'))
b=int(input('Inserisci secondo numero'))
c=int(input('Inserisce terzo numero'))

if a==b==c:
    print('I numeri sono uguali')
elif a>=b and a>=c:
    print(a)
elif b>=a and b>=c:
    print(c)
elif c>=a and c>=b:
    print(c)


