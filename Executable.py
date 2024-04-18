import os
import platform
import subprocess

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode().strip())

def create_virtual_environment():
    print("Creazione dell'ambiente virtuale...")
    execute_command("python -m venv venv")

def upgrade_pip():
    print("Aggiornamento di pip...")
    execute_command("pip install --upgrade pip")

def install_requirements():
    print("Installazione dei requisiti...")
    execute_command("pip install -r requirements.txt")

def install_nuitka():
    print("Installazione di Nuitka...")
    execute_command("pip install nuitka")

def compile_with_nuitka():
    if platform.system() in ['Linux', 'Darwin']:  # macOS or GNU/Linux
        command = "python3 -m nuitka --enable-plugin=tk-inter --standalone --onefile cifra.py -o passwordManager"
    elif platform.system() == 'Windows':
        command = "python -m nuitka --enable-plugin=tk-inter --standalone --onefile cifra.py -o passwordManager"
    else:
        raise Exception("Sistema operativo non supportato.")
    
    print("Compilazione con Nuitka...")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode().strip())

def remove_temporary_directories():
    if platform.system() == 'Windows':
        execute_command("rmdir /s /q passwordManager.build")
    else:
        execute_command("rm -rf passwordManager.dist passwordManager.build")

def choicing():
    choice = input("Vuoi mantenere l'ambiente virtuale [Y,n]? ").strip().lower()
    if choice in ["si", "sì", "s", "y", "yes"]:
        print("Rimozione dell'ambiente virtuale e delle directory temporanee di Nuitka…")
        execute_command("rmdir /s /q venv" if platform.system() == 'Windows' else "rm -rf venv")
        remove_temporary_directories()
    elif choice in ["no", "n",]:
        print("Rimozione delle directory temporanee di Nuitka...")
        remove_temporary_directories()
    else:
        print("Rispondere con un Sì o un no")
        choicing()

def main():
    create_virtual_environment()
    upgrade_pip()
    install_requirements()
    install_nuitka()
    compile_with_nuitka()

    print("La compilazione è stata completata.")

    choicing()

    print("Per usare Password Manager puoi eseguire il file Python con 'python cifra.py' (vedi istruzioni nel file 'README.md' partendo dalla sezione 'Installazione'), oppure puoi eseguire il file eseguibile appena creato 'passwordManager' (l'estensione cambia in base al sistema usato).")

if __name__ == "__main__":
    main()

