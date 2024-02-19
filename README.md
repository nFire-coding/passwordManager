# Simple Password Manager

A simple password manager capable of securely storing your passwords.

## Instructions

### Prerequisites
- Install Python from the [official website](https://www.python.org/) (latest version) and ensure it is added to the system Path and environment variables.

### Installation
1. Open a terminal or powershell/command prompt.
2. Launch the following command to install the required dependency:
    ```
    pip install cryptography
    ```

### Usage
1. Navigate to the script folder in the terminal or powershell/command prompt.
2. Launch the script with Python by executing:
    ```
    python Cifra.py
    ```

## Notes
- **Caution**: Avoid generating more than one secret key. By default, it is generated in the current folder. If you generate a new key without removing the old one, it will be overwritten.
- This program is intended for educational use only.
- Feel free to contribute and improve the program. For example, there is currently no functionality to change passwords already saved.

## Compatibility
- This program is compatible with Windows, macOS, and GNU/Linux operating systems.
