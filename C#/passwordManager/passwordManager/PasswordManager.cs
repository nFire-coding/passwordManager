using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Runtime.Serialization.Formatters.Binary;
using System.Security.Cryptography;
using System.Windows.Forms;

namespace passwordManager
{
    public partial class PasswordManager : Form
    {
        private byte[] key;

        public PasswordManager()
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.FormClosing += PasswordManager_FormClosing;
        }

        private void PasswordManager_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (e.CloseReason == CloseReason.UserClosing)
            {
                var result = MessageBox.Show("Sei sicuro di voler chiudere il programma?", "Conferma", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if (result == DialogResult.No)
                {
                    e.Cancel = true;
                }
            }
        }

        private void GenerateKey()
        {
            key = Aes.Create().Key;
            File.WriteAllBytes("secret.key", key);
        }

        private byte[] LoadKey()
        {
            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.Title = "Seleziona il file chiave segreta";
                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    return File.ReadAllBytes(openFileDialog.FileName);
                }
            }
            return null;
        }

        private byte[] EncryptPassword(string password, byte[] key)
        {
            using (Aes aesAlg = Aes.Create())
            {
                aesAlg.Key = key;
                aesAlg.GenerateIV();

                ICryptoTransform encryptor = aesAlg.CreateEncryptor(aesAlg.Key, aesAlg.IV);

                using (MemoryStream msEncrypt = new MemoryStream())
                {
                    using (CryptoStream csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write))
                    {
                        using (StreamWriter swEncrypt = new StreamWriter(csEncrypt))
                        {
                            swEncrypt.Write(password);
                        }
                    }
                    return aesAlg.IV.Concat(msEncrypt.ToArray()).ToArray();
                }
            }
        }

        private bool error = false;

        private string DecryptPassword(byte[] encryptedPassword, byte[] key)
        {
            try
            {
                using (Aes aesAlg = Aes.Create())
                {
                    aesAlg.Key = key;
                    aesAlg.IV = encryptedPassword.Take(16).ToArray();

                    ICryptoTransform decryptor = aesAlg.CreateDecryptor(aesAlg.Key, aesAlg.IV);

                    using (MemoryStream msDecrypt = new MemoryStream(encryptedPassword.Skip(16).ToArray()))
                    {
                        using (CryptoStream csDecrypt = new CryptoStream(msDecrypt, decryptor, CryptoStreamMode.Read))
                        {
                            using (StreamReader srDecrypt = new StreamReader(csDecrypt))
                            {
                                return srDecrypt.ReadToEnd();
                            }
                        }
                    }
                }
            } catch (Exception ex)
            {
                if (!error)
                {
                    error = true;
                    MessageBox.Show("Chiave segreta non valida! Se l'hai persa elimina il file passwords.dat.", "Chiave non valida", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                return null;

            }
        }

        private void SavePasswords(List<(string, string, string)> passwords, byte[] key)
        {
            using (FileStream fs = new FileStream("passwords.dat", FileMode.Create))
            {
                BinaryFormatter bf = new BinaryFormatter();
                List<(byte[], byte[], byte[])> encryptedData = new List<(byte[], byte[], byte[])>();
                foreach (var (service, username, password) in passwords)
                {
                    var encryptedService = EncryptPassword(service, key);
                    var encryptedUsername = EncryptPassword(username, key);
                    var encryptedPassword = EncryptPassword(password, key);
                    encryptedData.Add((encryptedService, encryptedUsername, encryptedPassword));
                }
                bf.Serialize(fs, encryptedData);
            }
        }

        public List<(string, string, string)> LoadPasswords(byte[] key)
        {
            List<(string, string, string)> passwords = new List<(string, string, string)>();

            if (File.Exists("passwords.dat"))
            {
                using (FileStream fs = new FileStream("passwords.dat", FileMode.Open))
                {
                    BinaryFormatter bf = new BinaryFormatter();
                    var encryptedData = (List<(byte[], byte[], byte[])>)bf.Deserialize(fs);

                    foreach (var (encryptedService, encryptedUsername, encryptedPassword) in encryptedData)
                    {
                        var service = DecryptPassword(encryptedService, key);
                        var username = DecryptPassword(encryptedUsername, key);
                        var password = DecryptPassword(encryptedPassword, key);

                        if (service != null && username != null && password != null)
                        {
                            passwords.Add((service, username, password));
                        }
                        else
                        {
                            return null;
                        }
                    }
                }
            }

            return passwords;
        }

        public void AddPassword(List<(string, string, string)> passwords, byte[] key, string service, string username, string password)
        {
            passwords.Add((service, username, password));
            SavePasswords(passwords, key);
        }

        public void RemovePassword(List<(string, string, string)> passwords, string serviceName, byte[] key)
        {
            var passwordToRemove = passwords.FirstOrDefault(p => p.Item1 == serviceName);

            if (passwordToRemove != default)
            {
                passwords.Remove(passwordToRemove);

                SavePasswords(passwords, key);

                MessageBox.Show($"Password del servizio '{serviceName}' rimossa con successo.", "Password rimossa", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show($"Password del servizio '{serviceName}' non trovata.", "Password non trovata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        public void UpdateServiceName(List<(string, string, string)> passwords, string oldServiceName, string newServiceName, byte[] key)
        {
            var passwordToUpdate = passwords.FirstOrDefault(p => p.Item1 == oldServiceName);

            if (passwordToUpdate != default)
            {
                passwords.Remove(passwordToUpdate);

                passwordToUpdate.Item1 = newServiceName;

                passwords.Add(passwordToUpdate);

                SavePasswords(passwords, key);

                MessageBox.Show($"Nome del servizio modificato da '{oldServiceName}' a '{newServiceName}'.", "Modifica completata", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show($"Password del servizio '{oldServiceName}' non trovata.", "Password non trovata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        public void UpdateUsername(List<(string, string, string)> passwords, string serviceName, string newUsername, byte[] key)
        {
            var passwordToUpdate = passwords.FirstOrDefault(p => p.Item1 == serviceName);

            if (passwordToUpdate != default)
            {
                passwords.Remove(passwordToUpdate);

                passwordToUpdate.Item2 = newUsername;

                passwords.Add(passwordToUpdate);

                SavePasswords(passwords, key);

                MessageBox.Show($"Username del servizio '{serviceName}' modificato in '{newUsername}'.", "Modifica completata", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show($"Password del servizio '{serviceName}' non trovata.", "Password non trovata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        public void UpdatePassword(List<(string, string, string)> passwords, string serviceName, string newPassword, byte[] key)
        {
            var passwordToUpdate = passwords.FirstOrDefault(p => p.Item1 == serviceName);

            if (passwordToUpdate != default)
            {
                passwords.Remove(passwordToUpdate);

                passwordToUpdate.Item3 = newPassword;

                passwords.Add(passwordToUpdate);

                SavePasswords(passwords, key);

                MessageBox.Show($"Password del servizio '{serviceName}' modificata in '{newPassword}'.", "Modifica completata", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show($"Password del servizio '{serviceName}' non trovata.", "Password non trovata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        public List<string> ViewPassword(List<(string, string, string)> passwords, byte[] key, string serviceName)
        {
            bool found = false;
            List<string> r = new List<string>();
            foreach (var (service, username, password) in passwords)
            {
                if (service == serviceName)
                {
                    r.Add(service);
                    r.Add(username);
                    r.Add(password);
                    found = true;
                    break;
                }
            }
            if (!found)
            {
                MessageBox.Show($"Password per il servizio '{serviceName}' non trovata.", "Password non trovata", MessageBoxButtons.OK, MessageBoxIcon.Error); return null;
            }
            return r;
        }

        public bool Exists(List<(string, string, string)> passwords, string serviceName)
        {
            bool found = false;
            foreach (var (service, username, password) in passwords)
            {
                if (service == serviceName)
                {
                    found = true; break;
                }
            }
            return found;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            error = false;
            key = LoadKey();
            if (key == null)
            {
                MessageBox.Show("Chiave segreta non valida! Se l'hai persa elimina il file passwords.dat.", "Chiave non valida", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            List<(string, string, string)> passwords = LoadPasswords(key);
            if (passwords == null)
            {
                return;
            } else
            {
                DisplayMenu(passwords);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            error = false;
            var res = MessageBox.Show("Sei sicuro di voler generare una chiave? Se hai una vecchia chiave in questa cartella verrà sovrascritta.", "Conferma", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (res == DialogResult.No)
            {
                return;
            }
            MessageBox.Show("Generata nella cartella corrente la tua chiave segreta (secret.key). NASCONDILA E CONSERVALA, serve a recuperare le tue password!", "Chiave segreta generata", MessageBoxButtons.OK, MessageBoxIcon.Information);
            GenerateKey();
            key = LoadKey();
            if (key == null)
            {
                MessageBox.Show("Chiave segreta non valida! Se l'hai persa elimina il file passwords.dat.", "Chiave non valida", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            List<(string, string, string)> passwords = LoadPasswords(key);
            if (passwords == null)
            {
                return;
            }
            else
            {
                DisplayMenu(passwords);
            }
        }

        private void DisplayMenu(List<(string, string, string)> passwords)
        {
            this.Hide();
            this.FormClosing -= PasswordManager_FormClosing;
            menu menu = new menu(passwords, key);
            menu.ShowDialog();
            this.Close();
        }

        private void PasswordManager_Load(object sender, EventArgs e)
        {

        }
    }
}