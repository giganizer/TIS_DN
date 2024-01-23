from math import log2
import numpy as np


def naloga3(vhod: list, n: int) -> tuple[list, str]:
    """
    Izvedemo dekodiranje binarnega niza `vhod`, zakodiranega 
    z razsirjenim Hammingovim kodom dolzine `n` in poslanega po zasumljenem kanalu.
    Nad `vhod` izracunamo vrednost `crc` po standardu CRC-16-CCITT.

    Parameters
    ----------
    vhod : list
        Sporocilo y, predstavljeno kot seznam bitov (stevil tipa int) 
    n : int
        Stevilo bitov v kodni zamenjavi
    
    Returns
    -------
    (izhod, crc) : tuple[list, str]
        izhod : list
            Odkodirano sporocilo y (seznam bitov - stevil tipa int)
        crc : str
            Vrednost CRC, izracunana nad `vhod`. Niz stirih znakov.
    """
    izhod = []
    crc = ''



    '''lastnosti koda'''
    n = n
    nh = n-1
    m = int(log2(n)) + 1
    mh = m - 1
    k = n - m

    '''obdelava vhoda'''
    #delitev na posamezne kodne besede
    vhodne_kodne_besede = []
    hamming_vhodne_besede = [] #odrezan sec-ded parity bit
    for i in range(0,len(vhod),n):
        vhodne_kodne_besede.append(vhod[i:i+n])
        hamming_vhodne_besede.append(vhod[i:i+n-1])

    '''dekodiranje s H(nh,k)'''
    #konstrukcija paritetne matrike
    matrika_h = None
    init_trap = True
    sindromski_slovar = {} #za translacijo sindromov kasneje
    for i in range(1,nh+1):
        if log2(i)%1 != 0:
            vector = np.fromiter(bin(i)[2:].zfill(mh), dtype=int) #stevilko (mesto/index) pretvorimo v binarni zapis in naredimo vektor iz stevk
            if(init_trap):
                init_trap = False
                matrika_h = vector.reshape((mh,1)) #s prvim stolpcem inicializiramo
            else:
                #polnimo matriko
                matrika_h = np.concatenate(
                    (
                    matrika_h,
                    vector.reshape((mh,1))
                    ),
                    axis=1
                    )
            
            sindromski_slovar[i] = len(sindromski_slovar)

    matrika_h = np.concatenate(
        (
        matrika_h,
        np.eye(mh,dtype=int)
        ),
        axis=1
    ) #na konec prilepimo se identiteto
    for i in range(mh,0,-1):
        sindromski_slovar[2**(i-1)] = len(sindromski_slovar)

    #izracun sindromov - naenkrat za vse y (hammingove)
    sindromi = np.matmul(np.array(hamming_vhodne_besede),matrika_h.transpose())
    sindromi = np.remainder(sindromi, 2)

    #obdelujemo vse kodne besede
    for i in range(len(vhodne_kodne_besede)):
        vkb = vhodne_kodne_besede[i]
        hkb = hamming_vhodne_besede[i]
        sindrom = sindromi[i]

        #preverimo paritetni bit

        #izracun paritete: XOR po bitih kodne besede
        p = 0
        for i in range(len(vkb)-1):
            p ^= vkb[i]

        #stanje paritetnega bita in sindroma
        if vkb[-1] ^ p == 1:
            if not np.all(sindrom == 0):
                #p = 1 in sindrom ni 0 -> enojna napaka
                sind_str = ""
                for bit in sindrom:
                    sind_str += str(bit)
                #popravimo napako
                hkb[sindromski_slovar[int(sind_str,2)]] ^= 1
                #hamming_vhodne_besede[i] = hkb #ni potrebno
        
        #izluscimo z
        z = hkb[0:k]
        #in damo na izhod
        izhod += z
        
            
    '''CRC'''

    #LFSR
    
    #init
    register = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lfsr_vhod = vhod[0]
    lfsr_pm = register[-1] ^ lfsr_vhod
    
    #ura tece
    for i in range(1,len(vhod)):
        lfsr_vhod = vhod[i]
        nov_register = [
            lfsr_pm,                #0
            register[0],            #1
            register[1],            #2
            register[2],            #3
            register[3],            #4
            register[4] ^ lfsr_pm,  #5
            register[5],            #6
            register[6],            #7
            register[7],            #8
            register[8],            #9
            register[9],            #10
            register[10],           #11
            register[11] ^ lfsr_pm, #12
            register[12],           #13
            register[13],           #14
            register[14]            #15
        ]
        register = nov_register
        lfsr_pm = lfsr_vhod ^ register[15]
    
    #vhoda je konec, se en pomik
    nov_register = [
        lfsr_pm,                #0
        register[0],            #1
        register[1],            #2
        register[2],            #3
        register[3],            #4
        register[4] ^ lfsr_pm,  #5
        register[5],            #6
        register[6],            #7
        register[7],            #8
        register[8],            #9
        register[9],            #10
        register[10],           #11
        register[11] ^ lfsr_pm, #12
        register[12],           #13
        register[13],           #14
        register[14]            #15
    ]
    register = nov_register
    
    #stanje v registru pretvorimo v sestnajstiski zapis
    crc_rez_str = ""
    for i in register[::-1]:
        crc_rez_str += str(i)
    crc = hex(int(crc_rez_str,2))[2:].zfill(4).upper()

    return (izhod, crc)