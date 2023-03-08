import psycopg2
import sqlalchemy.exc
from sqlalchemy import *

hostn1ame = "postgres.fbi.h-da.de"
database = ""
user = ""
pwd = ""
server = ""

engine = create_engine(f"postgresql+psycopg2://{user}:{pwd}@{server}/{database}", echo=False)
connection = engine.connect()
metadata = MetaData()


passagier = Table('passagier', metadata, autoload=True, autoload_with=engine)
flughafen = Table('flughafen', metadata, autoload=True, autoload_with=engine)
abflug = Table('abflug', metadata, autoload=True, autoload_with=engine)
flug = Table('flug', metadata, autoload=True, autoload_with=engine)
buchung = Table('buchung', metadata, autoload=True, autoload_with=engine)


def get_all_airports():
    query = select([flughafen.columns.iata, flughafen.columns.name])

    result_proxy = connection.execute(query)
    return result_proxy.fetchall()


def login(vorname: str, nachname: str) -> int:
    query = select([passagier.columns.kundennummer]).where(passagier.columns.vorname == vorname, passagier.columns.nachname == nachname)

    result_proxy = connection.execute(query)
    passenger_number = result_proxy.fetchone()

    if passenger_number is not None:
        return passenger_number[0]

    query = select([func.max(passagier.columns.kundennummer)])

    result_proxy = connection.execute(query)
    highest_passenger_number = result_proxy.fetchone()

    if highest_passenger_number is None:
        print("Die höchste Kundennumber kann nicht bestimmt werden")
        return -1

    new_passenger_number = highest_passenger_number[0] + 1

    query = insert(passagier).values(kundennummer=new_passenger_number, vorname=vorname, nachname=nachname)

    result_proxy = connection.execute(query)

    return new_passenger_number


def book_flight(current_user: int, home: str):
    query = select([abflug.columns.flugnr, abflug.columns.datum, flughafen.columns.name])
    query = query \
        .select_from(abflug
                        .join(flug, abflug.columns.flugnr == flug.columns.flugnr)
                        .join(flughafen, flughafen.columns.iata == flug.columns.ziel)) \
        .where(flug.columns.start == home)

    result_proxy = connection.execute(query)
    flights = result_proxy.fetchall()

    if not flights:
        print("Keine Flüge gefunden")
        return

    for flight in enumerate(flights):
        print(flight[0], flight[1][0], flight[1][1], flight[1][2])

    inp = int(input("Welche Flugnummer? "))
    if inp < 0 or inp >= len(flights):
        print("Ungültige Nummer")
        return

    flight = flights[inp]
    flight_number = flight[0]
    date = flight[1]

    query = insert(buchung).values(kundennummer=current_user, flugnr=flight_number,datum=date, ticket_preis=99)

    try:
        result_proxy = connection.execute(query)
        print(f"Flug {flight_number} für Datum {date} wurde gebucht.")
    except sqlalchemy.exc.IntegrityError:
        print(f"Sie haben den Flug {flight_number} für Datum {date} bereits gebucht.")

if __name__ == "__main__":

    current_user = None
    home = None
    while True:
        print()
        if current_user is None:
            print("Buchungssystem für Flüge - Hauptmenü")
            print("------------------------------------")
        else:
            print(
                f"Buchungssystem für Flüge - Hauptmenü (Eingeloggt: {current_user})")
            print("----------------------------------------------------")

        print("1 Benutzer einloggen")
        if current_user is not None:
            print("2 Heimatflughafen wählen")
            print("3 Flüge anzeigen und buchen")
        print("0 Programm beenden")
        inp = input("Eingabe? ")

        if inp == "0":
            break

        if inp == "1":
            vorname = input("Vorname? ")
            nachname = input("Nachname? ")
            current_user = login(vorname, nachname)
            print("Passagier eingeloggt")

        if current_user is not None and inp == "2":
            print()
            airports = get_all_airports()
            for airport in enumerate(airports):
                print(airport[0], airport[1][0], airport[1][1])
            inp = int(input("Welche Flughafennummer? "))
            if inp < 0 or inp >= len(airports):
                print("Ungültige Nummer ausgewählt!")
            else:
                home = airports[inp][0]

        if current_user is not None and inp == "3":
            if home is None:
                print("Bitte zuerst einen Heimatflughafen wählen")
            else:
                book_flight(current_user, home)
