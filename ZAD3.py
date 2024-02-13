import csv
import requests
from datetime import datetime


def sprawdz_date(data):
    try:
        datetime.strptime(data, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def zapisz_do_pliku(numer_faktury, data_faktury, kwota_faktury, waluta_faktury, kwota_oplacona, waluta_oplacona, data_oplacenia, roznica_kursowa, roznica_oplacenia):
    with open('faktury.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Numer faktury", "Data faktury", "Kwota faktury", "Waluta faktury", "Kwota oplacona","Waluta oplaty", "Data oplacenia", "Roznica kursowa", "Roznica oplacenia"])
        writer.writerow([numer_faktury, data_faktury, kwota_faktury, waluta_faktury, kwota_oplacona, waluta_oplacona, data_oplacenia, roznica_kursowa, roznica_oplacenia])

def odczytaj_z_pliku(numer_faktury):
    with open('faktury.csv', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        found = False
        for row in reader:
            if row[0] == numer_faktury:
                print("Nr faktury:", row[0])
                print("Data faktury:", row[1])
                print("Kwota faktury:", row[2])
                print("Waluta faktury:", row[3])
                print("Kwota oplacona:", row[4]) 
                print("Waluta oplaty:", row[5])
                print("Data oplacenia:", row[6])
                print("Roznica kursowa:", row[7])
                print("Roznica opłacenia:", row[8])
                found = True
                break
        
        if not found:
            print("Nie znaleziono faktury o numerze:", numer_faktury)

def check_currency(currency):
    if currency.upper() == 'EUR':
        print("Wybrana waluta: Euro € (EUR).")
    elif currency.upper() == 'USD':
        print("Wybrana waluta: Dolary $ (USD).")
    elif currency.upper() == 'PLN':
        print("Wybrana waluta: Polski złoty Zł POLSKAGUROM (PLN).")
    else:
        print("Wybranej waluty nie ma w bazie danych, Wpisz którąś z walut podanych wyżej")

def pobierz_kurs_waluty(currency):
    try:
        response = requests.get(f"https://api.nbp.pl/api/exchangerates/rates/A/{currency}/")
        data = response.json()
        return data['rates'][0]['mid']
    except Exception as e:
        print("Błąd podczas pobierania kursu wymiany")
        return None

opcja = input("Wybierz działanie\nWpisz 1 jeśli chcesz odczytać dane faktury\nWpisz 2 jeśli chcesz wpisać dane faktury\nWybieram: ")
odpowiedz = int(opcja)

if odpowiedz == 1:
    numer_faktury = input("Podaj numer faktury do odczytu: ")
    odczytaj_z_pliku(numer_faktury)
else:
#1
    numer_faktury = input('Wpisz nr faktury: ') 
#2
    while True:
        data_faktury = input('Data faktury (RRRR-MM-DD): ')
        if sprawdz_date(data_faktury):
            break
        else:
            print("Nieprawidłowa data. Spróbuj ponownie.")

#3
    kwota_faktury = float(input('Kwota faktury: ')) 
#4
    while True: 
        waluta_faktury = input("Wybierz Walutę (EUR '€', USD '$', or PLN 'zł'): ")
        if waluta_faktury.upper() in ['EUR', 'USD', 'PLN']:
            check_currency(waluta_faktury)
            break
        else:
            print("Nieprawidłowa waluta")
#5
    while True:
        data_oplacenia = input('Data opłacenia (RRRR-MM-DD): ')
        if sprawdz_date(data_oplacenia):
            break
        else:
            print("Nieprawidłowa data. Spróbuj ponownie.")
#6
    kwota_oplacona = float(input('Ile zostało opłacone: '))
#7
    while True:
        waluta_oplacona = input("Wybierz Walutę (EUR '€', USD '$', or PLN 'zł': ")
        if waluta_oplacona.upper() in ['EUR', 'USD', 'PLN']:
            check_currency(waluta_oplacona)
            break
        else:
            print("Wybranej waluty nie ma w bazie danych, wpisz walutę podaną powyżej")

#8
    if kwota_oplacona == kwota_faktury:
        print("Faktura została opłacona w całości.")
        roznica_oplacenia = 0
    elif kwota_oplacona > kwota_faktury:
        liczenie_oplacenia = kwota_oplacona - kwota_faktury
        roznica_oplacenia = "Nadplata: " + str(liczenie_oplacenia)
        print(f"Faktura została opłacona w nadpłacie o kwocie: {liczenie_oplacenia}")
    else:
        liczenie_oplacenia = kwota_faktury - kwota_oplacona
        roznica_oplacenia = "Niedoplata: " + str(liczenie_oplacenia)
        print(f"Faktura zawiera niedopłatę o kwocie: {liczenie_oplacenia}")

    kurs_faktury = pobierz_kurs_waluty(waluta_faktury)
    kurs_oplacona = pobierz_kurs_waluty(waluta_oplacona)


    if kurs_faktury is not None and kurs_oplacona is not None:
        roznica_kursowa = kwota_oplacona / kurs_oplacona - (kwota_faktury / kurs_faktury)
        print(f"Różnica kursowa: {roznica_kursowa} {waluta_faktury}")
    else:
        roznica_kursowa = None
    

    print("Zapisano dane faktury do pliku")

    zapisz_do_pliku(numer_faktury, data_faktury, kwota_faktury, waluta_faktury, kwota_oplacona, waluta_oplacona, data_oplacenia, roznica_kursowa, roznica_oplacenia)
