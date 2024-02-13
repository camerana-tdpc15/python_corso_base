testo = """Ed è proprio da questa portentosa crema che nasce la crema al mascarpone
base del tiramisù, prima classificata al premio Crema dell'Anno insieme
alla nutella. Il dolce italiano per eccellenza, quello più famoso e amato,
ma soprattutto che ha dato vita a tantissime altre versioni, anche tiramisù senza uova!
Poi il Tiramisù alle fragole o quello alla Nutella, giusto per citarne un paio!
Senza contare le rivisitazioni più raffinate come la crostata morbida o la torta al tiramisù.
"""

testo_diviso = testo.split()

testo_censurato_lista = []




parola_malefica1 = "Tiramisù"
parola_malefica2 = "nutella"

censura = "******"

testo_censurato = ''


for parola in testo_diviso:
    parola_pulita = parola.strip('')
    if parola_pulita.upper() == parola_malefica1.upper():
        parola = censura
        testo_censurato_lista.append(parola)
    elif parola_pulita.upper() == parola_malefica2.upper():
        parola = censura
        testo_censurato_lista.append(parola)
    else:
        testo_censurato_lista.append(parola)


        
    
print(testo_censurato_lista)
