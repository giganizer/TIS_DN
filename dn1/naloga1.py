import json
from math import log2
from collections import Counter

class vozlisce:
    def __init__(self):
        self.sinovi = []
        self.entropija = 'inf'
        self.verjetnost = 'inf'
        self.steviloR = 0 #stevilo razredov (instanc) ki se pojavijo v tem listu
        self.znacilnice = [] #znacilnice, ki smo jih izbrali na poti do tega lista
        self.izbire = [] #izbire vrednosti znacilnic, ki smo jih izbrali na poti do tega lista
        self.razredi = {} #stevilo pojavitev vrednosti razreda za to izbiro
        self.nivo = 1 #nivo v drevesu; koren je 1
        self.rezultat = "" #rezultat, ki nam ga napove ta pot
        self.izvor = None #oce


    def poracun(self):
        #iz nabora razredov izracuna entropijo
        #in nastavi rezultat glede na najbolj pojavljen razred
        vseh = sum(self.razredi.values())
        if vseh == 0:
            self.entropija = 0
            self.rezultat = ""
        else:
            verjetnosti = []
            max = list(self.razredi.keys())[0]
            for (k, v) in self.razredi.items():
                verjetnosti.append(v/vseh)
                if self.razredi[k] > self.razredi[max]:
                    max = k
                '''elif self.razredi[k] == self.razredi[max]:
                    max = k if k<max else max'''
            self.entropija = izrEntropija(verjetnosti)
            self.rezultat = max


def izrLastnaInformacija(verj):
    return -log2(verj)

def izrEntropija(verjetnosti):
    rez = 0
    for i in range(len(verjetnosti)):
        rez += verjetnosti[i]*izrLastnaInformacija(verjetnosti[i])
    return rez

def stetje(seznam):
    #presteje stevilo pojavitev razlicnih vrednosti
    #in vrne seznam (list) verjetnosti
    pojavitve = {}
    for i in seznam:
        if i in pojavitve.keys():
            pojavitve[i] += 1
        else:
            pojavitve[i] = 1
    
    #pojavitve spremenimo v verjetnosti
    verjetnosti = []
    for v in pojavitve.values():
        verjetnosti.append(v/len(seznam))
    
    #vrnemo seznam verjetnosti
    return verjetnosti


def korak(koreni,znacilnice,razredi,porabljeneZnacilnice):
    razredi_list = razredi
    dolzina = len(razredi_list)
    potencialna_drevesa = {} 
    for ime in znacilnice:
        if ime in porabljeneZnacilnice: continue
        potencialna_drevesa[ime] = {
                                        "listi" : [],
                                        "H" : 0, #skupna pogojna entropija
                                        "str" : 0 #stevilo vseh razredov 
                                    }

    vsi_novi_listi = []
    for (imeZ, vrednostiZ) in znacilnice.items():

        #preskocimo ze izbrane/uporabljene znacilnice
        if imeZ in porabljeneZnacilnice: continue

        #poiscemo vse razlicne vrednosti znacilnice
        nz_nabor = []
        for nz in vrednostiZ:
            if nz not in nz_nabor:
                nz_nabor.append(nz)

        for koren in koreni:
            
            #za vsako razlicno vrednost znacilnice naredimo nov list
            novi_listi = []
            for nz in nz_nabor:
                nov_sin = vozlisce()
                nov_sin.znacilnice = koren.znacilnice + [imeZ]
                nov_sin.izbire = koren.izbire + [nz]
                nov_sin.nivo = koren.nivo + 1
                nov_sin.izvor = koren
                #potencialna_drevesa[imeZ]["listi"].append(nov_sin)
                novi_listi.append(nov_sin)
            
            #sprehod cez stolpce izvorne tabele, pri vsakem stolpcu pogledamo za vsak nov list ujemanje 
            #po vseh izbirah - ce se ujema, stejemo razred v list
            for i in range(dolzina):

                for lst in novi_listi:
                    ujemanje = True
                    for j in range(len(lst.znacilnice)):

                        if znacilnice[lst.znacilnice[j]][i] != lst.izbire[j]:
                            ujemanje = False
                            break
                        
                    if ujemanje:
                        if razredi_list[i] in lst.razredi:
                            lst.razredi[razredi_list[i]] += 1
                        else:
                            lst.razredi[razredi_list[i]] = 1
                        break
            
            #izracun entropije novih listov
            for lst in novi_listi:
                lst.poracun()
            
            vsi_novi_listi += novi_listi
            potencialna_drevesa[imeZ]["listi"] += novi_listi

    #izračun pogojnih entropij
    for (znacilnica, podatki) in potencialna_drevesa.items():
        for lst in podatki["listi"]:
            for v in lst.razredi.values():
                lst.steviloR += v
            podatki["str"] += lst.steviloR
        for lst in podatki["listi"]:
            lst.verjetnost = lst.steviloR/podatki["str"]
            podatki["H"] += lst.verjetnost*lst.entropija
    
    #izberemo drevo/vejitev/znacilnico z najnizjo entropijo
    izbrana_znacilnica = list(potencialna_drevesa.keys())[0]
    for k in potencialna_drevesa:
        if potencialna_drevesa[k]["H"] < potencialna_drevesa[izbrana_znacilnica]["H"]:
            izbrana_znacilnica = k
    #for lst in potencialna_drevesa[izbrana_znacilnica]["listi"]:
    #    lst.izvor.sinovi.append(lst)
    return (izbrana_znacilnica, potencialna_drevesa[izbrana_znacilnica])     

