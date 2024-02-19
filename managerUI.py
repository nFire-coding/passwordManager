import os
import pickle
import pyperclip
from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet

# Funzioni per la gestione delle password
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    root = Tk()
    root.withdraw()

    # Chiedi all'utente di selezionare il file chiave
    file_path = filedialog.askopenfilename(title="Seleziona il file chiave")

    if not file_path:
        # Se non viene specificato un file, crea una nuova chiave e salvala in un nuovo file
        key = Fernet.generate_key()
        new_file_path = filedialog.asksaveasfilename(title="Salva la nuova chiave", defaultextension=".key")
        if new_file_path:
            with open(new_file_path, "wb") as key_file:
                key_file.write(key)
        else:
            # Chiudi il programma se l'utente non specifica il percorso per salvare la nuova chiave
            messagebox.showinfo("Informazione", "Il programma verrà chiuso.")
            root.destroy()
            return None
    else:
        # Leggi la chiave dal file selezionato
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
    if os.path.exists("passwords.dat") and os.path.getsize("passwords.dat") > 0:
        with open("passwords.dat", "rb") as password_file:
            encrypted_data = pickle.load(password_file)
        for encrypted_service, encrypted_username, encrypted_password in encrypted_data:
            service = decrypt_password(encrypted_service, key)
            username = decrypt_password(encrypted_username, key)
            password = decrypt_password(encrypted_password, key)
            passwords.append((service, username, password))
    return passwords

# Funzioni per l'interfaccia utente
def add_account():
    global add_window
    add_window = Toplevel(root)
    add_window.title("Aggiungi Account")

    label_service = Label(add_window, text="Servizio:")
    label_service.grid(row=0, column=0, padx=5, pady=5)

    entry_service = Entry(add_window)
    entry_service.grid(row=0, column=1, padx=5, pady=5)

    label_username = Label(add_window, text="Username/Email:")
    label_username.grid(row=1, column=0, padx=5, pady=5)

    entry_username = Entry(add_window)
    entry_username.grid(row=1, column=1, padx=5, pady=5)

    label_password = Label(add_window, text="Password:")
    label_password.grid(row=2, column=0, padx=5, pady=5)

    entry_password = Entry(add_window, show="*")
    entry_password.grid(row=2, column=1, padx=5, pady=5)

    button_save = Button(add_window, text="Salva", command=lambda: save_new_account(entry_service, entry_username, entry_password))
    button_save.grid(row=3, columnspan=2, padx=5, pady=5)

def edit_account():
    global edit_window, selected_index

    edit_window = Toplevel(root)
    edit_window.title("Modifica Account")

    # Creazione del listbox per visualizzare i servizi
    service_listbox = Listbox(edit_window)
    service_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Popola il listbox con i servizi esistenti
    for service, _, _ in passwords:
        service_listbox.insert(END, service)

    def populate_fields(event):
        global selected_index  # Dichiarazione di selected_index come globale
        selected_service_index = service_listbox.curselection()
        if selected_service_index:
            service = service_listbox.get(selected_service_index[0])
            for idx, (s, _, _) in enumerate(passwords):
                if s == service:
                    selected_index = idx
                    break
            else:
                selected_index = None

            if selected_index is not None:
                entry_service.delete(0, END)
                entry_service.insert(END, passwords[selected_index][0])
                entry_username.delete(0, END)
                entry_username.insert(END, passwords[selected_index][1])
                entry_password.delete(0, END)
                entry_password.insert(END, passwords[selected_index][2])

    service_listbox.bind("<<ListboxSelect>>", populate_fields)

    label_service = Label(edit_window, text="Servizio:")
    label_service.grid(row=1, column=0, padx=5, pady=5)

    entry_service = Entry(edit_window)
    entry_service.grid(row=1, column=1, padx=5, pady=5)
    entry_service.insert(END, "Servizio")

    label_username = Label(edit_window, text="Nuovo Username/Email:")
    label_username.grid(row=2, column=0, padx=5, pady=5)

    entry_username = Entry(edit_window)
    entry_username.grid(row=2, column=1, padx=5, pady=5)
    entry_username.insert(END, "Username/Email")

    label_password = Label(edit_window, text="Nuova Password:")
    label_password.grid(row=3, column=0, padx=5, pady=5)

    entry_password = Entry(edit_window, show="*")
    entry_password.grid(row=3, column=1, padx=5, pady=5)
    entry_password.insert(END, "Password")

    button_save = Button(edit_window, text="Salva", command=lambda: save_edited_account(entry_service, entry_username, entry_password))
    button_save.grid(row=4, columnspan=2, padx=5, pady=5)

