import os
import pickle
from cryptography.fernet import Fernet
from tkinter import filedialog, Tk

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
    print("Password salvata con successo!")

def view_password(passwords, key):
    service_name = input("Inserisci il nome del servizio per visualizzare la password: ")
    found = False
    for service, username, password in passwords:
        if service == service_name:
            print(f"Servizio: {service}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            found = True
            break
    if not found:
        print(f"Password per il servizio '{service_name}' non trovata.")

def list_services(passwords):
    if not passwords:
        print("Nessun servizio salvato.")
    else:
        print("Elenco dei servizi salvati:")
        for service, _, _ in passwords:
            print(service)

def main():
    choice = input("Hai già una chiave segreta? (SI/NO): ").strip().upper()
    if choice == "SI":
        key = load_key()
    elif choice == "NO":
        print("Generata nella cartella corrente la tua chiave segreta (secret.key). NASCONDILA E CONSERVALA, serve a recuperare le tue password!")
        generate_key()
        key = load_key()
    else:
        return

    passwords = load_passwords(key)

    while True:
        print("\nMenu:")
        print("1. Aggiungi nuovo servizio, username e password")
        print("2. Visualizza la password di un servizio")
        print("3. Visualizza la lista dei servizi salvati")
        print("4. Esci")
        choice = input("Scegli un'opzione (1/2/3/4): ").strip()

        if choice == "1":
            add_password(passwords, key)
        elif choice == "2":
            view_password(passwords, key)
        elif choice == "3":
            list_services(passwords)
        elif choice == "4":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Si prega di rispondere con 1, 2, 3 o 4.")

if __name__ == "__main__":
    main()
