from src.imports import *


def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password


def save_passwords(passwords, key):
    with open("../passwords.dat", "wb") as password_file:
        encrypted_data = []
        for service, username, password in passwords:
            encrypted_service = encrypt_password(service, key)
            encrypted_username = encrypt_password(username, key)
            encrypted_password = encrypt_password(password, key)
            encrypted_data.append((encrypted_service, encrypted_username, encrypted_password))
        pickle.dump(encrypted_data, password_file)


def load_passwords(key):
    passwords = []
    if os.path.exists("../passwords.dat"):
        with open("../passwords.dat", "rb") as password_file:
            encrypted_data = pickle.load(password_file)
            for encrypted_service, encrypted_username, encrypted_password in encrypted_data:
                service = decrypt_password(encrypted_service, key)
                username = decrypt_password(encrypted_username, key)
                password = decrypt_password(encrypted_password, key)
                passwords.append((service, username, password))
    return passwords


def add_password(passwords, key):
    service = input("\nInserisci il nome del servizio: ")
    username = input("Inserisci il nome utente: ")
    password = input("Inserisci la password: ")

    passwords.append((service, username, password))
    save_passwords(passwords, key)
    print(Fore.GREEN + "Password salvata con successo!")


def view_password(passwords, key):
    service_name = input("\nInserisci il nome del servizio per visualizzare la password: ")
    isFound = False
    for i, (service, username, password) in enumerate(passwords):
        if service == service_name:
            print(Fore.YELLOW + f"\nServizio: {service}")
            print(Fore.YELLOW + f"Username: {username}")
            print(Fore.YELLOW + f"Password: {password}")
            isFound = True
            break
    if not isFound:
        print(Fore.RED + f"\nPassword per il servizio '{service_name}' non trovata.")

    # Attendi l'invio prima di tornare al menu
    input(Fore.GREEN + "\nPremi Invio per tornare al menu principale...")
    print("\n")


def change_password(passwords, key):
    service_name = input("\nInserisci il nome del servizio per cambiare la password: ")
    isFound = False
    for i, (service, username, password) in enumerate(passwords):
        if service == service_name:
            new_password = input("\nInserisci la nuova password: ")
            passwords[i] = (service, username, new_password)
            save_passwords(passwords, key)
            print(Fore.GREEN + "\nPassword cambiata con successo!")
            isFound = True
            break
    if not isFound:
        print(Fore.RED + f"\nPassword per il servizio '{service_name}' non trovata.")