def save_edited_account(entry_service, entry_username, entry_password):
    global selected_index
    service = entry_service.get().strip()
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    if selected_index is not None:
        old_service, old_username, old_password = passwords[selected_index]
        if not service:
            service = old_service
        if not username:
            username = old_username
        if not password:
            password = old_password
        passwords[selected_index] = (service, username, password)
        save_passwords(passwords, key)
        # edit_window.destroy()  # Chiudi la finestra dopo aver salvato
        update_listbox()  # Aggiorna la visualizzazione degli account nel listbox
        messagebox.showinfo("Successo", "Account modificato con successo.")
    else:
        messagebox.showerror("Errore", "Nessun account selezionato.")


def save_new_account(entry_service, entry_username, entry_password):
    service = entry_service.get()
    username = entry_username.get()
    password = entry_password.get()

    # Aggiungi solo se tutti i campi sono stati compilati
    if service.strip() != "" and username.strip() != "" and password.strip() != "":
        passwords.append((service, username, password))
        save_passwords(passwords, key)
        add_window.destroy()  # Chiudi la finestra dopo aver salvato
        update_listbox()  # Aggiorna la visualizzazione degli account nel listbox
    else:
        messagebox.showerror("Errore", "Compila tutti i campi prima di salvare l'account.")


def view_accounts():
    listbox.delete(0, END)
    for service, _, _ in passwords:
        listbox.insert(END, service)

def update_listbox():
    listbox.delete(0, END)
    for service, _, _ in passwords:
        listbox.insert(END, service)

def view_details():
    selected_index = listbox.curselection()
    if selected_index:
        service, username, password = passwords[selected_index[0]]
        messagebox.showinfo("Dettagli Account", f"Servizio: {service}\nUsername/Email: {username}\nPassword: {password}")
    else:
        messagebox.showerror("Errore", "Seleziona un account dalla lista.")

def copy_username():
    selected_index = listbox.curselection()
    if selected_index:
        username = passwords[selected_index[0]][1]
        pyperclip.copy(username)
        #messagebox.showinfo("Copia riuscita", "Username/Email copiato negli appunti.") # Se vuoi che appaia ogni volta una finistra togli l'asterisco all'inizio
    else:
        messagebox.showerror("Errore", "Seleziona un account dalla lista.")

def copy_password():
    selected_index = listbox.curselection()
    if selected_index:
        password = passwords[selected_index[0]][2]
        pyperclip.copy(password)
        #messagebox.showinfo("Copia riuscita", "Password copiata negli appunti.") # Se vuoi che appaia ogni volta una finistra togli l'asterisco all'inizio
    else:
        messagebox.showerror("Errore", "Seleziona un account dalla lista.")

def on_closing():
    root.destroy()
    root.quit()

def main():
    global root
    root = Tk()
    root.title("Gestore Password")

    # Creazione del listbox per visualizzare gli account
    global listbox
    listbox = Listbox(root)
    listbox.pack(expand=YES, fill=BOTH)

    # Caricamento della chiave e delle password
    global key
    key = load_key()
    global passwords
    passwords = load_passwords(key)

    # Visualizzazione predefinita degli account
    view_accounts()
    # Ottieni le dimensioni dello schermo
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calcola la posizione centrale della finestra
    x = (screen_width - 400) / 2
    y = (screen_height - 400) / 2

    # Imposta le dimensioni e la posizione della finestra
    root.geometry("400x400+{}+{}".format(int(x), int(y)))

    # Creazione del menu
    menubar = Menu(root)
    root.config(menu=menubar)

    file_menu = Menu(menubar, tearoff=0)
    #file_menu.add_command(label="Visualizza Account", command=view_accounts)
    file_menu.add_command(label="Aggiungi Account", command=add_account)
    file_menu.add_command(label="Modifica Account", command=edit_account)
    file_menu.add_separator()
    file_menu.add_command(label="Esci", command=root.quit)
    menubar.add_cascade(label="Menu", menu=file_menu)

    # Pulsanti aggiuntivi
    button_view_details = Button(root, text="Visualizza Dettagli", command=view_details)
    button_view_details.pack(padx=5, pady=5)
    button_copy_username = Button(root, text="Copia Username/Email", command=copy_username)
    button_copy_username.pack(padx=5, pady=5)
    button_copy_password = Button(root, text="Copia Password", command=copy_password)
    button_copy_password.pack(padx=5, pady=5)

    # Associare la funzione on_closing all'evento di chiusura della finestra
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

if __name__ == "__main__":
    main()
