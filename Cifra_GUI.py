import os
import pickle

import customtkinter
from colorama import init
from cryptography.fernet import Fernet
from typing import NoReturn

init(autoreset=True)


def clear_row(root: str, row: int) -> NoReturn:
    """Removes all items in a given CTk window in a given row"""
    slaves = root.grid_slaves(row=row)
    for slave in slaves:
        slave.destroy()


def load_services() -> NoReturn:
    """Loads a windows which shows every available service"""
    global level_1
    level_1 = customtkinter.CTkToplevel()
    level_1.title("Password Manager")
    level_1.geometry("600x500")

    button_add_credentials = customtkinter.CTkButton(level_1, text="Aggiungi nuovo servizio, username e password",
                                                     command=lambda: add_password(passwords_global, key_assigned))
    button_add_credentials.grid(row=0, column=0, padx=20, pady=10)

    button_view_password = customtkinter.CTkButton(level_1, text="Visualizza la password di un servizio",
                                                   command=lambda: view_password(passwords_global))
    button_view_password.grid(row=1, column=0, padx=20, pady=10)

    button_change_password = customtkinter.CTkButton(level_1, text="Cambia la password di un servizio",
                                                     command=lambda: change_password(passwords_global, key_assigned))
    button_change_password.grid(row=2, column=0, padx=20, pady=10)

    button_view_services = customtkinter.CTkButton(level_1, text="Visualizza la lista dei servizi salvati",
                                                   command=lambda: list_services(passwords_global))
    button_view_services.grid(row=3, column=0, padx=20, pady=10)


