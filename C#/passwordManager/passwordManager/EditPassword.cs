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
    public partial class EditPassword : Form
    {
        private List<(string, string, string)> passwords;
        private byte[] key;
        private string service;
        public EditPassword(List<(string, string, string)> passwords, byte[] key, string service)
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.FormClosing += EditPassword_FormClosing;
            this.passwords = passwords;
            this.key = key;
            this.service = service;
            textBox1.PasswordChar = '*';
            label2.Text = $"Modifica della password del servizio: {service}";
        }

        private void EditPassword_FormClosing(object sender, FormClosingEventArgs e)
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

        private void EditPassword_Load(object sender, EventArgs e)
        {

        }

        private void back_Click(object sender, EventArgs e)
        {
            textBox1.Text = string.Empty;
            this.Hide();
            this.FormClosing -= EditPassword_FormClosing;
            Edit edit = new Edit(passwords, key, service);
            edit.ShowDialog();
            this.Close();
        }

        private void confirm_Click(object sender, EventArgs e)
        {
            string text = textBox1.Text;
            if (string.IsNullOrEmpty(text) || text == " ")
            {
                MessageBox.Show("Devi inserire del testo per modifcare la password!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            PasswordManager passwordManager = new PasswordManager();
            passwordManager.UpdatePassword(passwords, service, text, key);
            this.Hide();
            this.FormClosing -= EditPassword_FormClosing;
            Edit edit = new Edit(passwords, key, service);
            edit.ShowDialog();
            this.Close();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox1.Checked)
            {
                textBox1.PasswordChar = '*'; return;
            }
            textBox1.PasswordChar = '\0';
        }
    }
}
