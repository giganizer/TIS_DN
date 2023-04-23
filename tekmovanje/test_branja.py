import os

files = os.listdir("C:/Users/zigab/OneDrive - Univerza v Ljubljani//2. letnik/TIS/dn2//tekmovanje//testni-nabor")

for f in files:
    #if(f=="kennedy.xls" or f=="ptt5" or f=="sum"): continue
    with open("./testni-nabor/"+f,"rb") as file:
        print("Datoteka:",f)
        data = file.read()
        print(type(data))
        print("Podatki:")
        print("---------------------------------------------------------")
        print(data[0:100])
        print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||")