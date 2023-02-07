# pogram ksiegowy - magazyn - z wykorzystaniem plikow
historia_dl = 0
historia = {}
magazyn = {}
magazyn_add = []
magazyn_mv = []

def nadpisz_saldo(val):
    with open('saldo.txt', 'w') as sal:
        sal.write(f'{val}\n')
    return

def wczytaj_historie():
    with open('log.txt') as log:
        pos = 0
        historia.clear()
        for i in log:
            if pos == 0:
                key = int(i.strip())
                pos += 1
            elif pos == 1:
                opis1 = i.strip()
                pos += 1
            elif pos == 2:
                opis2 = i.strip()
                pos += 1
            elif pos == 3:
                opis3 = i.strip()
                pos += 1
            elif pos == 4:
                opis4 = i.strip()
                pos = 0
                historia[key] = [opis1, opis2, opis3, opis4]
    return

def zapisz_historie(id,oper,par1,par2,par3):
    with open('log.txt', 'a') as log:
        log.write(f'{id}\n')
        log.write(f'{oper}\n')
        log.write(f'{par1}\n')
        log.write(f'{par2}\n')
        log.write(f'{par3}\n')
    return

def wczytaj_magazyn():
    with open('mag.txt') as mag:
        poz = 0
        magazyn.clear()
        for i in mag:
            if poz == 0:
                kex = i.strip()
                poz += 1
            elif poz == 1:
                ops1 = i.strip()
                poz += 1
            elif poz == 2:
                ops2 = float(i.strip())
                poz += 1
            elif poz == 3:
                ops3 = int(i.strip())
                poz = 0
                magazyn[kex] = [ops1, ops2, ops3]
    return

def nadpisz_magazyn():
    f = open('mag.txt', 'w')
    f.close()
    for i in magazyn:
        id = i
        prod = magazyn[i][0]
        cena = magazyn[i][1]
        ilosc = magazyn[i][2]
        with open('mag.txt', 'a') as mag:
            mag.write(f'{id}\n')
            mag.write(f'{prod}\n')
            mag.write(f'{cena}\n')
            mag.write(f'{ilosc}\n')
    return

dostepne_operacje = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
# pobieramy i weryfikujemy dostepnosc operacji
while True:
    while True:
        print(f"Dostepne operacje: {dostepne_operacje}")
        operacja = input("Podaj operacje: ")
        if operacja in dostepne_operacje:
            break
        else:
            print("Operacja z poza listy dostępnych operacji")
