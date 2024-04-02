
def conta_vocali(stringa):
    conteggio = 0
    stringa = stringa.upper()
    for vocale in 'AEIOU':
        conteggio += stringa.count(vocale)
    return conteggio

testo = input('inserire un testo:')
conta_vocali(testo)

print('La stringa contiene', conta_vocali(testo), 'vocali')