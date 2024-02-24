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
    public partial class Edit : Form
    {
        private List<(string, string, string)> passwords;
        private byte[] key;
        private string service;
        public Edit(List<(string, string, string)> passwords, byte[] key, string service)
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.FormClosing += Edit_FormClosing;
            this.passwords = passwords;
            this.key = key;
            this.service = service;
            label2.Text = $"Modifica del servizio: {service}";
        }
        private void Edit_FormClosing(object sender, FormClosingEventArgs e)
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

        private void Edit_Load(object sender, EventArgs e)
        {
            
        }

        private void back_Click(object sender, EventArgs e)
        {
            this.Hide();
            this.FormClosing -= Edit_FormClosing;
            List list = new List(passwords, key);
            list.ShowDialog();
            this.Close();
        }

        private void delete_Click(object sender, EventArgs e)
        {
            var result = MessageBox.Show($"Sei sicuro di voler eliminare il servizio {service}?", "Conferma", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            if (result == DialogResult.Yes)
            {
                PasswordManager passwordManager = new PasswordManager();
                passwordManager.RemovePassword(passwords, service, key);
                this.Hide();
                this.FormClosing -= Edit_FormClosing;
                menu menu = new menu(passwords, key);
                menu.ShowDialog();
                this.Close();
                return;
            }
            

        }

        private void button3_Click(object sender, EventArgs e)
        {
            this.Hide();
            this.FormClosing -= Edit_FormClosing;
            EditServizio editServizio = new EditServizio(passwords, key, service);
            editServizio.ShowDialog();
            this.Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Hide();
            this.FormClosing -= Edit_FormClosing;
            EditUsername editUsername = new EditUsername(passwords, key, service);
            editUsername.ShowDialog();
            this.Close();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Hide();
            this.FormClosing -= Edit_FormClosing;
            EditPassword editPassword = new EditPassword(passwords, key, service);
            editPassword.ShowDialog();
            this.Close();
        }
    }
}
