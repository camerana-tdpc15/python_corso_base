testo = """Ed è proprio da questa portentosa crema che nasce la crema al mascarpone
base del tiramisù, prima classificata al premio Crema dell'Anno insieme
alla nutella. Il dolce italiano per eccellenza, quello più famoso e amato,
ma soprattutto che ha dato vita a tantissime altre versioni, anche tiramisù senza uova!
Poi il Tiramisù alle fragole o quello alla Nutella, giusto per citarne un paio!
Senza contare le rivisitazioni più raffinate come la crostata morbida o la torta al tiramisù.
"""


# primo metodo non ottimizzato

'''
parola_malefica1 = "Tiramisù"
parola_malefica2 = "nutella"


censura = "******"

testo_censurato = ''

testo_censurato = testo.replace(parola_malefica1.lower(), censura)
testo_censurato = testo_censurato.replace(parola_malefica1.title(), censura)
testo_censurato = testo_censurato.replace(parola_malefica2.lower(), censura)
testo_censurato = testo_censurato.replace(parola_malefica2.title(), censura)

conta_malefiche = testo_censurato.count(censura)

print('Censurata', conta_malefiche, 'parola')

print(testo_censurato)

'''

# secondo metodo ottimizzato ciclo for

testo2 = """Ed è proprio da questa portentosa crema che nasce la crema al mascarpone
base del tiramisù, prima classificata al premio Crema dell'Anno insieme
alla nutddella. Il dolce italiano per eccellenza, quello più famoso e amato,
ma soprattutto che ha dato vita a tantissime altre versioni, anche tiraddmisù senza uova!
Poi il Tirddamisù alle fragole o quello alla Nuteddlla, giusto per citarne un paio!
Senza contare le rivisitazioni più raffinate come la crostata morbida o la torta al tiraddmisù.
"""

parole_malefiche = ["Tiramisù", "nutella"]

censura = "******"

testo_censurato = testo2

for parola_malefica in parole_malefiche:
    testo_censurato = testo_censurato.replace(parola_malefica.lower(), censura)
    testo_censurato = testo_censurato.replace(parola_malefica.title(), censura)


conta_malefiche = testo_censurato.count(censura)


if conta_malefiche > 1:
    print('Censurate', conta_malefiche, 'parole')
else:
    print('Censurata', conta_malefiche, 'parola')



print(testo_censurato)






