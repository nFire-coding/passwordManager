# passwordManager
[Italian](/ReadMe/IT.md)

A simple password manager able to store your passwords

Instructions: 

-Install Python from the [official website](https://www.python.org/downloads/) (latest version) give access to Path and environment variables. 

-Launch the command ```pip install cryptography``` on the terminal in order install the only dependency. 

-Open a powershell window in the script folder and launch it with ```python Cifra.py```.


NB: Be careful about having the program generate more than one secret key. By default it is generated in the current folder so if you leave your old key in the current folder and have it generate a second one it will be overwritten. The program is made for educational use only and can be improved by everyone freely (for example, there is no functionality to change passwords already saved).