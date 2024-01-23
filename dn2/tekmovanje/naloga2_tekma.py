import math


def naloga2_tekma(dat_vhod: str, dat_izhod: str, nacin: int) -> float:
    """
    Izvedemo kodiranje ali dekodiranje datoteke z algoritmom LZW
    in morebitnimi izboljsavami.

    Parameters
    ----------
    dat_vhod : str
        Pot do vhodne datoteke

    dat_izhod : str
        Pot do izhodne datoteke;
        ce datoteka se ne obstaja, jo ustvari; ce obstaja, jo povozi.
    
    nacin : int 
        Nacin delovanja: kodiramo (0) ali dekodiramo (1).

    Returns
    -------
    R : float
        Kompresijsko razmerje
    """
    R = float('nan')
    
        
    
    if nacin==0:
        podatki = None
        with open(dat_vhod,"rb") as file:
            podatki = file.read()
        rezultat = kodiranje_LZW(podatki)
        dolzina = math.ceil(rezultat[0].bit_length() / 8) #st bajtov za zapis
        with open(dat_izhod,"wb") as file:
            file.write(dolzina.to_bytes(1))
            for i in rezultat[1]:
                file.write(i.to_bytes(dolzina))
        R = (len(podatki) * 8) / ((len(rezultat[1])*8*dolzina)+8)
    
    if nacin==1:
        podatki = []
        dolzina = None
        with open(dat_vhod,"rb") as file:
            dolzina = int.from_bytes(file.read(1))
            while True:
                p = file.read(dolzina)
                if not p:
                    break
                podatki.append(int.from_bytes(p))
        rezultat = dekodiranje_LZW(podatki)
        with open(dat_izhod,"wb") as file:
            for i in rezultat:
                file.write(i.to_bytes(1))
        R = (len(rezultat) * 8) / ((len(podatki) * 8 * dolzina)+8)
        

    return R


def zacetni_slovar_8b(mode):
    slovar = {}
    for i in range(256):
        slovar[(i,) if mode==0 else i] = i if mode==0 else (i,)
    return slovar

def kodiranje_LZW(vhod: list):
    # Inicializacija zacetnega slovarja
    slovar = zacetni_slovar_8b(0)
    naslednji_indeks = 256

    # Pomozne spremenljivke
    indeks_vhoda = 0
    izhod = []
    buffer = 0
    header = []
    bit_slovar = 16

    # Kodiranje
    N = ()
    while indeks_vhoda+buffer<len(vhod):
        z = vhod[indeks_vhoda + buffer]
        if N+(z,) in slovar:
            N = N+(z,)
            buffer += 1
        else:
            izhod.append(slovar[N])
            slovar[N+(z,)] = naslednji_indeks
            naslednji_indeks += 1
            if(naslednji_indeks >= 2**bit_slovar):
                bit_slovar += 8
                header.append(len(izhod))
            N = (z,)
            indeks_vhoda += buffer + 1
            buffer = 0
    izhod.append(slovar[N])
    """ izhod.insert(0,len(header))
    for i in range(len(header)):
        izhod.insert(1+i,header[i]) """
    
    # Vrnemo zaporedje kodnih zamenjav
    return (len(slovar),izhod)

def dekodiranje_LZW(vhod):
    # Inicializacija zacetnega slovarja
    slovar = zacetni_slovar_8b(1)
    naslednji_indeks = 256

    # Pomozne spremenljivke
    indeks_vhoda = 0
    izhod = []

    # Dekodiranje
    k = vhod[indeks_vhoda]
    indeks_vhoda += 1
    N = slovar[k]
    for i in N:
        izhod.append(i)
    K = N
    while indeks_vhoda < len(vhod):
        k = vhod[indeks_vhoda]
        indeks_vhoda += 1
        if k in slovar:
            N = slovar[k]
        else:
            N = K + (K[0],)
        for i in N:
            izhod.append(i)
        slovar[naslednji_indeks] = K + (N[0],)
        naslednji_indeks += 1
        K = N

    # Izhod pretvorimo tako, da je vsak znak svoj element
    #return list("".join(izhod))
    
    return izhod