myList = ["mele", "banane","ciliegie","prugne"]    # questa e una lista

#print(type(myList))

thiList = list (("mele", "banane","ciliegie","prugne"))   # cosi construiamo una lista

#print (thiList)S

#print (thiList [2]) #stampo il 3 elem---ricorda che parte da 0 = mele

#print (thiList [-1])    #il negativ stampa dalla fine -1 = prugne


lista01 = list(("mele", 10, "banane", 50, 150, "ciliegie",182.5873, "prugne"))

#print(len (lista01))    # stampa in num di elem contenuti in una lista 

#print (lista01[ -1])    # stampa prugne--- il -1 E INCLUSO

#print (lista01[-4 : -1])    #stampa [150, 'ciliegie', 182.5873]---   -4 e INCLISO  -1 NON E INCLUSO

#print (lista01[-4 : -1 : 2])    #stampa [150, 182.5873]--- il 2 indica il passo


#if 10 in lista01:
#    print ('OK')--- IN  e  una PAROLA CHIAVE 

#lista01 [2] = 184
#print(lista01)--- sostituisce l'elemento 2=10 cu 184





#print (len(lista01))
#print (lista01)
#lista01 [2 : 7] = "vodka" , "5824"  # lista diventa ['mele', 10, 'vodka', '5824', 'prugne']
#print(lista01)                      #ho eliminato l'indice 2,3,4,5,6 e inserito i nuovi valori
#lista01.insert(2, "banane")
#print (lista01) #ho inserito un oggetto nella lista al indice 2----NON SI POSSONO INSERIRE PIU OGGETTI IN CONTEMPORANEA??????

