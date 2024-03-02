from src.password_funcs import *
from src.key_funcs import *
from src.service_funcs import *


def main():
    global key

    choice = input("Hai già una chiave segreta? (Sì/No): ").strip().lower()

    if choice[0] == "s" or choice[0] == "y":
        key = load_key()
    elif choice[0] == "n":
        print(Fore.CYAN +
              "\nGenerata nella cartella corrente la tua chiave segreta (secret.key). "
              "NASCONDILA E CONSERVALA, serve a recuperare le tue password!")
        generate_key()
        exit()
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

        match choice:
            case "1":
                # TODO: Aggiungi un check per vedere se un servizio esiste già
                add_password(passwords, key)
            case "2":
                view_password(passwords, key)
            case "3":
                change_password(passwords, key)
            case "4":
                list_services(passwords)
            case "5":
                print(Fore.CYAN + "\nArrivederci!")
                break
            case _:
                print(Fore.RED + "Scelta non valida. " + Fore.YELLOW + "Si prega di rispondere con 1, 2, 3, 4 o 5.")


if __name__ == "__main__":
    main()
