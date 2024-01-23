import sys
import naloga2_tekma
import os

files = os.listdir("C:/Users/Ziga/OneDrive - Univerza v Ljubljani/2. letnik/TIS/dn2/tekmovanje/testni-nabor/")

for f in files:
    print("Datoteka:",f)    
    print(naloga2_tekma.naloga2_tekma("C:/Users/Ziga/OneDrive - Univerza v Ljubljani/2. letnik/TIS/dn2/tekmovanje/testni-nabor/"+f,"C:/Users/Ziga/OneDrive - Univerza v Ljubljani/2. letnik/TIS/dn2/tekmovanje/testiranje/"+f+".kodirano",0))
    print(naloga2_tekma.naloga2_tekma("C:/Users/Ziga/OneDrive - Univerza v Ljubljani/2. letnik/TIS/dn2/tekmovanje/testiranje/"+f+".kodirano","C:/Users/Ziga/OneDrive - Univerza v Ljubljani/2. letnik/TIS/dn2/tekmovanje/testiranje/"+f+".dekodirano",1))