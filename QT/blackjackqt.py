
import sys
import random
from random import shuffle
from itertools import product
from PyQt5 import uic
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QStackedWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel

def strtoint(value):
    if value == 'Jack':
        return int(10)
    elif value == 'Queen':
        return int(10)
    elif value == 'King':
        return int(10)
    elif value == 'Ace':
        return int(11)
    elif value in ('2','3','4','5','6','7','8','9','10'): 
        return int(value)
    else :
        print('Nieznana karta')

value = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
color = ['trefl','karo','kier','pik']
deck = list(product(value,color)) # lista krotek 52
carddeck = deck
shuffle(carddeck)


class StartBlackJackScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_widget.ui", self)
        self.button_play = self.findChild(QPushButton, "button_play")
        self.button_rules = self.findChild(QPushButton, "button_rules")

        self.button_rules.clicked.connect(self.go_rules)
        self.button_play.clicked.connect(self.go_play)

    def go_rules(self):
        window = self.window()
        window.setPage(window.rules)

    def go_play(self):
        window = self.window()
        window.setPage(window.game)


class RulesScreen(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("rulesscreen.ui", self)
        self.btn_rules = self.findChild(QPushButton, "button_homerules")
        self.btn_rules.clicked.connect(self.back)

    def back(self):
        window = self.window()
        window.setPage(window.start)

class GameScreen(QWidget):
    def __init__(self, **kw):
        super().__init__(**kw)
        uic.loadUi("gamescreen.ui", self)
        self.dealers_cards = self.findChild(QLabel, "dealers_cards")
        self.players_cards = self.findChild(QLabel, "players_cards")
        self.sum_dealer = self.findChild(QLabel, "sum_dealer")
        self.sum_player = self.findChild(QLabel, "sum_player")
        self.comment = self.findChild(QLabel, "comment")
        self.hit_button = self.findChild(QPushButton, "hit_button")
        self.pass_button = self.findChild(QPushButton, "pass_button")
        self.home_button = self.findChild(QPushButton, "home_button")
        self.restart_button = self.findChild(QPushButton, "restart_button")

        self.hit_button.clicked.connect(self.hit)
        self.pass_button.clicked.connect(self.pass_turn)
        self.restart_button.clicked.connect(self.reload)
        self.home_button.clicked.connect(self.go_home)
        
        deck = list(product(value,color))
        shuffle(deck)
        self.reload()
        
    def go_home(self):
        window = self.window()
        window.setPage(window.start) 

    def reload(self):
        self.comment.setText("")
        self.hit_button.setEnabled(True)
        self.pass_button.setEnabled(True)
        shuffle(deck)

        self.deck = deck 
        self.color = color
        self.value = value
        self.carddeck = carddeck

        self.dealer_cards_all = []
        self.sum_dealerhand = 0
        self.sum_dealerhand= self.draw_card(self.carddeck, self.dealer_cards_all)  # dodanie karty do listy i dodanie int reurnowanego do zmiennej 
        self.update_dealer_card_gui()
        self.sum_dealerhand += self.draw_card(self.carddeck, self.dealer_cards_all)
      
        self.player_cards_all = []
        self.sum_playerhand = 0
        self.sum_playerhand = self.sum_playerhand + self.draw_card(self.carddeck, self.player_cards_all)
        self.sum_playerhand = self.sum_playerhand + self.draw_card(self.carddeck, self.player_cards_all)

        self.update_player_card_gui()
        
    
    def draw_card(self,carddeck,hand):
        randomcard = random.choice(carddeck)   # losuj
        hand.append(randomcard)  
        carddeck.remove(randomcard)
        
        result = strtoint(randomcard[0])

        if randomcard[0] == 'Ace':
            sum = 0
            for card in hand:
                sum += strtoint(card[0])
            if sum > 21 :
               result -= 10
                    
        return result

    def update_player_card_gui(self):
        self.players_cards.setText(f"{self.player_cards_all}")
        self.sum_player.setText(f" Total: {self.sum_playerhand}")
        
    def update_dealer_card_gui(self):
        self.dealers_cards.setText(f"{self.dealer_cards_all}")
        self.sum_dealer.setText(f" Total: {self.sum_dealerhand}")

    def hide_disabled_button(self):
        self.hit_button.setEnabled(False)
        self.pass_button.setEnabled(False)

    def hit(self):
        self.sum_playerhand = self.sum_playerhand + self.draw_card(self.carddeck,self.player_cards_all)
        self.update_player_card_gui()
        if self.sum_playerhand > 21:
            self.comment.setText("Bust! You lose!")
            self.update_dealer_card_gui()
            self.hide_disabled_button()

    def pass_turn(self):

        while self.sum_dealerhand < 17 :
            self.sum_dealerhand = self.sum_dealerhand + self.draw_card(self.carddeck,self.dealer_cards_all)
            
        self.update_dealer_card_gui()
                
        if self.sum_dealerhand > 21:
            if self.sum_playerhand == 21 and len(self.player_cards_all) == 2:
                self.comment.setText('Blackjack! You win! :D')
            else:
                self.comment.setText('Dealer bust! You win!')
        #stop
        elif self.sum_playerhand <= self.sum_dealerhand:
            if self.sum_playerhand < self.sum_dealerhand:
                self.comment.setText('Dealer wins, you lose!')

            elif self.sum_playerhand == self.sum_dealerhand:
                self.comment.setText('Draw')
                
        else:  # tutaj juz mam więcej niz dealer 
            if self.sum_playerhand == 21:
                self.comment.setText('Blackjack! You win! :D')
            else:
                print('You win, dealer lost!')
                self.comment.setText('You win, dealer lost! :D')
        self.hide_disabled_button()

class BlackJackWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_jack.ui", self)
        self.stacked = self.findChild(QStackedWidget, "stackedWidget")
        self.rules = RulesScreen()
        self.start = StartBlackJackScreen()
        self.game = GameScreen()

        self.stacked.addWidget(self.rules)
        self.stacked.addWidget(self.start)
        self.stacked.addWidget(self.game)
        
        self.setPage(self.start)
        
    def setPage(self, page):
        self.stacked.setCurrentWidget(page)

    
if __name__ == "__main__":
    app = QApplication([])
    window = BlackJackWindow()
    # widget.resize(800, 600)
    window.show()
    sys.exit(app.exec_())