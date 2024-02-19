# Semplice gestore di password

Un semplice gestore di password in grado di memorizzare in modo sicuro le vostre password.

## Istruzioni

### Prerequisiti
- Installa python dal [sito ufficiale](https://www.python.org/) (ultima versione) e assicurati che sia stato aggiunto alla Path di sistema e alle variabili d'ambiente.

### Installazione
1. Apri un terminale o un prompt di comando powershell.
2. Lancia il seguente comando per installare le librerie necessarie:
    ```
    pip install -r requirements.txt
    ```

### Utilizzo
1. Naviga nella cartella del programma nel terminale o prompt di comando powershell.
2. Lancia lo script con python eseguendo:
    ```
    python Cifra.py
    ```

## Note
- **Attenzione**: Evita di generare più di una chiave segreta. Per impostazione predefinita, viene generata nella cartella corrente. Se si genera una nuova chiave senza rimuovere la vecchia, questa verrà sovrascritta.
- Questo programma è destinato esclusivamente all'uso didattico.
- Sentiti libero di contribuire e migliorare il programma. Ad esempio, attualmente non esiste una funzionalità per modificare le password già salvate.

## Compatibilità
- Questo programma è compatibile con Windows, macOS, e sistemi operativi GNU/Linux.