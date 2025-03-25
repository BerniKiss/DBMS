import os
import json

current_database = None  # Globális változó az aktuális adatbázishoz
current_db_metadata = None

#adatbazis tarolasa json faljba
DB_FILE = "databases.json"
BASE_DIR = "databases"

def use_database(db_name):
    """Beállítja az aktuális adatbázist és betölti az adatbázis JSON fájlját"""
    global current_database


    db_path = os.path.join(BASE_DIR, db_name)
    print(f" Dolgozo konyvtar{BASE_DIR}")


    print(f"Checking if the database exists at: {db_path}")  # Debug log
    if not os.path.exists(db_path):
        print(f"Database '{db_name}' does not exist.")
        return 1  # Az adatbázis vagy annak metaadata nem létezik

    # Beállítjuk az aktuális adatbázist
    current_database = db_name
    print(f"Using database: {current_database}")
    return 0


def load_databases():
    #betolti az adatrbazist
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_databases(databases):
    with open(DB_FILE, "w") as f:
        json.dump(databases, f, indent=4)

def create_database(db_name):
    #letrehoz egy uj foldert minden adatbazisnak
    db_path = os.path.join(BASE_DIR, db_name)
    """Létrehoz egy új adatbázist a JSON fájlban"""
    # Betöltjük a jelenlegi adatbázisokat
    databases = load_databases()

    # Ellenőrizzük, hogy már létezik-e az adatbázis
    if db_name in databases:
        return 1  # Ha létezik már, nem hozhatjuk létre újra

    # Hozzáadjuk az új adatbázist
    databases[db_name] = {"tables": {}}

    # Mentjük a változásokat
    save_databases(databases)
    return 0  # Sikeresen létrehoztuk az adatbázist
