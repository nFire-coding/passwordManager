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
    public partial class View : Form
    {
        private List<(string, string, string)> passwords;
        private byte[] key;
        public View(List<(string, string, string)> passwords, byte[] key)
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.FormClosing += View_FormClosing;
            this.passwords = passwords;
            this.key = key;
            textBox1.Click += textBox_Click;
            textBox2.Click += textBox_Click;
            textBox2.PasswordChar = '*';
        }

        private void View_FormClosing(object sender, FormClosingEventArgs e)
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

        private void textBox_Click(object sender, EventArgs e)
        {
            TextBox textBox = sender as TextBox;
            if (textBox != null)
            {
                Clipboard.SetText(textBox.Text);
                textBox.SelectAll();
            }
        }

        private void View_Load(object sender, EventArgs e)
        {
            List<string> services = new List<string>();
            foreach (var (service, username, password) in passwords)
            {
                services.Add(service);
            }
            foreach (var service in services)
            {
                listBox1.Items.Add(service);
            }
        }

        private void back_Click(object sender, EventArgs e)
        {
            List<string> services = new List<string>();
            foreach (var (service, username, password) in passwords)
            {
                services.Add(service);
            }
            foreach (var service in services)
            {
                listBox1.Items.Remove(service);
            }
            this.Hide();
            this.FormClosing -= View_FormClosing;
            menu menu = new menu(passwords, key);
            menu.ShowDialog();
            this.Close();
        }

        private void confirm_Click(object sender, EventArgs e)
        {
            var select = listBox1.SelectedItem;
            select = listBox1.GetItemText(select);
            if (string.IsNullOrEmpty(select.ToString()) || select.ToString() == " ")
            {
                MessageBox.Show("Seleziona un servizio per vedere la password!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            PasswordManager passwordManager = new PasswordManager();
            List<string> r = passwordManager.ViewPassword(passwords, key, select.ToString()); // 0 - service | 1 - username | 2 - password
            label1.Hide();
            confirm.Hide();
            listBox1.Hide();
            label3.Show();
            label4.Show();
            label5.Show();
            checkBox1.Show();
            textBox1.Show();
            textBox2.Show();
            textBox1.Text = r[1];
            textBox2.Text = r[2];
            List<string> services = new List<string>();
            foreach (var (service, username, password) in passwords)
            {
                services.Add(service);
            }
            foreach (var service in services)
            {
                listBox1.Items.Remove(service);
            }
            
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox1.Checked)
            {
                textBox2.PasswordChar = '*'; return;
            }
            textBox2.PasswordChar = '\0';
        }
    }
}
