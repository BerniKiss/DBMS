import os
import json
from server_files.database_op import DB_FILE, current_db_metadata  # Az adatbázis modulból importáljuk
#mindig a legfrisebb erteket kapjuk meg
import server_files.database_op as db_op

def create_table(table_name, columns):
    """
    Létrehoz egy új táblát az aktuális adatbázisban.

    :param table_name: A létrehozandó tábla neve.
    :param columns: Szótár formátumú oszlopdefiníció pl. {"id": "int", "name": "str"}.
    :return: 0 ha sikeres, 1 ha nincs kiválasztott adatbázis, 2 ha már létezik a tábla.
    """
    #global current_database
    print(f"Current database: {db_op.current_database}")
    # Ellenőrizzük, hogy van-e aktív adatbázis
    if db_op.current_database is None:
        return 1  # Nincs kiválasztott adatbázis


    # Betöltjük az adatbázisokat
    try:
        with open(DB_FILE, "r") as f:
            databases = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{DB_FILE}' not found.")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{DB_FILE}'.")
        return 1



    #db_path = os.path.join(DB_FILE, db_op.current_database)

    #print(table_path)
    tables=get_tables_from_database(db_op.current_database,DB_FILE)
    # Ellenőrizzük, hogy a tábla már létezik-e
    if table_name in tables:
        return 2  # A tábla már létezik
    #table_path = os.path.join(db_path, f"{table_name}")

    #os.makedirs(db_path, exist_ok=True)
    # Létrehozzuk a tábla JSON fájlt (üres adatokkal, csak a struktúrát tartalmazza)
    databases[db_op.current_database]["tables"][table_name] = {
        "columns": columns,  # Oszlopok és adattípusok
        "rows": []  # Üres tábla, nincsenek sorok még
    }
    '''
    with open(table_path, "w") as f:
        json.dump(table_data, f, indent=4)

    # Frissítjük az adatbázis metaadatait
    db_meta_path = os.path.join(db_path, "database.json")

    current_db_metadata["tables"].append(table_name)  # Táblanevet hozzáadjuk
    with open(db_meta_path, "w") as f:
        json.dump(current_db_metadata, f, indent=4)
    '''
    with open(DB_FILE, "w") as f:
        json.dump(databases, f, indent=4)
    return 0  # Sikeres létrehozás

def get_tables_from_database(db_name, filepath=DB_FILE):
    """Reads a JSON file and returns a list of tables for a given database."""
    try:
        with open(filepath, 'r') as file:
            database_data = json.load(file)  # Load the JSON file into a Python dictionary

            if db_name not in database_data:
                print(f"Error: Database '{db_name}' not found.")
                return []

            return list(database_data[db_name].get("tables", {}).keys())

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'.")
        return []