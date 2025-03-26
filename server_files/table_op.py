import os
import json
from server_files.database_op import DB_FILE, current_database, current_db_metadata  # Az adatbázis modulból importáljuk

def create_table(table_name, columns):
    """
    Létrehoz egy új táblát az aktuális adatbázisban.

    :param table_name: A létrehozandó tábla neve.
    :param columns: Szótár formátumú oszlopdefiníció pl. {"id": "int", "name": "str"}.
    :return: 0 ha sikeres, 1 ha nincs kiválasztott adatbázis, 2 ha már létezik a tábla.
    """
    global current_database, current_db_metadata

    # Ellenőrizzük, hogy van-e aktív adatbázis
    if current_database is None:
        return 1  # Nincs kiválasztott adatbázis

    db_path = os.path.join(DB_FILE, current_database)
    table_path = os.path.join(db_path, f"{table_name}.json")

    # Ellenőrizzük, hogy a tábla már létezik-e
    if os.path.exists(table_path):
        return 2  # A tábla már létezik

    # Létrehozzuk a tábla JSON fájlt (üres adatokkal, csak a struktúrát tartalmazza)
    table_data = {
        "columns": columns,  # Oszlopok és adattípusok
        "rows": []  # Üres tábla, nincsenek sorok még
    }

    with open(table_path, "w") as f:
        json.dump(table_data, f, indent=4)

    # Frissítjük az adatbázis metaadatait
    db_meta_path = os.path.join(db_path, "database.json")

    current_db_metadata["tables"].append(table_name)  # Táblanevet hozzáadjuk
    with open(db_meta_path, "w") as f:
        json.dump(current_db_metadata, f, indent=4)

    return 0  # Sikeres létrehozás
