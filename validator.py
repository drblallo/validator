from enum import Enum
from argparse import ArgumentParser

requiredTaba = 45
requiredTabbPlusTaba = 55
requiredInt1 = 15
maxCreditDifference = 20
totalCredit = 120


firstPartLink = "https://www4.ceda.polimi.it/manifesti/manifesti/controller/ManifestoPublic.do?EVN_DETTAGLIO_RIGA_MANIFESTO=evento&k_corso_la=481&idGruppo=3753&idRiga=227360&codDescr="
secondPartLink = "&aa=2018&lang=IT"

class Corso:
    def __init__(self):
        self.codice = ""
        self.crediti = 0
        self.nome = ""
        self.tipo = "NONE"
        self.semestre = 1
        self.anno = 1

    def clone(self):
        corso = Corso()
        corso.codice = self.codice
        corso.crediti = self.crediti
        corso.nome = self.nome
        corso.anno = self.anno
        corso.semestre = self.semestre
        corso.tipo = self.tipo
        return corso

class PianoStudi:

    def __init__(self):
        self.corsi = []

    def addCorso(self, corso):
        self.corsi.append(corso)

    def totaleCrediti(self):
        count = 0;
        for corso in self.corsi:
            count = count + corso.crediti;
        return count

    def totaleTipo(self, tipo):
        count = 0;
        for corso in self.corsi:
            if corso.tipo == tipo:
                count = count + corso.crediti
        return count

    def totaleInt1(self):
        return self.totaleTipo("INT1")

    def totaleTaba(self):
        return self.totaleTipo("TABA")

    def totaleTabb(self):
        return self.totaleTipo("TABB")

    def tabaValid(self):
        return self.totaleTaba() >= requiredTaba

    def tabValid(self):
        return self.tabaValid() and self.totaleTaba() + self.totaleTabb() >= requiredTabbPlusTaba

    def int1Valid(self):
        return self.totaleInt1() >= requiredInt1

    def isDotValid(self):
        count = 0;
        for corso in self.corsi:
            if corso.tipo == "DOT":
                count = count + 1
        return count <= 1

    def getCourseNotInOther(self, other):
        differentCourses = []
        for corso in self.corsi:
            if not corso in self.corsi:
                differentCourses.append(corso)
        return differentCourses

    def getCreditsDifference(self, other):
        courses = self.getCourseNotInOther(other)
        a = 0
        for corso in courses:
            a = a + corso.crediti
        return a

    def totaleCreditiSemestre(self, anno, semestre):
        count = 0
        for corso in self.corsi:
            if (corso.anno == anno) and corso.semestre == semestre:
                count = count + corso.crediti

        return str(count)


def loadPiano(fileName, corsi):
    fo = open(fileName, "r")
    piano = PianoStudi()
    year = 1

    numeroLinea = 0
    for line in fo.readlines():
        numeroLinea = numeroLinea + 1
        if line.startswith("-"):
            year = year + 1
            continue

        if line.startswith("#") or len(line) == 0   or line.startswith("\n"):
            continue

        splitted = line.split(" ")
        if len(splitted) < 1:
            print("Linea Malformata: "+ numeroLinea + " " + line+" file: "+fileName)
            exit(-1)

        if not splitted[0].replace("\n", "") in corsi:
        #if corsi[splitted[0].replace("\n", "")] == None:
            print("Corso sconosiuto: "+ splitted[0]+ " Linea: (" +str(numeroLinea)+") "+ line + " file: "+fileName)
            exit(-1)

        corso = corsi[splitted[0].replace("\n", "")].clone()
        corso.anno = year
        piano.addCorso(corso)

    return piano


def loadCorsi(fileName):
    fo = open(fileName, "r")
    corsi = {}

    numeroLinea = 0
    for line in fo.readlines():
        numeroLinea = numeroLinea + 1

        if line.startswith("#") or len(line) == 0 or line.startswith("\n"):
            continue

        splitted = line.split("_")
        if len(splitted) != 5:
            print("Linea Malformata: ("+ str(numeroLinea) + ") " + line+" file: "+fileName)
            exit(-1)

        corso = Corso()
        corso.codice = splitted[0].replace("\n", "")
        corso.nome = splitted[1]
        corso.semestre = int(splitted[2])
        corso.tipo = splitted[3]
        corso.crediti = int(splitted[4])

        corsi[corso.codice] = corso
    return corsi

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input",
                    help="Input File", metavar="FILE", default="user.txt")
    parser.add_argument("-c", "--compare",
                    action="store_true", dest="compare", default=False,
                    help="Compara due piani")
    parser.add_argument("-s", "--simple",
                    action="store_true", dest="simple", default=False,
                    help="Mostra solo i corsi")
    parser.add_argument("-l", "--link",
                        action="store_true", dest="link", default=False,
                        help="Mostra i link alle pagine dei corsi")

    args = parser.parse_args()



    corsi = loadCorsi("corsi.txt")
    base = loadPiano("base.txt", corsi)
    user = loadPiano(args.input, corsi)

    if not args.simple:
        print("# usa # per aggiungere un commento, - per dividire i semestri")

    if not user.isDotValid():
        print("#CI SONO TROPPI CORSI DOT")
    if not args.simple:
        print("#int1:" + str(user.totaleTipo("DOT")) + "/1")

    if not user.tabaValid():
        print("#NON CI SONO ABBASTANZA CORSI TABA")

    if not args.simple:
        print("#taba:" + str(user.totaleTaba()) + "/" + str(requiredTaba))

    if not user.tabValid():
        print("#NON CI SONO ABBASTANZA CORSI TABA E/O TABB")

    if not args.simple:
        print("#tabb + taba:" + str(user.totaleTaba() + user.totaleTabb())+"/"+str(requiredTabbPlusTaba))

    if user.totaleCrediti() < totalCredit:
        print("#NON CI SONO ABBASTANZA CREDITI")

    if not args.simple:
        print("#int1:" + str(user.totaleCrediti()) + "/" + str(totalCredit))

    if not user.int1Valid():
        print ("#NON CI SONO ABBSATNZA CORSI INT1")

    if not args.simple:
        print("#int1:" + str(user.totaleInt1()) + "/" + str(requiredInt1))

    if base.getCreditsDifference(user):
        print("#IL PIANO HA TROPPI CREDITI DIVERSI DA QUELLO BASE")

    print("\n#PIANO DI STUDI INGEGNERIA INFORMATICA: ")





    for year in range(1, 3):
        for semester in range(1, 3):


            if year == 2 and semester == 1:
                print("-anno: " + str(year) + ", semestre: " + str(semester)+ " "+user.totaleCreditiSemestre(year, semester) +" crediti")
            else:
                print("#anno: " + str(year) + ", semestre: " + str(semester)+ " "+user.totaleCreditiSemestre(year, semester) +" crediti")
            for corso in user.corsi:
                if corso.semestre == semester and corso.anno == year:
                    print(corso.codice + " " + corso.tipo + " " + corso.nome + " " + str(corso.crediti))
                    if args.link:
                        print("# "+firstPartLink+corso.codice+secondPartLink)
            print("")


