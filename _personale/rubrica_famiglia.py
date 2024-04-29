# 1. Crea un dizionario dove le chiavi sono i nomi dei membri della famiglia (nonni, zii, genitori, figli) 
# e i valori sono altri dizionari contenenti informazioni anagrafiche (telefono, indirizzo, data di nascita) del rispettivo parente.

# 2. Aggiungere nuovi membri della famiglia alla rubrica.
# 3. Cercare un parente per nome e stampare i suoi dati.
# 4. Visualizzare l'intera rubrica.

# creo dizionario rubrica
rubrica = {}

# creo funzione 'Aggiungi parente
def aggiungi_parente (nome, informazioni):
    informazioni = {
    nome : input('inserisce il grado di parentela e il nome '),     
    telefono : input('inserisce il numero di telefono '),
    indirizzo : input('inserisce l\'indirizzo '),
    anno_nascita : input('inserisce anno di nascita ')
}


    rubrica[nome] = informazioni
    print(f"Parente {nome} aggiunto alla rubrica")
    
  # creo dizionario 'informazioni con input dell'utente  


aggiungi_parente("Mario Rossi")

print(rubrica[nome]["telefono"])
