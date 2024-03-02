from src.imports import *


def list_services(passwords):
    if not passwords:
        print(Fore.YELLOW + "\nNessun servizio salvato.")
    else:
        print(Fore.YELLOW + "\nElenco dei servizi salvati:")
        for service, _, _ in passwords:
            print(Fore.LIGHTGREEN_EX + f"{service}")
