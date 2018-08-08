from urllib.request import urlopen
from urllib.request import Request
from http import client
from pyquery import PyQuery
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1',
}
if __name__ == '__main__':
    firstPartLink = "https://www4.ceda.polimi.it/manifesti/manifesti/controller/ManifestoPublic.do?EVN_DETTAGLIO_RIGA_MANIFESTO=evento&k_corso_la=481&idGruppo=3753&idRiga=227360&codDescr="
    secondPartLink = "&aa=2018&lang=IT"

    link = "https://www4.ceda.polimi.it/manifesti/manifesti/controller/ManifestoPublic.do?k_corso_la=481&idGruppo=3753&idRiga=227360&codDescr=090914&aa=2018&lang=IT"

    fo = open("idCorsi.txt", "r")

    request = Request(link)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1')

    response = urlopen(request)
    html = response.read()

    pq = PyQuery(html)

    a = 17;

    while a < 50:

        table = pq('td.CenterBar').children(":nth-child("+str(a)+")")
        tableType = table.text()

        tableType = tableType.replace("Insegnamenti del Gruppo ", "")

        actualTable = pq('td.CenterBar').children(":nth-child("+str(a+1)+")").children(":nth-child(1)")

        corso = 2
        while corso <= len(actualTable.children()):

            linea = actualTable.children(":nth-child("+str(corso)+")")
            codice = linea.children(":nth-child(1)").text()
            nome = linea.children(":nth-child(4)").children(":nth-child(1)").text()
            semestre = linea.children(":nth-child(8)").text()
            crediti = linea.children(":nth-child(9)").text()

            if "\n" in crediti:
                crediti = crediti[0: crediti.index("\n")]

            if "--" in semestre:
                semestre = "1"

            print(codice+"_"+nome+"_"+ semestre+"_"+tableType+"_"+str(int(float(crediti))))
            corso = corso + 1

        a = a + 4

    print("089254_PROVA FINALE_2_NONE_20")