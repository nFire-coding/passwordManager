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
    public partial class List : Form
    {
        private List<(string, string, string)> passwords;
        private byte[] key;
        public List(List<(string, string, string)> passwords, byte[] key)
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.FormClosing += List_FormClosing;
            this.passwords = passwords;
            this.key = key;
        }

        private void List_FormClosing(object sender, FormClosingEventArgs e)
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
            this.FormClosing -= List_FormClosing;
            menu menu = new menu(passwords, key);
            menu.ShowDialog();
            this.Close();
        }

        private void List_Load(object sender, EventArgs e)
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

        private void confirm_Click(object sender, EventArgs e)
        {
            var select = listBox1.SelectedItem;
            if (select == null)
            {
                MessageBox.Show("Per modificare un servizio devi prima selezionarlo!", "Errore", MessageBoxButtons.OK, MessageBoxIcon.Error); return;
            }
            select = listBox1.GetItemText(select);
            this.Hide();
            this.FormClosing -= List_FormClosing;
            Edit edit = new Edit(passwords, key, select.ToString());
            edit.ShowDialog();
            this.Close();
        }
    }
}