# wykonujemy zadane operacje
    with open('saldo.txt') as sal:
        konto = float(sal.readline().strip())
    if operacja == "saldo":
        saldo_add = input("Podaj kwote do dodania(odjęcia) do konta <int>/<float>: ")
        if saldo_add != '':
            if konto + float(saldo_add) < 0:
                print("Operacja niemozliwa do wykonania")
            else:
                wczytaj_historie()
                konto += float(saldo_add)
                nadpisz_saldo(konto)
                historia_dl = len(historia) + 1
                zapisz_historie(historia_dl,'saldo',konto,'-','-')
        else:
            print("Podano pustą wartosc - operacja niemozliwa do wykonania")

    elif operacja == "sprzedaz":
        nazwa = input("Podaj nazwe produktu: ")
        cena = input("Podaj cene produktu<int><float>: ")
        ilosc = input("Podaj ilosc produktow<int>: ")
        # weryfikujemy poprawnosc zlecenia
        if nazwa == '' or cena == '' or ilosc == '':
            print("Operacja niemozliwa - podano pusta wartosc")
        else:
            # sprawdzamy poprawnosc ceny i ilosci
            noint = 0
            for y in cena:
                if y not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'):
                    noint = 1
            for z in ilosc:
                if z not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                    noint = 1
            if noint == 1 or cena == '0' or ilosc == '0':
                print("Przynajmniej  jedna podana wartosc jest niepoprawna")
            else:
                ilosc = int(ilosc)
                # jako identyfikatora uzyjemy sumy nazwy i ceny - bo mozemy miec te same produkty o roznych cenach
                magazyn_mv = nazwa + cena, nazwa, float(cena), ilosc
                # sprawdzamy czy mamy taki produkt
                wczytaj_magazyn()
                if magazyn_mv[0] not in magazyn:
                    print("Produktu o takiej nazwie i cenie niema w magazynie")
                else:
                    # sprawdzamy czy mamy wystarczajaca ilosc sztuk
                    if ilosc > magazyn[magazyn_mv[0]][2]:
                        print(f"Dostepna ilosc produktu jest mniejsza i wynosi: {magazyn[magazyn_mv[0]][2]}")
                    else:
                        # jesli zlecenie zabiera wszystkie sztuki produktu usuwamy produkt z magazynu
                        if ilosc == magazyn[magazyn_mv[0]][2]:
                            del magazyn[magazyn_mv[0]]
                            konto += magazyn_mv[2] * magazyn_mv[3]
                            nadpisz_saldo(konto)
                            nadpisz_magazyn()
                            print(f"Sprzedano caly zapas produktu o nazwie: {magazyn_mv[1]} i cenie: {magazyn_mv[2]}")
                            wczytaj_historie()
                            historia_dl = len(historia) + 1
                            cef = float(cena)
                            zapisz_historie(historia_dl, 'sprzedaz', nazwa, cef, ilosc)
                        # jesli taki produkt istnieje modyfikujemy tylko ilosc sztuk
                        else:
                            x = magazyn[magazyn_mv[0]][1]
                            y = magazyn[magazyn_mv[0]][2] - ilosc
                            magazyn[magazyn_mv[0]] = [nazwa, x, y]
                            konto += magazyn_mv[2] * magazyn_mv[3]
                            nadpisz_saldo(konto)
                            nadpisz_magazyn()
                            print(f"Zmodyfikowano ilosc produktu o nazwie: {magazyn_mv[1]} i cenie: {magazyn_mv[2]} "
                                  f"obecny stan to {magazyn[magazyn_mv[0]][2]}")
                            wczytaj_historie()
                            historia_dl = len(historia) + 1
                            cef = float(cena)
                            zapisz_historie(historia_dl, 'sprzedaz', nazwa, cef, ilosc)
    # zakup - wprowadzamy zakupiony produkt do magazynu
    elif operacja == "zakup":
        nazwa = input("Podaj nazwe produktu: ")
        cena = input("Podaj cene produktu<int><float>: ")
        ilosc = input("Podaj ilosc produktow<int>: ")
        if nazwa == '' or cena == '' or ilosc == '':
            print("Operacja niemozliwa - podano pusta wartosc")
        else:
            # sprawdzamy poprawnosc ceny i ilosci
            noint = 0
            for y in cena:
                if y not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.'):
                    noint = 1
            for z in ilosc:
                if z not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                    noint = 1
            if noint == 1 or cena == '0' or ilosc == '0':
                print("Przynajmniej  jedna podana wartosc jest niepoprawna")
            else:
                ilosc = int(ilosc)
                # jako identyfikatora uzyjemy sumy nazwy i ceny - bo mozemy miec te same produkty o roznych cenach
                magazyn_add = nazwa + cena, nazwa, float(cena), ilosc
                # Najpierw sprawdzamy czy mamy wystarczajace srodki na koncie
                if konto < (float(magazyn_add[2]) * int(magazyn_add[3])):
                    print("Operacja niemozliwa - brak wystarczajacych srodkow na koncie")
                else:
                    wczytaj_magazyn()
                    if magazyn_add[0] not in magazyn:
                        # jesli takiego produktu niema w magazynie dopisujemy do magazynu
                        magazyn[magazyn_add[0]] = [magazyn_add[1], magazyn_add[2], magazyn_add[3]]
                        konto -= magazyn_add[2] * magazyn_add[3]
                        nadpisz_saldo(konto)
                        nadpisz_magazyn()
                        print("Dodano produkt do magazynu")
                        wczytaj_historie()
                        historia_dl = len(historia) + 1
                        cef = float(cena)
                        zapisz_historie(historia_dl, 'zakup', nazwa, cef, ilosc)
                    else:
                        # jesli taki produkt istnieje dodajemy tylko ilosc sztuk
                        x = magazyn[magazyn_add[0]][1]
                        y = magazyn[magazyn_add[0]][2] + ilosc
                        magazyn[magazyn_add[0]] = [nazwa, x, y]
                        konto -= magazyn_add[2] * magazyn_add[3]
                        nadpisz_saldo(konto)
                        nadpisz_magazyn()
                        print("Zmodyfikowano liczbe produktow w magazynie")
                        wczytaj_historie()
                        historia_dl = len(historia) + 1
                        cef = float(cena)
                        zapisz_historie(historia_dl, 'zakup', nazwa, cef, ilosc)
    # konto - wyswietlamy stan konta
    elif operacja == "konto":
        print(f"Stan konta wynosi: {konto}")
    # lista - wyswietlamy stan magazynu
    elif operacja == "lista":
        print("Stan magazynu: ")
        komunikat = "Magazyn jest pusty"
        wczytaj_magazyn()
        for i in magazyn:
            print(f"Nazwa: {magazyn[i][0]}, cena: {magazyn[i][1]}, ilosc: {magazyn[i][2]}")
            komunikat = ''
        if komunikat != '':
            print(komunikat)
    # magazyn - wyswietalmy stan magazynu dla danego produktu
    elif operacja == "magazyn":
        produkt = input("Podaj nazwe produktu: ")
        kontrolna = 0
        if produkt == '':
            print("Podano pusta nazwa - operacja niemozliwa do wykonania")
        else:
            wczytaj_magazyn()
            print("Stan magazynu dla podanego produktu: ")
            info = 'Magazyn jest pusty'
            kontrolna = 1
            for element in magazyn:
                if produkt == magazyn[element][0]:
                    print(f"Nazwa: {magazyn[element][0]}, cena: {magazyn[element][1]}, ilosc: {magazyn[element][2]}")
                    kontrolna = 0
                elif produkt != magazyn[element][0]:
                    info = "Brak w magazynie"
            if kontrolna == 1:
                print(info)
    elif operacja == "przeglad":
        wczytaj_historie()
        if len(historia) < 1:
            print("Brak wpisow")
        else:
            od = input("Podaj numer wpisu od ktorego chcesz rozpoczac<int>: ")
            do = input("Podaj numer wpisu do ktorego chcesz kontynuowac<int>: ")
            if od == '' and do == '':
                print("Podano puste wartosci - wyswietlam cala historia")
                for i in historia:
                    print(i, ": ", historia[i])
            elif od == '' and do != '':
                # sprawdzamy wprowadzona wartosc czy jest int+
                noint = 0
                for y in do:
                    if y not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                        noint = 1
                if noint == 1 or do == '0':
                    print("Podana wartosc jest niepoprawna")
                    print(f"Dopuszczalne wartosci powinny zawierac sie pomiedzy 1 i {len(historia)}")
                else:
                    print("Wyswietlam historie od poczatku do podanej wartosci")
                    for i in historia:
                        if i <= int(do):
                            print(i, ": ", historia[i])
            elif od != '' and do == '':
                noint = 0
                for y in od:
                    if y not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                        noint = 1
                if noint == 1 or od == '0':
                    print("Podana wartosc jest niepoprawna")
                    print(f"Dopuszcalne wartosci powinny zawierac sie pomiedzy 1 i {len(historia)}")
                else:
                    print("Wyswietlam historie od podanej wartosci do konca")
                    for i in historia:
                        if i >= int(od):
                            print(i, ": ", historia[i])
            elif od != '' and do != '':
                noint = 0
                for y in od:
                    if y not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                        noint = 1
                for z in do:
                    if z not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
                        noint = 1
                if noint == 1:
                    print("Przynajmniej  jedna podana wartosc jest niepoprawna")
                elif int(od) == 0 or int(do) == 0:
                    print("Podano niedopuszczalna zerowa wartosc")
                    print(f"Dopuszcalne wartosci powinny zawierac sie pomiedzy 1 i {len(historia)}")
                elif int(od) > int(do):
                    print("Wartosc poczatkowa wieksza od koncowej")
                    print(f"Dopuszcalne wartosci powinny zawierac sie pomiedzy 1 i {len(historia)}")
                else:
                    print("Wyswietlam historie dla podanego zakresu wartosci")
                    for i in historia:
                        if int(od) <= i <= int(do):
                            print(i, ": ", historia[i])
    # koniec - konczymy program
    elif operacja == "koniec":
        print("Koniec programu")
        break
