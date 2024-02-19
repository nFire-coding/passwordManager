import os
import pickle
import easygui
import base64
import hashlib
from cryptography.fernet import Fernet
from pathlib import Path
from typing import List, Tuple

class PasswordManager:
    def __init__(self):
        self.key_file = Path("secret.key")
        self.password_file = Path("passwords.dat")
        self.salt_file = Path("salt.dat")
        self.backend = hashlib.sha256()

    def generate_salt(self) -> bytes:
        """Generate a random salt."""
        return os.urandom(16)

    def generate_key(self, master_password: str):
        """Generate a new key using a master password."""
        salt = self.generate_salt()
        key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
        with self.key_file.open("wb") as key_file:
            key_file.write(key)
        with self.salt_file.open("wb") as salt_file:
            salt_file.write(salt)

    def load_key(self, master_password: str) -> bytes:
        """Load the key using a master password."""
        with self.salt_file.open("rb") as salt_file:
            salt = salt_file.read()
        key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
        return key

    def encrypt_password(self, password: str, key: bytes) -> bytes:
        """Encrypt a password."""
        fernet = Fernet(base64.urlsafe_b64encode(key))
        encrypted_password = fernet.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password: bytes, key: bytes) -> str:
        """Decrypt a password."""
        fernet = Fernet(base64.urlsafe_b64encode(key))
        decrypted_password = fernet.decrypt(encrypted_password).decode()
        return decrypted_password

    def save_passwords(self, passwords: List[Tuple[str, str, str]], key: bytes):
        """Save encrypted passwords to a file."""
        with self.password_file.open("wb") as password_file:
            encrypted_data = [(self.encrypt_password(service, key), self.encrypt_password(username, key), self.encrypt_password(password, key)) for service, username, password in passwords]
            pickle.dump(encrypted_data, password_file)

    def load_passwords(self, key: bytes) -> List[Tuple[str, str, str]]:
        """Load encrypted passwords from a file."""
        passwords = []
        if self.password_file.exists():
            with self.password_file.open("rb") as password_file:
                encrypted_data = pickle.load(password_file)
                passwords = [(self.decrypt_password(encrypted_service, key), self.decrypt_password(encrypted_username, key), self.decrypt_password(encrypted_password, key)) for encrypted_service, encrypted_username, encrypted_password in encrypted_data]
        return passwords

    def add_password(self, passwords: List[Tuple[str, str, str]], key: bytes):
        """Add a new password."""
        service = input("Inserisci il nome del servizio: ")
        username = input("Inserisci il nome utente: ")
        password = input("Inserisci la password: ")

        passwords.append((service, username, password))
        self.save_passwords(passwords, key)
        print("Password salvata con successo!")

    def view_password(self, passwords: List[Tuple[str, str, str]], key: bytes):
        """View a password."""
        service_name = input("Inserisci il nome del servizio per visualizzare la password: ")
        for service, username, password in passwords:
            if service == service_name:
                print(f"Servizio: {service}")
                print(f"Username: {username}")
                print(f"Password: {password}")
                return
        print(f"Password per il servizio '{service_name}' non trovata.")

    def list_services(self, passwords: List[Tuple[str, str, str]]):
        """List all services."""
        if not passwords:
            print("Nessun servizio salvato.")
        else:
            print("Elenco dei servizi salvati:")
            for service, _, _ in passwords:
                print(service)

    def main(self):
        """Main function."""
        master_password = input("Inserisci la password master: ").strip()
        choice = input("Hai già una chiave segreta? (SI/NO): ").strip().upper()
        if choice == "SI":
            key = self.load_key(master_password)
        elif choice == "NO":
            print("Generata nella cartella corrente la tua chiave segreta (secret.key). NASCONDILA E CONSERVALA, serve a recuperare le tue password!")
            self.generate_key(master_password)
            key = self.load_key(master_password)
        else:
            return

        passwords = self.load_passwords(key)

        while True:
            print("\nMenu:")
            print("1. Aggiungi nuovo servizio, username e password")
            print("2. Visualizza la password di un servizio")
            print("3. Visualizza la lista dei servizi salvati")
            print("4. Esci")
            choice = input("Scegli un'opzione (1/2/3/4): ").strip()

            if choice == "1":
                self.add_password(passwords, key)
            elif choice == "2":
                self.view_password(passwords, key)
            elif choice == "3":
                self.list_services(passwords)
            elif choice == "4":
                print("Arrivederci!")
                break
            else:
                print("Scelta non valida. Si prega di rispondere con 1, 2, 3 o 4.")

if __name__ == "__main__":
    PasswordManager().main()
