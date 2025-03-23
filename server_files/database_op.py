import os
import json

# Az adatbázisok tárolása JSON fájlban
DB_FILE = "databases.json"

def load_databases():
    """Betölti az adatbázisok listáját a JSON fájlból."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_databases(databases):
    """Ment egy adatbázist a JSON fájlba."""
    with open(DB_FILE, "w") as f:
        json.dump(databases, f, indent=4)

def create_database(db_name):
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
