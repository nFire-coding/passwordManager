from src.imports import *


def generate_key():
    key = Fernet.generate_key()
    with open("../secret.key", "wb") as key_file:
        key_file.write(key)


# Per qualche ragione, secret.key è valido solo se è nella stessa directory del file .py
def load_key():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleziona il file chiave segreta")
    with open(file_path, "rb") as key_file:
        key = key_file.read()
    return key
