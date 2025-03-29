import socket
import os
import re
from server_files.database_op import create_database
from server_files.table_op import create_table
from server_files.database_op import use_database
from server_files.database_op import get_database_names_from_file,drop_database
from server_files.table_op import drop_table,get_tables_from_database

HOST = '127.0.0.1'
PORT = 12345

def parse_command(command):
    command = command.strip()

    #visszakuldi az operator tipusat + a neve (pl tabla, database)
    if match := re.match(r'create database (\w+)', command):
        return "create_database", match.group(1)
    elif match := re.match(r'use database (\w+)', command):
        return "use_database", match.group(1)
    elif match := re.match(r'create table (\w+)\s+(.*)', command):
        table_name = match.group(1)
        columns_raw = match.group(2).split(",")
        columns = {}
        for col in columns_raw:
            col_parts = col.strip().split(":")  # Kettőspont szerint is szétbontás
            if len(col_parts) == 2:
                col_name = col_parts[0].strip()
                col_type = col_parts[1].strip()
                columns[col_name] = col_type  # Dictionary-ba mentjük
            else:
                print(f"Hibas oszlopdefinicio: {col}")
        '''
        columns = match.group(2).split(",")
        columns = [col.strip() for col in columns]
        print(table_name)
        print(columns)'
        '''
        return "create_table", (table_name,columns)
    elif match := re.match(r'list databases', command):
        return "list_databases", None
    elif match := re.match(r'drop table (\w+)', command):
        return "drop_table", match.group(1)
    elif match := re.match(r'list tables',command):
        return "list_tables",None
    elif match := re.match(r'drop database (\w+)', command):
        return "drop_database", match.group(1)
    else:
        return None, None

def handle_client(client_socket):
    with client_socket:
        client_socket.sendall(b"Simple DB Server Ready. Send commands:\n")

        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            print(f"Received command: {data}")
            if data.lower() == "exit":
                client_socket.sendall(b"Goodbye!\n")
                break

            command_type, argument = parse_command(data)
            print(command_type)
            if command_type == "create_database":
                status = create_database(argument)
                response = f"Database '{argument}' created successfully!" if status == 0 else f"Database '{argument}' already exists."
            elif command_type == "list_databases":
                databases=get_database_names_from_file("databases.json")
                #szervernke ossze kell allitnaia eloszor a valaszt
                response= "Available databases:\n" + "\n".join(databases) if databases else "No databases found."
            elif command_type == "use_database":
                status =use_database(argument)
                if status == 0:
                    response = f"Using database '{argument}'"
                else:
                    response = f"Database '{argument}' does not exist."
            elif command_type == "create_table":
                status = create_table(argument[0],argument[1])
                print(status)
                response = f"Table '{argument}' created successfully!" if status == 0 else f"Table '{argument}' already exists."
            elif command_type == "drop_table":
                status = drop_table(argument)
                if status == 0:
                    response = f"Table '{argument}' deleted successfully!"
                elif status == 1:
                    response = "No database selected."
                else:
                    response = f"Table '{argument}' does not exist."
            elif command_type=="list_tables":
                print(argument)
                tables=get_tables_from_database()
                response= "Available tables:\n" + "\n".join(tables) if tables else "No tables found."
            elif command_type == "drop_database":
                status=drop_database(argument)
                response=f"Database '{argument}' deleted successfully!" if status == 0 else f"Database '{argument}' doesn't exist."
                print(status)
            else:
                response = "Invalid command."

            print(f"Sending response: {response}")
            client_socket.sendall(response.encode() + b"\n")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server is listening on {HOST}:{PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_client(client_socket)

if __name__ == "__main__":
    main()
