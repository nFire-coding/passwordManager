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
    public partial class EditUsername : Form
    {
        private List<(string, string, string)> passwords;
        private byte[] key;
        private string service;
        public EditUsername(List<(string, string, string)> passwords, byte[] key, string service)
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.FormClosing += EditUsername_FormClosing;
            this.passwords = passwords;
            this.key = key;
            this.service = service;
            label2.Text = $"Modifica dell'username del servizio: {service}";
        }

        private void EditUsername_FormClosing(object sender, FormClosingEventArgs e)
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

        private void EditUsername_Load(object sender, EventArgs e)
        {

        }

        private void back_Click(object sender, EventArgs e)
        {
            textBox1.Text = string.Empty;
            this.Hide();
            this.FormClosing -= EditUsername_FormClosing;
            Edit edit = new Edit(passwords, key, service);
            edit.ShowDialog();
            this.Close();
        }

        private void confirm_Click(object sender, EventArgs e)
        {
            string text = textBox1.Text;
            if (string.IsNullOrEmpty(text) || text == " ")
            {
                MessageBox.Show("Devi inserire del testo per modifcare l'username!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            PasswordManager passwordManager = new PasswordManager();
            passwordManager.UpdateUsername(passwords, service, text, key);
            this.Hide();
            this.FormClosing -= EditUsername_FormClosing;
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

    }
}
