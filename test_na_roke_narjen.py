import sys
import json
from pathlib import Path
from timeit import default_timer as timer

# V tej datoteki se testira enakost po paru nasprotnih korakov (kodiranje in dekodiranje)
# tako da na koncu dobimo izvorne podatke. Primerjata se tudi slovarja po obeh postopkih, 
# ki morata seveda biti enaka. 


def naloga2(vhod: list, nacin: int) -> tuple[list, float]:
    """
    Izvedemo kodiranje ali dekodiranje z algoritmom LZW.
    Zacetni slovar vsebuje vse 8-bitne vrednosti (0-255). 
    Najvecja dolzina slovarja je 4096.

    Parameters
    ----------
    vhod : list
        Seznam vhodnih znakov: bodisi znaki abecede
        (ko kodiramo) bodisi kodne zamenjave 
        (ko dekodiramo).
    nacin : int 
        Stevilo, ki doloca nacin delovanja: 
            0: kodiramo ali
            1: dekodiramo.

    Returns
    -------
    (izhod, R) : tuple[list, float]
        izhod : list
            Ce je nacin = 0: "izhod" je kodiran "vhod"
            Ce je nacin = 1: "izhod" je dekodiran "vhod"
        R : float
            Kompresijsko razmerje
    """

    izhod = []
    R = float('nan')

    # Magic
    rez1_i, rez1_s = kodiranje_LZW(vhod) if nacin==0 else (dekodiranje_LZW(vhod))
    rez2_i, rez2_s = dekodiranje_LZW(rez1_i) if nacin==0 else (kodiranje_LZW(rez1_i))

    print("Enakost vhoda in izhoda po dveh korakih:",vhod==rez2_i)
    print("Enakost slovarjev:", list(rez1_s.keys())==list(rez2_s.values()) and list(rez1_s.values())==list(rez2_s.keys()))
    
    
    '''dolzina_vhod = len(vhod)*8 if nacin==0 else len(izhod)*8
    dolzina_izhod = len(izhod)*12 if nacin==0 else len(vhod)*12
    R = dolzina_vhod/dolzina_izhod'''

    return (izhod, R)

def zacetni_slovar_ASCII_8b(mode):
    # Naredi zacetni slovar - 8-bitna ASCII tabela
    # -------------------------------------------------------------
    # int mode: nacin - pove ali gradimo za kodirnik ali dekodirnik 
    #           0: kodirnik ;; 1: dekodirnik
    #           * ce delamo za kodirnik, bodo kljuci nizi in vrednosti stevilke (kodne zamenjave)
    #           * sicer (za dekodirnik), pa obratno
    slovar = {}
    for i in range(256):
        slovar[chr(i) if mode==0 else i] = i if mode==0 else chr(i)
    return slovar

def kodiranje_LZW(vhod: list):
    # Inicializacija zacetnega slovarja
    slovar = zacetni_slovar_ASCII_8b(0)
    naslednji_indeks = 256

    # Pomozne spremenljivke
    indeks_vhoda = 0
    izhod = []
    buffer = 0

    # Kodiranje
    N = ""
    while indeks_vhoda+buffer<len(vhod):
        z = vhod[indeks_vhoda + buffer]
        if N+z in slovar:
            N = N+z
            buffer += 1
        else:
            izhod.append(slovar[N])
            if(naslednji_indeks < 4096):
                # Velikost slovarja omejimo na 2^12
                slovar[N+z] = naslednji_indeks
                naslednji_indeks += 1
            N = z
            indeks_vhoda += buffer + 1
            buffer = 0
    izhod.append(slovar[N])

    # Vrnemo zaporedje kodnih zamenjav
    return (izhod,slovar)

def dekodiranje_LZW(vhod):
    # Inicializacija zacetnega slovarja
    slovar = zacetni_slovar_ASCII_8b(1)
    naslednji_indeks = 256

    # Pomozne spremenljivke
    indeks_vhoda = 0
    izhod = []

    # Dekodiranje
    k = vhod[indeks_vhoda]
    indeks_vhoda += 1
    N = slovar[k]
    izhod.append(N)
    K = N
    while indeks_vhoda < len(vhod):
        k = vhod[indeks_vhoda]
        indeks_vhoda += 1
        if k in slovar:
            N = slovar[k]
        else:
            N = K + K[0]
        izhod.append(N)
        if naslednji_indeks < 4096:
            slovar[naslednji_indeks] = K + N[0]
            naslednji_indeks += 1
        K = N

    return (list("".join(izhod)),slovar)


# Zahtevana natančnost izračunov za r
tol = 1e-6
# Zahtevana časovna omejitev (sekunde)
t_max = 30

case_dir = "lanskitesti"
for case_id in range(1,11):
    print("Test(lanski) {}".format(case_id))
    # Naložimo vhodne podatke in rešitev
    base_path = Path(__file__).parent
    file_path = base_path / str(case_dir) / (str(case_id) + '.json')
    json_file = open(file_path, 'r', encoding='utf8')
    data = json.load(json_file, strict=False)

    # Poženemo rešitev domače naloge in izmerimo izvajalni čas
    start = timer()
    izhod, r = naloga2(data['vhod'], data['nacin'])
    end = timer()
    t_elapsed = end - start

    # Ovrednotimo rešitev
    success_izhod = izhod == data['izhod']
    success_r = abs(r - data['r']) < tol
    success = int(success_izhod and success_r)
print()

case_dir = "primeri"
for case_id in range(1,4):
    print("Test(primeri) {}".format(case_id))
    # Naložimo vhodne podatke in rešitev
    base_path = Path(__file__).parent
    file_path = base_path / str(case_dir) / (str(case_id) + '.json')
    json_file = open(file_path, 'r', encoding='utf8')
    data = json.load(json_file, strict=False)

    # Poženemo rešitev domače naloge in izmerimo izvajalni čas
    start = timer()
    izhod, r = naloga2(data['vhod'], data['nacin'])
    end = timer()
    t_elapsed = end - start

    # Ovrednotimo rešitev
    success_izhod = izhod == data['izhod']
    success_r = abs(r - data['r']) < tol
    success = int(success_izhod and success_r)