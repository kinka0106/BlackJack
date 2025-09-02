import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.widget import Widget 
from kivy.graphics import Line
from kivy.uix.button import Button
import random
from itertools import product 
from random import shuffle
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


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


class StartBlackJackScreen(Screen):
    pass

class RulesScreen(Screen):
    pass

class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        deck = list(product(value,color))
        shuffle(deck)
        self.reload()
        
    def reload(self):
        self.ids.comment.text = ""
        self.ids.hit_button.disabled = False
        self.ids.pass_button.disabled = False
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
        self.ids.players_cards.text = f"{self.player_cards_all}"
        self.ids.sum_player.text= f" Total: {self.sum_playerhand}"
        
    def update_dealer_card_gui(self):
        self.ids.dealers_cards.text= f"{self.dealer_cards_all}"
        self.ids.sum_dealer.text = f" Total: {self.sum_dealerhand}"

    def hide_disabled_button(self):
        self.ids.hit_button.disabled = True
        self.ids.pass_button.disabled = True

    def hit(self):
        self.sum_playerhand = self.sum_playerhand + self.draw_card(self.carddeck,self.player_cards_all)
        self.update_player_card_gui()
        if self.sum_playerhand > 21:
            self.ids.comment.text = "Bust! You lose!"
            self.update_dealer_card_gui()
            self.hide_disabled_button()

    def pass_turn(self):

        while self.sum_dealerhand < 17 :
            self.sum_dealerhand = self.sum_dealerhand + self.draw_card(self.carddeck,self.dealer_cards_all)
            
        self.update_dealer_card_gui()
                
        if self.sum_dealerhand > 21:
            if self.sum_playerhand == 21 and len(self.player_cards_all) == 2:
                self.ids.comment.text = 'Blackjack! You win! :D'
            else:
                self.ids.comment.text = 'Dealer bust! You win!'
        #stop
        elif self.sum_playerhand <= self.sum_dealerhand:
            if self.sum_playerhand < self.sum_dealerhand:
                self.ids.comment.text = 'Dealer wins, you lose!'

            elif self.sum_playerhand == self.sum_dealerhand:
                self.ids.comment.text = 'Draw'
                
        else:  # tutaj juz mam więcej niz dealer 
            if self.sum_playerhand == 21:
                self.ids.comment.text = 'Blackjack! You win! :D'
            else:
                print('You win, dealer lost!')
                self.ids.comment.text = 'You win, dealer lost! :D'
        self.hide_disabled_button()

class BlackJackApp(MDApp):
    def build(self):
         sm = ScreenManager()
         sm.add_widget(StartBlackJackScreen(name='startscreen'))
         sm.add_widget(RulesScreen(name='rules'))
         sm.add_widget(GameScreen(name='game'))
         return sm

    
if __name__ == "__main__":
    BlackJackApp().run()