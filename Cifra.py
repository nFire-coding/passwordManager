import os
import pickle
import sys
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                           QHeaderView, QMessageBox, QFileDialog, QDialog, QInputDialog,
                           QTabWidget, QGridLayout, QFrame, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QPixmap
import qdarkstyle

class PasswordEntry(QDialog):
    def __init__(self, parent=None, service="", username="", edit_mode=False):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Nuovo Servizio" if not edit_mode else "Modifica Servizio")
        self.setMinimumWidth(350)
        
        layout = QVBoxLayout()
        
        # Service input
        service_layout = QHBoxLayout()
        service_label = QLabel("Servizio:")
        self.service_input = QLineEdit(service)
        service_layout.addWidget(service_label)
        service_layout.addWidget(self.service_input)
        layout.addLayout(service_layout)
        
        # Username input
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_input = QLineEdit(username)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password input
        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.show_password_btn = QPushButton("👁️")
        self.show_password_btn.setFixedWidth(30)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.show_password_btn)
        layout.addLayout(password_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Annulla")
        self.confirm_btn = QPushButton("Salva")
        
        self.cancel_btn.clicked.connect(self.reject)
        self.confirm_btn.clicked.connect(self.accept)
        
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.confirm_btn)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # If in edit mode, disable service field
        if edit_mode:
            self.service_input.setReadOnly(True)
            self.service_input.setStyleSheet("background-color: #444;")
    
    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_btn.setText("🔒")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_btn.setText("👁️")
    
    def get_values(self):
        return (self.service_input.text(), 
                self.username_input.text(), 
                self.password_input.text())

class InitialKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurazione Chiave")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("Benvenuto in Cifra")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Per iniziare, hai bisogno di una chiave segreta per criptare le tue password.")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Buttons
        self.new_key_btn = QPushButton("Genera Nuova Chiave")
        self.existing_key_btn = QPushButton("Carica Chiave Esistente")
        
        self.new_key_btn.clicked.connect(self.accept_new)
        self.existing_key_btn.clicked.connect(self.accept_existing)
        
        layout.addWidget(self.new_key_btn)
        layout.addWidget(self.existing_key_btn)
        
        self.setLayout(layout)
        self.choice = None
    
    def accept_new(self):
        self.choice = "new"
        self.accept()
    
    def accept_existing(self):
        self.choice = "existing"
        self.accept()

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.passwords = []
        self.key = None
        
        self.setup_ui()
        self.init_key()
    
    def setup_ui(self):
        self.setWindowTitle("Cifra - Gestore Password")
        self.setMinimumSize(800, 500)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Password list tab
        password_tab = QWidget()
        password_layout = QVBoxLayout()
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Le Tue Password")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        
        # Search field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca servizio...")
        self.search_input.textChanged.connect(self.filter_table)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.search_input)
        
        password_layout.addLayout(header_layout)
        
        # Password table
        self.password_table = QTableWidget(0, 3)
        self.password_table.setHorizontalHeaderLabels(["Servizio", "Username", "Password"])
        self.password_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.password_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.password_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.password_table.setAlternatingRowColors(True)
        self.password_table.setSortingEnabled(True)
        password_layout.addWidget(self.password_table)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Aggiungi")
        self.edit_btn = QPushButton("Modifica")
        self.delete_btn = QPushButton("Elimina")
        self.view_btn = QPushButton("Mostra Password")
        
        self.add_btn.clicked.connect(self.add_password)
        self.edit_btn.clicked.connect(self.edit_password)
        self.delete_btn.clicked.connect(self.delete_password)
        self.view_btn.clicked.connect(self.view_password)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.edit_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.view_btn)
        
        password_layout.addLayout(buttons_layout)
        password_tab.setLayout(password_layout)
        
        # Settings tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout()
        
        # Key info
        key_group_layout = QVBoxLayout()
        key_title = QLabel("Chiave di Crittografia")
        key_title.setFont(QFont("Arial", 12, QFont.Bold))
        
        key_group_layout.addWidget(key_title)
        
        key_info_layout = QHBoxLayout()
        key_label = QLabel("File chiave corrente:")
        self.key_path_label = QLabel("Nessuna chiave caricata")
        key_info_layout.addWidget(key_label)
        key_info_layout.addWidget(self.key_path_label)
        key_info_layout.addStretch()
        
        key_group_layout.addLayout(key_info_layout)
        
        key_buttons_layout = QHBoxLayout()
        self.gen_key_btn = QPushButton("Genera Nuova Chiave")
        self.load_key_btn = QPushButton("Carica Chiave Esistente")
        self.save_key_btn = QPushButton("Esporta Chiave")
        
        self.gen_key_btn.clicked.connect(self.generate_key)
        self.load_key_btn.clicked.connect(self.load_key)
        self.save_key_btn.clicked.connect(self.save_key)
        
        key_buttons_layout.addWidget(self.gen_key_btn)
        key_buttons_layout.addWidget(self.load_key_btn)
        key_buttons_layout.addWidget(self.save_key_btn)
        
        key_group_layout.addLayout(key_buttons_layout)
        settings_layout.addLayout(key_group_layout)
        
        # Warning note
        warning_frame = QFrame()
        warning_frame.setFrameShape(QFrame.StyledPanel)
        warning_frame.setStyleSheet("QFrame { background-color: #FFA500; border-radius: 5px; }")
        warning_layout = QVBoxLayout(warning_frame)
        
        warning_title = QLabel("⚠️ Attenzione")
        warning_title.setFont(QFont("Arial", 12, QFont.Bold))
        warning_text = QLabel(
            "La chiave segreta è essenziale per la sicurezza delle tue password.\n"
            "• Conservala in un luogo sicuro\n"
            "• Se perdi la chiave, non potrai più accedere alle tue password\n"
            "• Non generare più chiavi se non necessario"
        )
        warning_text.setWordWrap(True)
        
        warning_layout.addWidget(warning_title)
        warning_layout.addWidget(warning_text)
        settings_layout.addWidget(warning_frame)
        
        # About section
        about_layout = QVBoxLayout()
        about_title = QLabel("Informazioni")
        about_title.setFont(QFont("Arial", 12, QFont.Bold))
        
        about_text = QLabel(
            "Cifra - Gestore Password\n"
            "Un semplice gestore di password per mantenere al sicuro le tue credenziali.\n"
            "Versione 2.0 - GUI Edition"
        )
        about_text.setWordWrap(True)
        about_text.setAlignment(Qt.AlignCenter)
        
        about_layout.addWidget(about_title)
        about_layout.addWidget(about_text)
        settings_layout.addLayout(about_layout)
        
        # Add spacer to push everything up
        settings_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        settings_tab.setLayout(settings_layout)
        
        # Add tabs to widget
        tab_widget.addTab(password_tab, "Password")
        tab_widget.addTab(settings_tab, "Impostazioni")
        
        main_layout.addWidget(tab_widget)
    
    def init_key(self):
        dialog = InitialKeyDialog(self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            if dialog.choice == "new":
                self.generate_key()
            elif dialog.choice == "existing":
                if not self.load_key():
                    # If loading failed, ask again
                    self.init_key()
        else:
            # User closed the dialog without choosing
            sys.exit()
    
    def generate_key(self):
        key = Fernet.generate_key()
        
        # Ask where to save the key
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salva Chiave Segreta", "secret.key", "Key Files (*.key)"
        )
        
        if file_path:
            try:
                with open(file_path, "wb") as key_file:
                    key_file.write(key)
                
                self.key = key
                self.key_path_label.setText(file_path)
                
                QMessageBox.information(
                    self, 
                    "Chiave Generata", 
                    f"La chiave è stata generata e salvata in:\n{file_path}\n\n"
                    "IMPORTANTE: Conserva questa chiave in un luogo sicuro. "
                    "Senza di essa non potrai recuperare le tue password!"
                )
                
                # Load empty passwords list
                self.passwords = []
                self.update_table()
                
                return True
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Impossibile salvare la chiave: {str(e)}")
                return False
        
        return False
    
    def save_key(self):
        if not self.key:
            QMessageBox.warning(self, "Attenzione", "Nessuna chiave caricata da esportare.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Esporta Chiave Segreta", "secret.key", "Key Files (*.key)"
        )
        
        if file_path:
            try:
                with open(file_path, "wb") as key_file:
                    key_file.write(self.key)
                
                QMessageBox.information(
                    self, 
                    "Chiave Esportata", 
                    f"La chiave è stata esportata in:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Impossibile esportare la chiave: {str(e)}")
    
    def load_key(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona File Chiave", "", "Key Files (*.key);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, "rb") as key_file:
                    key = key_file.read()
                
                self.key = key
                self.key_path_label.setText(file_path)
                
                # Load passwords with the new key
                self.load_passwords()
                
                return True
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Impossibile caricare la chiave: {str(e)}")
                return False
        
        return False
    
    def encrypt_password(self, text):
        if not self.key:
            QMessageBox.critical(self, "Errore", "Nessuna chiave caricata.")
            return None
        
        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(text.encode())
        return encrypted
    
    def decrypt_password(self, encrypted_text):
        if not self.key:
            QMessageBox.critical(self, "Errore", "Nessuna chiave caricata.")
            return None
        
        try:
            fernet = Fernet(self.key)
            decrypted = fernet.decrypt(encrypted_text).decode()
            return decrypted
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Errore di decrittazione", 
                "Impossibile decifrare i dati. La chiave potrebbe essere errata."
            )
            return None
    
    def save_passwords(self):
        if not self.key:
            QMessageBox.critical(self, "Errore", "Nessuna chiave caricata.")
            return False
        
        try:
            encrypted_data = []
            for service, username, password in self.passwords:
                encrypted_service = self.encrypt_password(service)
                encrypted_username = self.encrypt_password(username)
                encrypted_password = self.encrypt_password(password)
                encrypted_data.append((encrypted_service, encrypted_username, encrypted_password))
            
            with open("passwords.dat", "wb") as password_file:
                pickle.dump(encrypted_data, password_file)
            
            return True
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile salvare le password: {str(e)}")
            return False
    
    def load_passwords(self):
        self.passwords = []
        
        if not self.key:
            QMessageBox.critical(self, "Errore", "Nessuna chiave caricata.")
            return False
        
        if os.path.exists("passwords.dat"):
            try:
                with open("passwords.dat", "rb") as password_file:
                    encrypted_data = pickle.load(password_file)
                    
                    for encrypted_service, encrypted_username, encrypted_password in encrypted_data:
                        service = self.decrypt_password(encrypted_service)
                        username = self.decrypt_password(encrypted_username)
                        password = self.decrypt_password(encrypted_password)
                        
                        if service and username and password:
                            self.passwords.append((service, username, password))
                
                self.update_table()
                return True
            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "Errore", 
                    f"Impossibile caricare le password: {str(e)}\n"
                    "La chiave potrebbe essere errata."
                )
                return False
        else:
            self.update_table()
            return True
    
    def update_table(self):
        self.password_table.setRowCount(0)
        
        if not self.passwords:
            return
        
        for row, (service, username, _) in enumerate(self.passwords):
            self.password_table.insertRow(row)
            
            service_item = QTableWidgetItem(service)
            username_item = QTableWidgetItem(username)
            password_item = QTableWidgetItem("••••••••")
            
            self.password_table.setItem(row, 0, service_item)
            self.password_table.setItem(row, 1, username_item)
            self.password_table.setItem(row, 2, password_item)
    
    def filter_table(self):
        search_text = self.search_input.text().lower()
        
        for row in range(self.password_table.rowCount()):
            service = self.password_table.item(row, 0).text().lower()
            username = self.password_table.item(row, 1).text().lower()
            
            if search_text in service or search_text in username:
                self.password_table.setRowHidden(row, False)
            else:
                self.password_table.setRowHidden(row, True)
    
    def add_password(self):
        if not self.key:
            QMessageBox.warning(self, "Attenzione", "Carica o genera una chiave prima di aggiungere password.")
            return
        
        dialog = PasswordEntry(self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            service, username, password = dialog.get_values()
            
            if not service or not username or not password:
                QMessageBox.warning(self, "Campi vuoti", "Tutti i campi sono obbligatori.")
                return
            
            # Check if service already exists
            for s, _, _ in self.passwords:
                if s == service:
                    QMessageBox.warning(
                        self, 
                        "Servizio duplicato", 
                        f"Esiste già un servizio chiamato '{service}'."
                    )
                    return
            
            self.passwords.append((service, username, password))
            self.save_passwords()
            self.update_table()
            
            QMessageBox.information(self, "Successo", "Password salvata con successo!")
    
    def edit_password(self):
        if not self.password_table.selectedItems():
            QMessageBox.warning(self, "Nessuna selezione", "Seleziona un servizio da modificare.")
            return
        
        selected_row = self.password_table.currentRow()
        service, username, password = self.passwords[selected_row]
        
        dialog = PasswordEntry(self, service, username, edit_mode=True)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            _, new_username, new_password = dialog.get_values()
            
            if not new_username or not new_password:
                QMessageBox.warning(self, "Campi vuoti", "Tutti i campi sono obbligatori.")
                return
            
            self.passwords[selected_row] = (service, new_username, new_password)
            self.save_passwords()
            self.update_table()
            
            QMessageBox.information(self, "Successo", "Password aggiornata con successo!")
    
    def delete_password(self):
        if not self.password_table.selectedItems():
            QMessageBox.warning(self, "Nessuna selezione", "Seleziona un servizio da eliminare.")
            return
        
        selected_row = self.password_table.currentRow()
        service = self.passwords[selected_row][0]
        
        confirm = QMessageBox.question(
            self,
            "Conferma eliminazione",
            f"Sei sicuro di voler eliminare il servizio '{service}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            del self.passwords[selected_row]
            self.save_passwords()
            self.update_table()
            
            QMessageBox.information(self, "Successo", "Servizio eliminato con successo!")
    
    def view_password(self):
        if not self.password_table.selectedItems():
            QMessageBox.warning(self, "Nessuna selezione", "Seleziona un servizio per visualizzare la password.")
            return
        
        selected_row = self.password_table.currentRow()
        service, username, password = self.passwords[selected_row]
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Dettagli Password")
        msg.setText(f"<b>Servizio:</b> {service}<br>"
                   f"<b>Username:</b> {username}<br>"
                   f"<b>Password:</b> {password}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    window = PasswordManager()
    window.show()
    
    sys.exit(app.exec_())