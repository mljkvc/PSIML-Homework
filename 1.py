import sys

def brojac_fajlova(mapa):
    file_br = 0  
    for m, n in mapa.items():
        # prebrojavam fajlove (f)  
        
        reci = n.split()
        fajlovi_lista = [token for token in reci if token.startswith("(f)")]
        file_br += len(fajlovi_lista)
    print(file_br)


def sort_dir(mapa):
    for m, n in sorted(mapa.items()):
        x = sorted(mapa[m].split())
        n = ''
        for i in x:
            n += i + ' '
        mapa[m] = n
    return mapa


def ispis_dir(mapa):
    #ispis dir
    for m, n in sorted(mapa.items()):
        print("key:", m, " -----: values:", n)
    print()

def ispis(mapa, putanja, dir_name, uvecanje):
    print('|-' * uvecanje + dir_name)
    for lista in mapa[putanja].split():
        if lista.startswith('(d)'):
            ispis(mapa, putanja + lista[3:] + '/', lista[3:] + '/', uvecanje + 1)
        elif lista.startswith('(f)'):
            print('|-' * (uvecanje + 1) + lista[3:])
        else:
            print('|-' * (uvecanje + 1) + lista)


file_lista = []
poslednja_putanja = '/'
def rm(mapa, putanja):
    global poslednja_putanja
    for lista in mapa[putanja].split():
        if lista.startswith('(d)'):
            rm(mapa, putanja + lista[3:] + '/')
        elif lista.startswith('(f)'):
            if lista[3:] not in file_lista:
                # print('prvi put u', putanja, "nasao sam", lista[3:])
                file_lista.append(lista[3:])
            else:
                # print('putanja mi je', putanja, "nasao sam", lista[3:])

                #prvi put krece od root
                if poslednja_putanja == '/':
                    cd_lista = putanja.split('/')
                    print('$ cd /')
                    for i in cd_lista[1:-1]:
                        print('$ cd ' + i)
                    print('$ rm ' + lista[3:])
                #else koji ispisuje ako nije prvi put
                else:
                    pr_lista = poslednja_putanja.split('/')[1:-1]
                    tr_lista = putanja.split('/')[1:-1]
                    # print('trnutna je', tr_lista)
                    # print('prethod je', pr_lista)
                    
                    #ovde idem cd /dir
                    if len(pr_lista) < len(tr_lista):
                        pass
                    else:
                        #ovde treba cd .. 
                        # print(len(pr_lista), len(tr_lista))
                        if (len(pr_lista) - len(tr_lista)) <= len(tr_lista) + 1:
                            for i in range(len(pr_lista) - len(tr_lista)):
                                print('$ cd ..')
                            print('$ rm', lista[3:])
                        #ovde treba cd /        
                        else:
                            print('$ cd /')
                            for i in tr_lista[1:-1]:
                                print('$ cd ' + i)
                            print('$ rm ' + lista[3:])
                            # -------->
                # print()    

                poslednja_putanja = putanja



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
    elif komanda.startswith('('):
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
rm(pom_mapa, '/')

# for m, n in sorted(mapa.items):
#     print