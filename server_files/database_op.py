import os

def create_database(db_name):
    """Létrehoz egy új adatbázist mappaként"""
    try:
        # Ellenőrizzük, hogy létezik-e a 'databases' mappa, és ha nem, létrehozzuk
        if not os.path.exists("databases"):
            os.mkdir("databases")

        # Most létrehozhatjuk az adatbázist a megadott névvel
        os.mkdir(f"databases/{db_name}")
        return 0  # Siker

    except FileExistsError:
        return 1  # Sikertelen (már létezik)
    except Exception as e:
        print(f"Error creating database: {e}")
        return 2  # Általános hiba
