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
    return (izhod, R)
