import sys

#mapa, kljuc: putanja, vrednost: sadrzaj na putanji
trenutni = '/'
mapa = {trenutni: ''}

for line in sys.stdin: #cita do EOF
    komanda = line.strip() #cisti beline sa krajeva

    if komanda.startswith('$ cd'):    #ako je komanda cd
        if komanda == '$ cd /':         #root 
            trenutni = '/'
        elif komanda == '$ cd ..':      #<---
            trenutni = trenutni.rsplit('/', 2)[0] + '/' 
        else:       #--->
            sta = '(d)' + komanda[5:]
            if mapa[trenutni].find(sta):
                mapa[trenutni] += sta + ' '
            trenutni = trenutni + komanda[5:] + '/'  #pravi novu putanju tako sto dodaje ime dir i / 

        #nakon sto smo skontali novu lokaciju za dir pravimo novi dir ako ne postoji
        if trenutni not in mapa:     
            mapa[trenutni] = ''

    #ako smo uradili ls, stavljamo ovu liniju da nam bude vrednos u mapi
    elif komanda.startswith('(d)') or komanda.startswith('(f)'):
        mapa[trenutni] = komanda
        reci = komanda.split()
        
        #izvuci iz linije sve (d)
        dir_lista = [token[3:] for token in reci if token.startswith("(d)")]       
 
        if len(dir_lista) > 0:
            for dir in dir_lista:
                pom = trenutni + dir + '/'
                if pom not in mapa:
                    mapa[pom] = ''


dir_br = len(mapa) - 1 #bez root
file_br = 0  

for m, n in mapa.items():
    # prebrojavam fajlove (f)  
    reci = n.split()
    fajlovi_lista = [token[3:] for token in reci if token.startswith("(f)")]
    file_br += len(fajlovi_lista)
    # print("kluc je ", m, " ----- njegov sadrzaj: ", n)


print(dir_br)
print(file_br)