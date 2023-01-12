from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel
import sys

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        
        # load ui file
        uic.loadUi("assets/calculator.ui", self)
        
        # define objects and set event listener
        self.label = self.findChild(QLabel, "label")
        
        self.btn_number = []
        for i in range(10):
            self.btn_number.append(self.findChild(QPushButton, f"btn_{i}"))
            self.btn_number[i].clicked.connect(self.onClick)
        
        self.btn_function = ["btn_clear", 
                             "btn_divide", 
                             "btn_equal",
                             "btn_minus",
                             "btn_multiply",
                             "btn_plus" ]    
        
        for ix, name in enumerate(self.btn_function):
            self.btn_function[ix] = self.findChild(QPushButton, name)
            self.btn_function[ix].clicked.connect(self.onClick)        
    
    def onClick(self):
        input = self.sender().text()
        output = self.label.text()        
        
        if input == 'C': 
            output = '0' 
        elif input == '=': 
            try:
                output = str(eval(output))
            except:
                output = 'Error'
        else: 
            if input.isnumeric():
                output += input
            else:
                output += f' {input} '
            
        self.label.setText(output)
    

class MainMenu(QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        
        # load ui file
        uic.loadUi("assets/menu.ui", self)
        
        # define objects
        self.btn_login  = self.findChild(QPushButton, "btn_login")
        self.btn_signup = self.findChild(QPushButton, "btn_signup")
        self.btn_accounts = self.findChild(QPushButton, "btn_accounts")
        self.btn_calculator = self.findChild(QPushButton, "btn_calculator")
        self.btn_game = self.findChild(QPushButton, "btn_game")
        
        self.calculator = Calculator()
        
        # event listener
        self.btn_login.clicked.connect(self.onClick)
        self.btn_signup.clicked.connect(self.onClick)
        self.btn_accounts.clicked.connect(self.onClick)
        self.btn_calculator.clicked.connect(self.onClick)
        self.btn_game.clicked.connect(self.onClick)
        

    def onClick(self):
        sender = self.sender().text()
        print(sender+' was pressed')
        
        if sender == 'Calculator':
            self.calculator.show()    
        


# boilerplate
app = QApplication(sys.argv)
win = MainMenu()
win.show()


sys.exit(app.exec_())
