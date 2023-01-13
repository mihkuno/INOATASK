from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QDateEdit, QPlainTextEdit, QRadioButton
import sys
import random
import jsonlines

class Game(QMainWindow):
    def __init__(self):
        super(Game, self).__init__()
        
        # load ui file
        uic.loadUi("assets/game.ui", self)
        
        # define objects and set event listener        
        self.btn_tiles = []
       
        btn_count = 0
        for row in range(3):
            bucket = []
            for col in range(3):
                object = self.findChild(QPushButton, f"btn_{btn_count}")
                object.clicked.connect(self.onClick)
                bucket.append(object)
                btn_count += 1
            self.btn_tiles.append(bucket)        
        
        self.human = random.choice(['X', 'O'])
        self.robot = 'X' if self.human == 'O' else 'O'        
        
        if self.robot == 'X': self.robotMove()
       
        
    def onClick(self):   
        # player clicks
        self.sender().setText(self.human)
        
        # check tiles
        result = self.checkTiles(self.human)

        # disable all tiles
        self.pauseTiles(True)
        
        if result: 
            self.gameOver('human')
            self.pauseTiles(True)
        else:        
            QTimer.singleShot(1000, self.robotMove)
                
            
    def robotMove(self):
        # robot clicks
        while True:
            rb_col = random.randint(0,2)
            rb_row = random.randint(0,2)
            selected = self.btn_tiles[rb_row][rb_col]
            
            if not selected.text().isalpha():
                selected.setStyleSheet("""color: red; 
                                       background-color: #7158e2""")
                
                selected.setText(self.robot)
                break
        
        # check tiles
        result = self.checkTiles(self.robot)
        
        # enable all tiles
        self.pauseTiles(False)

        if result: 
            self.gameOver('robot')
            self.pauseTiles(True)
            return True
                
        
    def pauseTiles(self, state):
        for row in self.btn_tiles:
            for col in row: 
                col.setEnabled(not state)
            
        
    def checkTiles(self, player):
        tiles_initial = []
        for row in range(3):
            col = self.btn_tiles[row]
            col = tuple(map(lambda row: 1 if row.text() == player else 0, col))
            tiles_initial.append(col)

        tiles_rotate = list(zip(*reversed(tiles_initial)))

        tiles_forward = []
        for ix, row in enumerate(tiles_initial):
            tiles_forward.append(row[ix])
        
        tiles_backward = []
        for ix, row in enumerate(tiles_initial):
            tiles_backward.append(row[2-ix])
            
        result = False
        
        if sum(tiles_forward) == 3: result = True
        
        if sum(tiles_backward) == 3: result = True
                        
        for row in tiles_initial:
            if sum(row) == 3: result = True
        
        for col in tiles_rotate:
            if sum(col) == 3: result = True
        
        return result
        

    def gameOver(self, player):
        for row in self.btn_tiles:
            for col in row: 
                if player == 'human':
                    col.setStyleSheet("""color: chartreuse; 
                                    background-color: #303030""")
                elif player == 'robot':
                    col.setStyleSheet("""color: red; 
                                    background-color: #303030""")


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        
        # load ui file
        uic.loadUi("assets/calculator.ui", self)
        
        # define objects and set event listener
        self.label = self.findChild(QLabel, "label")
        
        self.btn_number = []
        for i in range(10):
            object = self.findChild(QPushButton, f"btn_{i}")
            object.clicked.connect(self.onClick)
            self.btn_number.append(object)
        
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
    

class SignUp(QMainWindow):
    def __init__(self):
        super(SignUp, self).__init__()
        
        # load ui file
        uic.loadUi("assets/signup.ui", self)
        
        # define objects
        self.btn_signup = self.findChild(QPushButton, "btn_signup")
        self.in_ubdate = self.findChild(QDateEdit, "in_ubdate")
        self.in_uname = self.findChild(QPlainTextEdit, "in_uname")
        self.in_upasw = self.findChild(QPlainTextEdit, "in_upasw")
        self.in_upref1 = self.findChild(QRadioButton, "in_upref1")
        self.in_upref2 = self.findChild(QRadioButton, "in_upref2")
        self.out_label = self.findChild(QLabel, "out_label")
        
        # set event listener 
        self.btn_signup.clicked.connect(self.getUserInput)
        
    
    def getUserInput(self):
        uname = self.in_uname.toPlainText()
        upasw = self.in_upasw.toPlainText()
        ubdate = str(self.in_ubdate.date().toPyDate())
        upref = ''
        
        if self.in_upref1.isChecked():
            upref = self.in_upref1.text()
        elif self.in_upref2.isChecked():
            upref = self.in_upref2.text()

        if self.checkUserExists():
            self.out_label.setText(f"The account, '{uname}' already exists!")
        else:
            self.out_label.setText(f'Nice to meet you, {uname}')
            self.createUser(uname, upasw, ubdate, upref)
        
    
    def createUser(self, uname, upasw, ubdate, upref):
        # data to be written
        new_user = {
            "username": uname,
            "password": upasw,
            "birthdate": ubdate,
            "preference": upref
        }
        
        with jsonlines.open("users.jsonl", "a") as writer:   # for writing
            writer.write(new_user)
    
    
    def checkUserExists(self):
        with jsonlines.open('users.jsonl') as reader:      # for reading
            for obj in reader:
                if self.in_uname.toPlainText() == obj['username']:
                    return True
                               

class LogIn(QMainWindow):
    def __init__(self):
        super(LogIn, self).__init__()
        
        # load ui file
        uic.loadUi("assets/login.ui", self)
        
        # define objects
        self.in_uname = self.findChild(QPlainTextEdit, "in_uname")
        self.in_upasw = self.findChild(QPlainTextEdit, "in_upasw")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.out_label = self.findChild(QLabel, "out_label")
        
        # set event listener
        self.btn_login.clicked.connect(self.checkUserExists)
        
                
    def checkUserExists(self):        
        with jsonlines.open('users.jsonl') as reader:      # for reading
            for obj in reader:
                if self.in_uname.toPlainText() == obj['username']:
                    if self.in_upasw.toPlainText() != obj['password']:
                        self.out_label.setText(f"Incorrect Password")
                    else:
                        self.out_label.setText(f"Welcome back, {obj['username']}!")
                    break
                
        
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
            self.calculator = Calculator()
            self.calculator.show()    
            
        if sender == 'Game':
            self.game = Game()
            self.game.show()
            
        if sender == 'Sign Up':
            self.signup = SignUp()
            self.signup.show()
            
        if sender == 'Log In':
            self.login = LogIn()
            self.login.show()
        

# boilerplate
app = QApplication(sys.argv)
win = MainMenu()
win.show()

sys.exit(app.exec_())