def naloga1(znacilnice, razredi, koraki):

    entropija = float('inf')
    tocnost = float('inf')

    ##konstrukcija korena
    koren = vozlisce()
    koren.verjetnost = 1
    for r in razredi:
        if r in koren.razredi.keys():
            koren.razredi[r] += 1
        else:
            koren.razredi[r] = 1
    koren.poracun()
    koren.izvor = "root"
    

    ##magic: entropija in gradnja drevesa
    porabljene_znacilnice = []
    vozlisca = [koren]
    for iteracija in range(koraki):
        retval = korak(vozlisca,znacilnice,razredi,porabljene_znacilnice)
        porabljene_znacilnice += [retval[0]]
        entropija = retval[1]["H"]
        for lst in retval[1]["listi"]:
            lst.izvor.sinovi.append(lst)
        vozlisca = retval[1]["listi"]
    ###

    ##tocnost
    #polnjenje tabele napovedi
    napovedani_razredi = []
    for i in range(len(razredi)):
        voz = koren
        while len(voz.sinovi) != 0:
            znac = voz.sinovi[0].znacilnice[-1]
            for sin in voz.sinovi:
                if sin.izbire[-1] == znacilnice[znac][i]:
                    voz = sin
                    break
        napovedani_razredi.append(voz.rezultat)
    #primerjava
    tocnost = 0
    for i in range(len(razredi)):
        if razredi[i] == napovedani_razredi[i]: tocnost += 1
    tocnost /= len(razredi)
    ###


    return (entropija, tocnost)

#print(entropija([0.4,0.6]))

# ghetto test
'''
a = {
    "podatki":
    {
        "ime": "Kolesarjenje",
        "znacilnice":
        {
            "Nebo" : ["j", "j", "j", "j", "j", "j", "o", "o", "o", "o"],
            "Temp" : ["h", "h", "t", "h", "h", "t", "t", "t", "t", "t"],
            "Veter": ["v", "v", "v", "m", "m", "m", "v", "v", "m", "m"]
        },
        "razredi":
        {
            "Kolo" : ["d", "n", "d", "d", "d", "d", "n", "n", "d", "n"]
        } 
    },
    "koraki": 1,
    "entropija": 0.71452,
    "tocnost": 0.8000
    }
print(naloga1(a["podatki"]["znacilnice"],a["podatki"]["razredi"]["Kolo"],a["koraki"]))
'''