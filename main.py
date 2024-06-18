REPLACE   AND  WITH REQUIRED EMAIL AND PASSWORD.
store() METHOD IS OPTIONAL FOR STORING USER EMAILS IN DATABASE.
DATABASE:phoneapp
TABLE:numbers
COLUMN:phn

import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit,QPushButton,QPlainTextEdit
from PyQt6.QtGui import QAction

import mysql.connector

import smtplib

db = mysql.connector.connect(host="localhost",user="root",password="123456",database="phoneapp")
com = db.cursor()
class Window(QMainWindow):
    def __init__(self,db,com):
        self.db = db
        self.com = com
        super().__init__()
        self.setWindowTitle("Mail Client")
        self.emailLabel = QLabel("Email",self)
        self.emailLabel.setStyleSheet('''
                                font-family:Aerial;
                                font-weight:bold;
                              '''                               
                             )
        self.emailLabel.move(450,250)
        self.email = QLineEdit(self)
        self.email.move(600,250)
        self.email.resize(250,30)     

        self.msgLabel = QLabel("Message",self)
        self.msgLabel.setStyleSheet('''
                                font-family:Aerial;
                                font-weight:bold;
                              '''                               
                             )
        self.msgLabel.move(450,300)

        self.msg = QPlainTextEdit(self)
        self.msg.resize(500,300)
        self.msg.move(600,300)
        self.send = QPushButton(self)
        self.send.setText("Send Message")
        self.send.adjustSize()
        self.send.move(550,600)
        self.send.clicked.connect(self.sendmsg)

    def store(self):
        sql = "insert into numbers(phn) values(%s)";
        val = self.email.text(),
        self.com.execute(sql,val)

    def sendmsg(self):
        self.store()
        try:
            self.sender = "your_email"
            self.pwd  = "your_password"    
            smtp = smtplib.SMTP("smtp.gmail.com", port=587)
            smtp.starttls()
            smtp.login(self.sender, self.pwd)
            smtp.sendmail(self.sender, self.email.text(), self.msg.toPlainText())
            smtp.quit()
        except:
            SendingError = QMessageBox()
            SendingError.setIcon(QMessageBox.Icon.Warning)
            SendingError.setWindowTitle("Mail Client")
            SendingError.setText("Could not send the message!")
            SendingError.setStandardButtons(QMessageBox.StandardButton.Ok)
            SendingError.show()
            SendingError.exec()
        else:
            SendingSuccess = QMessageBox()
            SendingSuccess.setIcon(QMessageBox.Icon.Information)
            SendingSuccess.setWindowTitle("Mail Client")
            SendingSuccess.setText("Message sent successfully.")
            SendingSuccess.setStandardButtons(QMessageBox.StandardButton.Ok)
            SendingSuccess.show()
            SendingSuccess.exec()

app = QApplication(sys.argv)
w = Window(db,com)
w.show()
app.exec()

