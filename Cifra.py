import os
import pickle
from cryptography.fernet import Fernet
from tkinter import filedialog, Tk
from colorama import init, Fore, Style

init(autoreset=True)

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleziona il file chiave segreta")
    with open(file_path, "rb") as key_file:
        key = key_file.read()
    return key

def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def save_passwords(passwords, key):
    with open("passwords.dat", "wb") as password_file:
        encrypted_data = []
        for service, username, password in passwords:
            encrypted_service = encrypt_password(service, key)
            encrypted_username = encrypt_password(username, key)
            encrypted_password = encrypt_password(password, key)
            encrypted_data.append((encrypted_service, encrypted_username, encrypted_password))
        pickle.dump(encrypted_data, password_file)

def load_passwords(key):
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

def add_password(passwords, key):
    service = input("Inserisci il nome del servizio: ")
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    passwords.append((service, username, password))
    save_passwords(passwords, key)
    print(Fore.GREEN + "Password salvata con successo!")

def view_password(passwords, key):
    service_name = input("Inserisci il nome del servizio per visualizzare la password: ")
    found = False
    for i, (service, username, password) in enumerate(passwords):
        if service == service_name:
            print(Fore.YELLOW + f"\nServizio: {service}")
            print(Fore.YELLOW + f"Username: {username}")
            print(Fore.YELLOW + f"Password: {password}")
            found = True
            break
    if not found:
        print(Fore.RED + f"Password per il servizio '{service_name}' non trovata.")

    # Attendi l'invio prima di tornare al menu
    input("Premi Invio per tornare al menu principale...")

def change_password(passwords, key):
    service_name = input("Inserisci il nome del servizio per cambiare la password: ")
    found = False
    for i, (service, username, password) in enumerate(passwords):
        if service == service_name:
            new_password = input("Inserisci la nuova password: ")
            passwords[i] = (service, username, new_password)
            save_passwords(passwords, key)
            print(Fore.GREEN + "Password cambiata con successo!")
            found = True
            break
    if not found:
        print(Fore.RED + f"Password per il servizio '{service_name}' non trovata.")

def list_services(passwords):
    if not passwords:
        print(Fore.YELLOW + "Nessun servizio salvato.")
    else:
        print(Fore.YELLOW + "Elenco dei servizi salvati:")
        for service, _, _ in passwords:
            print(Fore.LIGHTGREEN_EX + f"{service}")

def main():
    choice = input("Hai già una chiave segreta? (Sì/No): ").strip().lower()
    
    if choice in ["si", "sì", "s", "y", "yes"]:
        key = load_key()
    elif choice in ["n", "no"]:
        print(Fore.CYAN + "\nGenerata nella cartella corrente la tua chiave segreta (secret.key). NASCONDILA E CONSERVALA, serve a recuperare le tue password!")
        generate_key()
        key = load_key()
    else:
        print(Fore.RED + "Opzione non valida.")
        main()

    passwords = load_passwords(key)

    while True:
        print(Fore.CYAN + f"\nMenu:")
        print("1. Aggiungi nuovo servizio, username e password")
        print("2. Visualizza la password di un servizio")
        print("3. Cambia la password di un servizio")
        print("4. Visualizza la lista dei servizi salvati")
        print("5. Esci")
        choice = input("Scegli un'opzione (1/2/3/4/5): ").strip()

        if choice == "1":
            add_password(passwords, key)
        elif choice == "2":
            view_password(passwords, key)
        elif choice == "3":
            change_password(passwords, key)
        elif choice == "4":
            list_services(passwords)
        elif choice == "5":
            print(Fore.CYAN + "Arrivederci!")
            break
        else:
            print(Fore.RED + Fore.YELLOW + "Scelta non valida. Si prega di rispondere con 1, 2, 3, 4 o 5.")

if __name__ == "__main__":
    main()
