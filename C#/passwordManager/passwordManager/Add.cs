using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace passwordManager
{
    public partial class Add : Form
    {
        private List<(string, string, string)> passwords;
        private byte[] key;

        public Add(List<(string, string, string)> passwords, byte[] key)
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.FormClosing += Add_FormClosing;
            this.passwords = passwords;
            this.key = key;
            passwordBox.PasswordChar = '*';
        }

        private void Add_FormClosing(object sender, FormClosingEventArgs e)
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

        private void confirm_Click(object sender, EventArgs e)
        {
            var service = serviceBox.Text;
            if (service == null || service == " " || service == "")
            {
                MessageBox.Show("Devi inserire del testo per il nome del servizio!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            var username = usernameBox.Text;
            if (username == null || username == " " || username == "")
            {
                MessageBox.Show("Devi inserire del testo per il nome utente!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            var password = passwordBox.Text;
            if (password == null || password == " " || password == "")
            {
                MessageBox.Show("Devi inserire del testo per la password!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            PasswordManager passwordManager = new PasswordManager();
            var passwords = this.passwords;
            var key = this.key;
            bool exists = passwordManager.Exists(passwords, service);
            if (exists)
            {
                MessageBox.Show("Questo servizio è già esistente!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            passwordManager.AddPassword(passwords, key, service, username, password);
            MessageBox.Show($"Servizio {service} aggiunto correttamente!", "", MessageBoxButtons.OK, MessageBoxIcon.Information);
            serviceBox.Text = string.Empty;
            usernameBox.Text = string.Empty;
            passwordBox.Text = string.Empty;
            this.Hide();
            this.FormClosing -= Add_FormClosing;
            menu menu = new menu(passwords, key);
            menu.ShowDialog();
            this.Close();
        }

        private void back_Click(object sender, EventArgs e)
        {
            serviceBox.Text = string.Empty;
            usernameBox.Text = string.Empty;
            passwordBox.Text = string.Empty;
            this.Hide();
            this.FormClosing -= Add_FormClosing;
            menu menu = new menu(passwords, key);
            menu.ShowDialog();
            this.Close();
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox1.Checked)
            {
                passwordBox.PasswordChar = '*'; return;
            }
            passwordBox.PasswordChar = '\0';
        }
    }
}
