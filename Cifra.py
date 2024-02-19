import os
import pickle
import easygui
import sys
from getpass import getpass

from time import sleep
from PyInquirer import prompt, style_from_dict, Token
from colorama import Fore, init
from cryptography.fernet import Fernet

style = style_from_dict({
Token.Separator: '',
Token.QuestionMark: '#c675ff',
Token.Selected: '#24fc03',
Token.Pointer: '#24fc03',
Token.Instruction: '#d9fc38 bold',
Token.Answer: '#24fc03',
Token.Question: '#c675ff',
})

def clear():
    try:
        os.system("cls")
    except:
        os.system("clear")

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    file_path = easygui.fileopenbox(title='Seleziona il file chiave segreta', filetypes=['*.key'], default='*.key')
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
    password = getpass("Inserisci la password: ") # nasconde la password

    passwords.append((service, username, password))
    save_passwords(passwords, key)
    print("Password salvata con successo!")
    sleep(2)
    home()

def view_password(passwords, service_name):
    for service, username, password in passwords:
        if service == service_name:
            print(f"Servizio: {service}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            break
    print("\n\nPremi invio per tornare alla home")
    resp = prompt(back, style=style)
    do(resp['operation'])

def list_services(passwords):
    if not passwords:
        print("Nessun servizio salvato.")
        sleep(2)
        home()
    else:
        print("Elenco dei servizi salvati:")
        for service, _, _ in passwords:
            print(service)
        print("\n\nPremi invio per tornare alla home")
        resp = prompt(back, style=style)
        do(resp['operation'])

def get_services():
    services = []
    for service, _, _ in passwords:
        services.append(service)
    return services


back = [
    {
        'type': 'list',
        'name': 'operation',
        'message': '',
        'choices': [
            'Indietro',
        ]
    }
]

choiceKey = [
    {
        'type': 'list',
        'name': 'operation',
        'message': 'Hai già una chiave segreta?',
        'choices': [
            'Si',
            'No',
        ]
    }
]

choice = [
    {
        'type': 'list',
        'name': 'operation',
        'message': 'Menu',
        'choices': [
            'Aggiungi nuovo servizio, username e password',
            'Visualizza la password di un servizio',
            'Visualizza la lista dei servizi salvati',
            'Esci',
        ]
    }
]

services = get_services()

def do(operation):
    global passwords, key
    
    if operation == "Si":
        clear()
        key = load_key()
        passwords = load_passwords(key)
        home()
    elif operation == "No":
        clear()
        generate_key()
        print("Generata nella cartella corrente la tua chiave segreta (secret.key). NASCONDILA E CONSERVALA, serve a recuperare le tue password!")
        sleep(2)
        clear() 
        key = load_key()
        passwords = load_passwords(key)
        home()
    elif operation == "Aggiungi nuovo servizio, username e password":
        clear()
        add_password(passwords, key)
    elif operation == "Visualizza la password di un servizio":
        clear()
        view_password(passwords, key)
    elif operation == "Visualizza la lista dei servizi salvati":
        clear()
        list_services(passwords)
    elif operation == "Esci":
        clear()
        print("Arrivederci!")
        sleep(1.5)
        sys.exit(0)
    elif operation == "Indietro":
        home()
    elif operation in services:
        view_password(passwords, operation)

    
def start():
    clear()
    resp = prompt(choiceKey, style=style)
    do(resp['operation'])

def home():
    clear()
    resp = prompt(choice, style=style)
    do(resp['operation'])

if __name__ == "__main__":
    start()
