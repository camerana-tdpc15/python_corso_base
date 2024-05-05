# Creamo la clase studente

class Studente:
    def __init__(self, nome, cognome, classe, voti):
        self.nome = nome
        self.cognome = cognome
        self.classe = classe
        self.voti = {
            'matematica': voti[0],
            'italiano': voti[1],
            'inglese': voti[2],
            'storia': voti[3]
        }

# creamo le funzioni di calcolare
    def calcola_media_materia(self, materia):
        voti = self.voti.get(materia)
        if voti:
            return round(sum(voti) / len(voti), 2)
        else:
            return 0

    def calcola_media_globale(self):
        media_totale = sum(sum(voti) for voti in self.voti.values()) / len(self.voti)
        return round(media_totale)

    def voto_massimo(self):
        return max(voto for voti in self.voti.values() for voto in voti)

    def voto_minimo(self):
        return min(voto for voti in self.voti.values() for voto in voti)




# chiediamo l'imput al utente
def main():
    nome = input("Inserisci il nome dello studente: ")
    cognome = input("Inserisci il cognome dello studente: ")
    classe = input("Inserisci la classe dello studente: ")
    voti_matematica = [int(x) for x in input("Inserisci i voti di matematica separati da spazio: ").split()]
    voti_italiano = [int(x) for x in input("Inserisci i voti di italiano separati da spazio: ").split()]
    voti_inglese = [int(x) for x in input("Inserisci i voti di inglese separati da spazio: ").split()]
    voti_storia = [int(x) for x in input("Inserisci i voti di storia separati da spazio: ").split()]

    studente = Studente(nome, cognome, classe, [voti_matematica, voti_italiano, voti_inglese, voti_storia])

    

    # Stampiamo 
    print("Media di Matematica:", studente.calcola_media_materia('matematica'))
    print("Media di Italiano:", studente.calcola_media_materia('italiano'))
    print("Media di Inglese:", studente.calcola_media_materia('inglese'))
    print("Media di Storia:", studente.calcola_media_materia('storia'))
    print("Media Globale dell'Alunno:", studente.calcola_media_globale())
    print("Voto più alto tra tutte le materie:", studente.voto_massimo())
    print("Voto più basso tra tutte le materie:", studente.voto_minimo())


if __name__ == "__main__":
    main()