print('Inserire i seguenti dati e confermarli con invio:')

nome = input('Inserire nome alunno: ')
cognome = input('Inserire cognome alunno: ') 
classe = input('Inserire classe alunno: ')


voto_matematica1 = int(input('Inserire 1° voto di Matematica: '))
voto_matematica2 = int(input('Inserire 2° voto di Matematica: '))
voto_matematica3 = int(input('Inserire 3° voto di Matematica: '))
voto_matematica4 = int(input('Inserire 4° voto di Matematica: '))
voto_matematica5 = int(input('Inserire 5° voto di Matematica: '))


voto_italiano1= int(input('Inserire 1° voto) di Italiano: '))
voto_italiano2 = int(input('Inserire 2° voto di Italiano: '))
voto_italiano3 = int(input('Inserire 3° voto di Italiano: '))
voto_italiano4 = int(input('Inserire 4° voto di Italiano: '))
voto_italiano5 = int(input('Inserire 5° voto di Italiano: '))


voto_inglese1 = int(input('Inserire 1° voto di Inglese: '))
voto_inglese2 = int(input('Inserire 2° voto di Inglese: '))
voto_inglese3 = int(input('Inserire 3° voto di Inglese: '))
voto_inglese4 = int(input('Inserire 4° voto di Inglese: '))
voto_inglese5 = int(input('Inserire 5° voto di Inglese: '))


voto_storia1 = int(input('Inserire 1° voto di Storia: '))
voto_storia2 = int(input('Inserire 2° voto di Storia: '))
voto_storia3 = int(input('Inserire 3° voto di Storia: '))
voto_storia4 = int(input('Inserire 4° voto di Storia: '))
voto_storia5 = int(input('Inserire 5° voto di Storia: '))


media_matematica = (voto_matematica1 + voto_matematica2 + voto_matematica3 + voto_matematica4 + voto_matematica5) / 5

media_italiano = (voto_italiano1 + voto_italiano2 + voto_italiano3 + voto_italiano4 + voto_italiano5) / 5

media_inglese = (voto_inglese1 + voto_inglese2 + voto_inglese3 + voto_inglese4 + voto_inglese5) / 5

media_storia = (voto_storia1 + voto_storia2 + voto_storia3 + voto_storia4 + voto_storia5) / 5


media_globale = (voto_matematica1 + voto_matematica2 + voto_matematica3 + voto_matematica4 + voto_matematica5) + (voto_italiano1 + voto_italiano2 + voto_italiano3 + voto_italiano4 + voto_italiano5) + (voto_inglese1 + voto_inglese2 + voto_inglese3 + voto_inglese4 + voto_inglese5) + (voto_storia1 + voto_storia2 + voto_storia3 + voto_storia4 + voto_storia5) / 4 


print(f'Risultati per l\'alunno {nome} {cognome} della classe {classe}:')

print('Media per Matematica: ', media_matematica)
print('Media per Matematica: ', media_italiano)
print('Media per Matematica: ', media_inglese)
print('Media per Matematica: ', media_storia)

print('Media Globale: ', media_globale)

print('Voto più alto matematica: ', max(voto_matematica1, voto_matematica2, voto_matematica3, voto_matematica4, voto_matematica5))
print('Voto più alto italiano: ', max(voto_italiano1, voto_italiano2, voto_italiano3, voto_italiano4, voto_italiano5))
print('Voto più alto inglese: ', max(voto_inglese1, voto_inglese2, voto_inglese3, voto_inglese4, voto_inglese5))
print('Voto più alto storia: ', max(voto_storia1, voto_storia2, voto_storia3, voto_storia4, voto_storia5))
print('Voto più alto inglese: ', max(voto_inglese1, voto_inglese2, voto_inglese3, voto_inglese4, voto_inglese5))

print('Voto più alto di tutte le materie: ', max(max(voto_matematica1, voto_matematica2, voto_matematica3, voto_matematica4, voto_matematica5), max(voto_italiano1, voto_italiano2, voto_italiano3, voto_italiano4, voto_italiano5), max(voto_inglese1, voto_inglese2, voto_inglese3, voto_inglese4, voto_inglese5), max(voto_storia1, voto_storia2, voto_storia3, voto_storia4, voto_storia5)))

print('Voto più basso matematica: ', min(voto_matematica1, voto_matematica2, voto_matematica3, voto_matematica4, voto_matematica5))
print('Voto più basso italiano: ', min(voto_italiano1, voto_italiano2, voto_italiano3, voto_italiano4, voto_italiano5))
print('Voto più basso inglese: ', min(voto_inglese1, voto_inglese2, voto_inglese3, voto_inglese4, voto_inglese5))
print('Voto più basso storia: ',min(voto_storia1, voto_storia2, voto_storia3, voto_storia4, voto_storia5))

print('Voto più basso di tutte le materie: ', min(min(voto_matematica1, voto_matematica2, voto_matematica3, voto_matematica4, voto_matematica5), min(voto_italiano1, voto_italiano2, voto_italiano3, voto_italiano4, voto_italiano5), min(voto_inglese1, voto_inglese2, voto_inglese3, voto_inglese4, voto_inglese5), min(voto_storia1, voto_storia2, voto_storia3, voto_storia4, voto_storia5)))
