from src.imports import *
import os


def generate_key():
    key = Fernet.generate_key()
    key_file_path = os.path.join(os.getcwd(), "secret.key")
    with open(key_file_path, "wb") as key_file:
        key_file.write(key)
    print(Fore.GREEN + "Chiave generata con successo e salvata in secret.key.")


def load_key():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleziona il file chiave segreta")
    if not file_path:
        print(Fore.RED + "Nessun file selezionato. Impossibile caricare la chiave.")
        exit()
    with open(file_path, "rb") as key_file:
        key = key_file.read()
    return key
