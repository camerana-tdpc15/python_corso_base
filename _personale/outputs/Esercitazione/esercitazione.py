Nome = input ("Inserisci Nome e cognome dell'allunno: ")

Classe = input ("Inserisci la classe dell' alunno: ")

Materie = {

'Matematica' :  [int(input('Inserisci 5 voti per la materia MATEMATICA:  Voto 1')),
                    int(input ('Inserisci 5 voti per la materia MATEMATICA:  Voto 2')),
                    int(input ('Inserisci 5 voti per la materia MATEMATICA:  Voto 3')),
                    int(input ('Inserisci 5 voti per la materia MATEMATICA:  Voto 4')),
                    int(input ('Inserisci 5 voti per la materia MATEMATICA:  Voto 5'))],

'Italiano' :  [int(input('Inserisci 5 voti per la materia ITALIANO:  Voto 1')),
                    int(input ('Inserisci 5 voti per la materia ITALIANO:  Voto 2')),
                    int(input ('Inserisci 5 voti per la materia ITALIANO:  Voto 3')),
                    int(input ('Inserisci 5 voti per la materia ITALIANO:  Voto 4')),
                    int(input ('Inserisci 5 voti per la materia ITALIANO:  Voto 5'))],

'Inglese' :  [int(input('Inserisci 5 voti per la materia INGLESE:  Voto 1')),
                    int(input ('Inserisci 5 voti per la materia INGLESE:  Voto 2')),
                    int(input ('Inserisci 5 voti per la materia INGLESE:  Voto 3')),
                    int(input ('Inserisci 5 voti per la materia INGLESE:  Voto 4')),
                    int(input ('Inserisci 5 voti per la materia INGLESE:  Voto 5'))],

'Storia' :  [int(input('Inserisci 5 voti per la materia STORIA:  Voto 1')),
                    int(input ('Inserisci 5 voti per la materia STORIA:  Voto 2')),
                    int(input ('Inserisci 5 voti per la materia STORIA:  Voto 3')),
                    int(input ('Inserisci 5 voti per la materia STORIA:  Voto 4')),
                    int(input ('Inserisci 5 voti per la materia STORIA:  Voto 5'))],

}

Media_Matematica = sum(Materie['Matematica'])/len(Materie['Matematica'])
Media_Italiano = sum(Materie['Italiano'])/len(Materie['Italiano'])
Media_Inglese = sum(Materie['Inglese'])/len(Materie['Inglese'])
Media_Storia = sum(Materie['Storia'])/len(Materie['Storia'])

Medie = [Media_Matematica, Media_Italiano, Media_Inglese, Media_Storia]
Media_Globale = int(sum(Medie) / len(Medie))


Voto_Alto =  max(Materie['Matematica'] + Materie['Italiano'] + Materie['Inglese'] + Materie['Storia'])

Voto_Basso=  min(Materie['Matematica'] + Materie['Italiano'] + Materie['Inglese'] + Materie['Storia'])

print(f"Risultati per l' alunno {Nome} della classe {Classe}:")

for x in Materie :
    print(f"Media per {x} : {sum(Materie[x])/len(Materie[x])}")

    
print(f"Media Globale dell' alunno : {Media_Globale}" )

print(f"Il voto più Alto dell' Alunno: {Voto_Alto}")

print(f"Il voto più Basso dell' Alunno: {Voto_Basso}")
