import os
import json
from server_files.database_op import DB_FILE, current_db_metadata
#mindig a legfrisebb erteket kapjuk meg
import server_files.database_op as db_op

def create_table(table_name, columns):
    #global current_database
    print(f"Current database: {db_op.current_database}")
    if db_op.current_database is None:
        return 1

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
    tables=get_tables_from_database(db_op.current_database)
    if table_name in tables:
        return 2
    #table_path = os.path.join(db_path, f"{table_name}")

    #os.makedirs(db_path, exist_ok=True)
    databases[db_op.current_database]["tables"][table_name] = {
        "columns": columns,
        "rows": []
    }
    '''
    with open(table_path, "w") as f:
        json.dump(table_data, f, indent=4)

    db_meta_path = os.path.join(db_path, "database.json")

    current_db_metadata["tables"].append(table_name)
    with open(db_meta_path, "w") as f:
        json.dump(current_db_metadata, f, indent=4)
    '''
    with open(DB_FILE, "w") as f:
        json.dump(databases, f, indent=4)
    return 0  #sikeres letrehozas

def get_tables_from_database(filepath=DB_FILE):
    try:
        with open(filepath, 'r') as file:
            database_data = json.load(file)
            print(db_op.current_database)
            if db_op.current_database not in database_data:
                print(f"Error: Database '{db_op.current_database}' not found.")
                return []

            return list(database_data[db_op.current_database].get("tables", {}).keys())

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{filepath}'.")
        return []

def drop_table(table_name):
    if db_op.current_database is None:
        return 1

    try:
        with open(DB_FILE, "r") as f:
            databases = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{DB_FILE}' not found.")
        return 1
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{DB_FILE}'.")
        return 1

    db_name = db_op.current_database


    if table_name not in databases[db_name]["tables"]:
        return 2


    del databases[db_name]["tables"][table_name]


    with open(DB_FILE, "w") as f:
        json.dump(databases, f, indent=4)

    return 0
