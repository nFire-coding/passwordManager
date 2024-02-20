using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Text;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using static System.Windows.Forms.VisualStyles.VisualStyleElement.Window;

namespace passwordManager
{
    public partial class PasswordManager : Form
    {
        public PasswordManager()
        {
            InitializeComponent();
            
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

        private void button1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("SI");
        }

        private void button2_Click(object sender, EventArgs e)
        {
            MessageBox.Show("NO");
        }
    }

}