def generate_key() -> NoReturn:
    """Generates a key which is used in other parts"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    label_file_created = customtkinter.CTkLabel(app, text="File secrek.key generato nella cartella corrente")
    label_file_created.grid(row=2, column=0, padx=20, pady=10)
    assign_load_key()


def load_key() -> bytes | None:
    """Loads the key, asking the user to select the related file"""
    file_path = customtkinter.filedialog.askopenfilename(title="Seleziona il file chiave segreta",
                                                         defaultextension=".key")
    if file_path == "":
        label_file_error = customtkinter.CTkLabel(app, text="Nessun file selezionato")
        label_file_error.grid(row=2, column=0, padx=20, pady=10)
        return None
    else:
        with open(file_path, "rb") as key_file:
            key = key_file.read()
        label_file_ok = customtkinter.CTkLabel(app, text=f"Selezionato file in {file_path}")
        label_file_ok.grid(row=2, column=0, padx=20, pady=10)
        return key


def assign_load_key() -> NoReturn:
    """Assigns the key to a global variable which is used by other functions"""
    global key_assigned
    key_assigned = load_key()
    global passwords_global
    passwords_global = load_passwords(key_assigned)
    load_services()


def encrypt_password(password: str, key: bytes) -> bytes:
    """Encrypts a password using the fernet module"""
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password: bytes, key: bytes) -> str:
    """Returns an encrypted password given a key"""
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


def save_passwords(passwords, key: bytes):
    """Saves passwords in a file"""
    with open("passwords.dat", "wb") as password_file:
        encrypted_data = []
        for service, username, password in passwords:
            encrypted_service = encrypt_password(service, key)
            encrypted_username = encrypt_password(username, key)
            encrypted_password = encrypt_password(password, key)
            encrypted_data.append((encrypted_service, encrypted_username, encrypted_password))
        pickle.dump(encrypted_data, password_file)


def load_passwords(key: bytes) -> list:
    """Loads passwords from the password database"""
    passwords = []
    if os.path.exists("passwords.dat"):
        with open("passwords.dat", "rb") as password_file:
            encrypted_data = pickle.load(password_file)
            for encrypted_service, encrypted_username, encrypted_password in encrypted_data:
                service = decrypt_password(encrypted_service, key)
                username = decrypt_password(encrypted_username, key)
                password = decrypt_password(encrypted_password, key)
                passwords.append((service, username, password))
    return passwords


def add_password(passwords, key: bytes) -> NoReturn:
    """Adds a password in the database"""

    level_1b = customtkinter.CTkToplevel()
    level_1b.title("Aggiungi credenziali")
    level_1b.geometry("600x400")

    service_label = customtkinter.CTkLabel(level_1b, text="Servizio")
    service_input = customtkinter.CTkEntry(level_1b, placeholder_text="Inserisci il nome del servizio", width=200)
    service_label.grid(row=0, column=0, padx=20, pady=10)
    service_input.grid(row=0, column=1, padx=20, pady=10)

    username_label = customtkinter.CTkLabel(level_1b, text="Username")
    username_input = customtkinter.CTkEntry(level_1b, placeholder_text="Inserisci l'username del servizio", width=200)
    username_label.grid(row=1, column=0, padx=20, pady=10)
    username_input.grid(row=1, column=1, padx=20, pady=10)

    password_label = customtkinter.CTkLabel(level_1b, text="Password")
    password_input = customtkinter.CTkEntry(level_1b, placeholder_text="Inserisci la password del servizio", width=200)
    password_label.grid(row=2, column=0, padx=20, pady=10)
    password_input.grid(row=2, column=1, padx=20, pady=10)

    def get_credentials():
        service = service_input.get()
        username = username_input.get()
        password = password_input.get()

        passwords.append((service, username, password))
        save_passwords(passwords, key)

    button_add_credentials = customtkinter.CTkButton(level_1b,text="Aggiungi credenziali", command=get_credentials)
    button_add_credentials.grid(row=4, column=0, padx=20, pady=10)


def view_password(passwords) -> NoReturn:
    """Views a password given a service"""

    level_1bis = customtkinter.CTkToplevel()
    level_1bis.title("Vedi la password")
    level_1bis.geometry("600x400")
    service_input = customtkinter.CTkEntry(level_1bis,
                                           placeholder_text="Inserisci il nome del servizio per visualizzare la password", width=400)
    service_input.grid(row=0, column=0, padx=20, pady=10)

    def find() -> NoReturn:
        """Tries to get a password given a service"""

        service_name = service_input.get()

        found = False
        for _, (service, username, password) in enumerate(passwords):
            if service == service_name:
                try:
                    clear_row(level_1bis, 2)
                except:
                    pass
                finally:
                    service_label = customtkinter.CTkLabel(level_1bis, text=f"servizio: {service}")
                    username_label = customtkinter.CTkLabel(level_1bis, text=f"username: {username}")
                    password_label = customtkinter.CTkLabel(level_1bis, text=f"passowrd: {password}")

                    service_label.grid(row=2, column=0, padx=20, pady=10)
                    username_label.grid(row=3, column=0, padx=20, pady=10)
                    password_label.grid(row=4, column=0, padx=20, pady=10)
                    found = True
                    break
        if not found:
            try:
                service_label.destroy()
                username_label.destroy()
                password_label.destroy()
            except:
                pass
            finally:
                message_404_label = customtkinter.CTkLabel(level_1bis,
                                                        text=f"Password per il servizio '{service_name}' non trovata.")
                message_404_label.grid(row=2, column=0, padx=20, pady=10)

    service_button =customtkinter.CTkButton(level_1bis, text="Trova", command=find)
    service_button.grid(row=1, column=0, padx=20, pady=10)


def change_password(passwords, key: bytes) -> NoReturn:
    """Changes the password given a service"""

    level_1bis = customtkinter.CTkToplevel()
    level_1bis.geometry("600x400")
    level_1bis.title("Cambia password")
    service_input = customtkinter.CTkEntry(level_1bis,
                                           placeholder_text="Inserisci il nome del servizio per cambiare la password", width=400)
    service_input.grid(row=0, column=0, padx=20, pady=10)

    def find() -> NoReturn:
        """Tries to change a password given a service"""

        service_name = service_input.get()
        found = False
        for i, (service, username, password) in enumerate(passwords):
            if service == service_name:
                new_password_input = customtkinter.CTkEntry(level_1bis,
                                                    placeholder_text="Inserisci la nuova password: ")
                new_password_input.grid(row=1, column=0, padx=20, pady=10)
                def change():
                    new_password = new_password_input.get()
                    passwords[i] = (service, username, new_password)
                    save_passwords(passwords, key)
                    message_changed_label = customtkinter.CTkLabel(level_1bis,
                                                            text=f"Password per il servizio '{service_name}' cambiata con successo.")
                    message_changed_label.grid(row=3, column=0, padx=20, pady=10)
                found = True
                new_password_button = customtkinter.CTkButton(level_1bis, text="Cambia", command=change)
                new_password_button.grid(row=2, column=0, padx=20, pady=10)
                break
        if not found:
            message_404_label = customtkinter.CTkLabel(level_1bis,
                                                    text=f"Password per il servizio '{service_name}' non trovata.")
            message_404_label.grid(row=3, column=0, padx=20, pady=10)

    service_button =customtkinter.CTkButton(level_1bis, text="Trova", command=find)
    service_button.grid(row=1, column=0, padx=20, pady=10)


def list_services(passwords) -> NoReturn:
    """Gives a list of the services stored in the database"""

    level_1b = customtkinter.CTkToplevel()
    level_1b.title("Lista dei servizi")
    level_1b.geometry("200x500")
    if not passwords:
        label_no_passwords = customtkinter.CTkLabel(level_1b, text="Nessun servizio salvato.")
        label_no_passwords.grid(row=0, column=0, padx=20, pady=10)
    else:
        label_list_services = customtkinter.CTkLabel(level_1b, text="Elenco dei servizi salvati:")
        label_list_services.grid(row=1, column=0, padx=20, pady=10)
        index = 2
        for service, x, y in passwords:
            label_name = {service: f"label_{service}"}
            if service == "": 
                pass
            else:
                label_name[service] = customtkinter.CTkLabel(level_1b, text=service)
                label_name[service].grid(row=index, column=0, padx=20, pady=10)
                index += 1


def main():
    
    global app
    app = customtkinter.CTk()
    app.geometry("800x200")
    app.title("Password manager")

    key_label = customtkinter.CTkLabel(app, text="Hai già una chiave segreta?")
    key_label.grid(row=0, column=0, padx=20, pady=10)

    button_yes = customtkinter.CTkButton(app, text="SI", command=assign_load_key)
    button_yes.grid(row=1, column=0, padx=20, pady=10)

    button_no = customtkinter.CTkButton(app, text="NO", command=generate_key)
    button_no.grid(row=1, column=1, padx=20, pady=10)

    app.mainloop()


if __name__ == "__main__":
    main()
