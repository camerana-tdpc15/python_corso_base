#!/usr/bin/env python3

"""Moltiplica due numeri

This script allows the user to print to the result of the multiplication the two
parameters passed.

Usage:
    ./moltiplica_due_numeri_sm.py 5 2

This file can also be imported as a module and contains the following
functions:

    * moltiplica_due_numeri(a,b) - returns the result of multiplication of a by b

Author:
    Leonardo Galilei (leonardo@galilei.com)

License:
    MIT License

    Copyright (c) 2023 Leonardo Galilei

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

def moltiplica_due_numeri(a, b):
    """
    Function that multiplies two integer or float numbers and returns the result.

    Args:
        a: the first number as int, float or str.
        b: the second number as int, float or str.
    
    Returns:
        The result of the multiplication as float.

    """
    return a * b

if __name__ == '__main__':  # Se viene esegiuto come script
    
    import sys  

    lista_argomenti = sys.argv
    qta_numeri = len(lista_argomenti) - 1  # Non considero il primo argomento, dato che c'è sempre

    def stampa_risultato(num_a, num_b, risultato):
        print('Il prodotto di ' + str(num_a) + ' per ' + str(num_b) + ' è uguale a ' + str(risultato))

    if qta_numeri == 2:
        num_a = float(lista_argomenti[1])  
        num_b = float(lista_argomenti[2])
        prodotto = moltiplica_due_numeri(num_a, num_b)
        stampa_risultato(lista_argomenti[1], lista_argomenti[2], prodotto)

    else:
        err_msg = 'Lo script deve essere eseguito passando due argomenti, il primo e il secondo numero da moltiplicare:'
        errore_input = True
        prodotto = None

        while prodotto is None:
            try:
                if qta_numeri < 2:
                    print(err_msg, f'me ne hai passati {qta_numeri} e sono troppo pochi.', sep='\n')
                    if qta_numeri == 0:
                        num_a = float(input('Inserisci il primo numero:'))
                        num_b = float(input('Inserisci il secondo numero:'))
                    elif qta_numeri == 1:
                        num_a = float(lista_argomenti[1])
                        print(f'Il primo numero me lo hai dato ed è {num_a}.')
                        num_b = float(input('Inserisci il secondo numero:'))

                else:  # elif num_list > 2:
                    print(err_msg, f'me ne hai passati {qta_numeri} e sono troppi! Devo chederti di reinserire i due numeri.', sep='\n')
                    num_a = float(input('Inserisci il primo numero:'))
                    num_b = float(input('Inserisci il secondo numero:'))

                prodotto = moltiplica_due_numeri(num_a, num_b)
                stampa_risultato(num_a, num_b, prodotto)
            except ValueError as err:
                print('I dati inseriti non sono validi:', err)
else:
    pass