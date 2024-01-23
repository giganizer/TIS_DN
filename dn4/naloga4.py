import numpy as np
#from matplotlib import pyplot as plt

def naloga4(vhod: list, fs: int, t: float) -> str:
    """
    Poisce sekvenco pritiskov tipk v zvocnem zapisu.

    Parameters
    ----------
    vhod : list
        vhodni zvocni zapis 
    fs : int
        frekvenca vzorcenja
    t : float
        trajanje posameznega pritiska tipke v sekundah ter pavze za vsakim pritiskom tipke
    
    Returns
    -------
    izhod : str
         niz pritiskov tipk, ki se skriva v zvocnem zapisu
    """


    ## Obdelava vhoda
    t_vzorcev = int(fs * t) #dolzina enega znaka/tona v stevilu vzorcev
    vhodni_signali = [] #en signal je en ton/znak/pritisk
    for i in range(t_vzorcev,len(vhod)+1,t_vzorcev*2): #razdelimo na intervale posameznih tonov in preskocimo tisine
        vhodni_signali.append(vhod[i-t_vzorcev:i])
    ##
    
    ## Obdelava signalov
    # FFT
    for i in range(len(vhodni_signali)):
        vhodni_signali[i] = np.fft.fft(vhodni_signali[i])
    
    # Mocnostni spekter
    delta_f = fs / t_vzorcev
    moc_spektri = []
    for i in range(len(vhodni_signali)):
        P={}
        for j in range(len(vhodni_signali[i])):
            P[j*delta_f] = (abs(vhodni_signali[i][j])**2) / len(vhodni_signali[i])
        moc_spektri.append(P)

    izhod = ''

    # Prevedba v znak
    slovar_frek_znak = {
        697 : {1209 : "1", 1336 : "2", 1477 : "3"},
        770 : {1209 : "4", 1336 : "5", 1477 : "6"},
        852 : {1209 : "7", 1336 : "8", 1477 : "9"},
        941 : {1209 : "*", 1336 : "0", 1477 : "#"}
    }
    frekvence1 = (697, 770, 852, 941)
    frekvence2 = (1209, 1336, 1477)
    #ce naredimo slovar_frek_zank[<prva frekvenca>][<druga frekvenca>] dobimo ven znak, ki ga predstavlja kombinacija frekvenc (prva frekvenca je iz stolpca in druga iz vrstice)

    for P in moc_spektri:
        #za spekter vsakega znaka
        frek1 = frek2 = -1
        najvisje_vrednosti = sorted(list(set(np.partition(np.floor(list(P.values())),-10)[-10:])),reverse=True)
        
        for trenutna_najvisja in najvisje_vrednosti:
            if trenutna_najvisja <= 0: break
            if (frek1 != -1 and frek2 != -1): break
            for f1 in frekvence1:
                try:
                    if P[f1] >= trenutna_najvisja:
                        frek1 = f1
                        break
                except:
                    najv_manj = najm_vec = f1
                    while najv_manj not in P.keys():
                        najv_manj -= 1
                    while najm_vec not in P.keys():
                        najm_vec += 1
                    if (P[najm_vec]+P[najv_manj])/2 >= trenutna_najvisja:
                        frek1 = f1
                        break
                    
            for f2 in frekvence2:
                try:
                    if P[f2] >= trenutna_najvisja:
                        frek2 = f2
                        break
                except:
                    najv_manj = najm_vec = f2
                    while najv_manj not in P.keys():
                        najv_manj -= 1
                    while najm_vec not in P.keys():
                        najm_vec += 1
                    if (P[najm_vec]+P[najv_manj])/2 >= trenutna_najvisja:
                        frek2 = f2
                        break
                    '''if P[f2-1] >= trenutna_najvisja and P[f2+1] >= trenutna_najvisja:
                        frek2 = f2
                        break'''
        znak = ""
        try:
            znak = slovar_frek_znak[frek1][frek2]
        except:
            znak = ""
        izhod += znak



    '''#DEBUG#
    f_os = np.arange(0,t_vzorcev)*(fs/t_vzorcev)
    t_os = np.arange(0,t_vzorcev)
    # Narišimo grafe
    for i in range(int(len(vhod)/t_vzorcev)):
        figure, axis = plt.subplots(2,1)
        axis[0].plot(t_os, vhodni_signali[i])
        axis[0].set_title('Amplituda vs. čas')
        axis[0].set_xlabel('t [s]')

        axis[1].plot(f_os, moc_spektri[i])
        axis[1].set_title('Moč vs. frekvenca')
        axis[1].set_xlabel('f [Hz]')
        
        plt.show()
    ##'''

    
    return izhod