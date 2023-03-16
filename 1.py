import sys

def brojac_fajlova(mapa):
    file_br = 0  
    for m, n in mapa.items():
        # prebrojavam fajlove (f)  
        
        reci = n.split()
        fajlovi_lista = [token[3:] for token in reci if token.startswith("(f)")]
        file_br += len(fajlovi_lista)
    print(file_br)


def sort_dir(mapa):
    for m, n in sorted(mapa.items(), reverse = False):
        x = sorted(mapa[m].split())
        n = ''
        for i in x:
            n += i + ' '
        mapa[m] = n
    return mapa


def ispis_dir(mapa):
    #ispis dir
    for m, n in sorted(mapa.items(), reverse = False):
        print("key:", m, " -----: values:", n)
    print()

def ispis(mapa, putanja, dir_name, uvecanje):
    print('|-' * uvecanje + dir_name)
    for lista in mapa[putanja].split():
        if lista.startswith('(d)'):
            # print(lista)
            # uvecanje += 1
            ispis(mapa, putanja + lista[3:] + '/', lista[3:] + '/', uvecanje + 1)
        elif lista.startswith('(f)'):
            print('|-' * (uvecanje + 1) + lista[3:])
        else:
            print('|-' * (uvecanje + 1) + lista)


file_lista = []
def rm(mapa, putanja, dir_name):
    for lista in mapa[putanja].split():
        if lista.startswith('(d)'):
            rm(mapa, putanja + lista[3:] + '/', lista[3:] + '/')
        elif lista.startswith('(f)'):
            if lista[3:] not in file_lista:
                file_lista.append(lista[3:])
            else:
                cd_lista = putanja.split('/')
                print('$ cd /')
                for i in cd_lista[1:-1]:
                    print('$ cd ' + i)
                print('$ rm ' + lista[3:])



#mapa, kljuc: putanja, vrednost: sadrzaj na putanji
trenutni = '/'
mapa = {trenutni: '?'}

for line in sys.stdin: #cita do EOF
    komanda = line.strip() #cisti beline sa krajeva

    if komanda.startswith('$ cd'):    #ako je komanda cd
        if komanda == '$ cd /':         #root 
            trenutni = '/'
        elif komanda == '$ cd ..':      #<---
            trenutni = trenutni.rsplit('/', 2)[0] + '/' 
        else:       #--->
            sta = '(d)' + komanda[5:].strip()
            if sta not in mapa[trenutni]:
                mapa[trenutni] += ' ' + sta
            trenutni = trenutni + komanda[5:] + '/'  #pravi novu putanju tako sto dodaje ime dir i / 

        #novi kljuc sa putanjom ako vec ne postoji
        if trenutni not in mapa:     
            mapa[trenutni] = '?'

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
                    mapa[pom] = '?'
    #ls komanda
    elif komanda.startswith('$ ls'):
        mapa[trenutni] = ''

dir_br = len(mapa) - 1 #bez root
print(dir_br)
brojac_fajlova(mapa)

# ispis_dir(mapa)

pom_mapa = sort_dir(mapa)
# ispis_dir(pom_mapa)

ispis(pom_mapa, '/', '/', 0)
rm(pom_mapa, '/', '/')

# for m, n in sorted(mapa.items):
#     print