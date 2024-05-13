import sys
from src.password_funcs import *
from src.key_funcs import *
from src.service_funcs import *


def get_choice():
    """
    Ottiene e valida l'input dell'utente per la scelta dell'opzione del menu.
    """
    while True:
        choice = input("Scegli un'opzione (1/2/3/4/5): ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print(Fore.RED + "Scelta non valida. Si prega di rispondere con 1, 2, 3, 4 o 5.")


def main():
    """
    Funzione principale del programma.
    """
    try:
        global key

        choice = input("Hai già una chiave segreta? (Sì/No): ").strip().lower()

        if choice.startswith("s") or choice.startswith("y"):
            key = load_key()
        elif choice.startswith("n"):
            print(Fore.CYAN +
                  "\nGenerata nella cartella corrente la tua chiave segreta (secret.key). "
                  "NASCONDILA E CONSERVALA, serve a recuperare le tue password!")
            generate_key()
            sys.exit()
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

            choice = get_choice()

            if choice == "1":
                # TODO: Aggiungi un check per vedere se un servizio esiste già
                add_password(passwords, key)
            elif choice == "2":
                view_password(passwords, key)
            elif choice == "3":
                change_password(passwords, key)
            elif choice == "4":
                list_services(passwords)
            elif choice == "5":
                print(Fore.CYAN + "\nArrivederci!")
                break

    except KeyboardInterrupt:
        print(Fore.RED + "\nOperazione interrotta dall'utente. Arrivederci!")
        sys.exit()


if __name__ == "__main__":
    main()
