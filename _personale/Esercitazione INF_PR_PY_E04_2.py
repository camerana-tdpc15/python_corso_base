print('Inserire i seguenti dati e confermarli con invio:')
nome = input('Inserire nome alunno: ')
cognome = input('Inserire cognome alunno: ') 
classe = input('Inserire classe alunno: ')


materie = ['matematica', 'italiano', 'inglese', 'storia']

num_voti = 5 

voti_materia = []

for materia in materie:
    voti = []
    for idx in range(num_voti):
        voto = int(input(f'Inserire voto {materia} {idx+1} :'))
        voti.append(voto)
    voti_materia.append(voti)   


media_matematica = sum(voti_materia[0]) / len(voti_materia[0])    
media_italiano = sum(voti_materia[1]) / len(voti_materia[1])   
media_inglese = sum(voti_materia[2]) / len(voti_materia[2])    
media_storia = sum(voti_materia[3]) / len(voti_materia[3])  

media_globale = (media_matematica + media_italiano + media_inglese + media_storia) / len(voti_materia)


print(f'Risultati per l\'alunno {nome} {cognome} della classe {classe}:')
print(f'Media per Matematica: , {media_matematica:.2f}')
print(f'Media per Matematica: , {media_italiano:.2f}')
print(f'Media per Matematica: , {media_inglese:.2f}')
print(f'Media per Matematica: , {media_storia:.2f}')

print('Media Globale: ', media_globale)

voti_min = []
voti_max = []

for i in range(len(voti_materia)):
    voti_min.append(min(voti_materia[i]))


for i in range(len(voti_materia)):
    voti_max.append(max(voti_materia[i]))


print('Voto più basso di tutte le materie: ', min(voti_min))
print('Voto più alto di tutte le materie: ', max(voti_max))
