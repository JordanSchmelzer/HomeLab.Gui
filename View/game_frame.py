import customtkinter as ctk
from random import randint
import threading
import time
from dataclasses import dataclass


@dataclass
class GameState:
  deck = []
  player_hand = []
  dealer_hand = []
  player_bet = 0
  player_bank = 200000
  
  start_phase = True
  bet_phase = False
  round_complete = False

  doubled_down = False
  player_win = False
  player_bust = False
  dealer_bust = False
  push = False


class GameFrame(ctk.CTkFrame):
  def __init__(self, parent, controller):
    super().__init__(master=parent)
    self._controller = controller
    self._state = GameState()
    self._state.deck = self.new_deck()
    
    self._canvas = ctk.CTkCanvas(self, bg='white')
    self._canvas.pack(fill=ctk.BOTH)
    self._canvas.bind("<Button-1>", self.on_canvas_click)
    self.draw()


  def new_deck(self) -> list:
    clubs = ["Ac","2c","3c","4c","5c","6c","7c","8c","9c","1c","Jc","Qc","Kc"]
    diamonds = ["Ad","2d","3d","4d","5d","6d","7d","8d","9d","1d","Jd","Qd","Kd"]
    hearts = ["Ah","2h","3h","4h","5h","6h","7h","8h","9h","1h","Jh","Qh","Kh"]
    spades = ["As","2s","3s","4s","5s","6s","7s","8s","9s","1s","Js","Qs","Ks"]
    deck = clubs + diamonds + hearts + spades
    for i in range(3):
      deck = self.shuffle_deck(deck)
    return deck


  @staticmethod
  def shuffle_deck(deck):
    ''' Fisher-Yates Algorithm
    '''
    deck_size = deck.__len__()
    # Start from the last element and swap one by one.
    # We dont need to run for the first element, hence why i > 0.
    for i in range(deck_size-1, 0, -1):
      # Pick a random index from 0 to i
      j = randint(0, i+1)
      # Swap arr[i] with element at random index
      deck[i],deck[j] = deck[j],deck[i]
    return deck


  @staticmethod
  def deal(deck: list) -> str:
    card = deck.pop()
    return card
  

  def on_canvas_click(self, event, rect_coords):
    # What did the user click?
    margin = 10
    x1, y1, x2, y2 = rect_coords
    return (x1 - margin <= event.x <= x2 + margin) and (y1 - margin <= event.y <= y2 + margin)
  

  def draw(self):
    self.draw_ui()
    self.draw_cards()


  def draw_cards(self):
    # Draw Players Cards
    

    # Draw Dealers Cards
    ...

  def draw_ui(self):
    if self._state.start_phase == True:
      ...
    if self._state.bet_phase == True:
      ...
    if self._state.round_complete == True:
      ...
    # Draw Deal button
    # Draw Stay Button
    # Draw Double Down Button
    # Draw Place Bet Button
    # Draw Max Bet Button
    # Draw Increase Bet Button
    # Draw Decrease Beet Button
    # Draw Check Cards Button
    # Draw Check Dealers Cards Button
    ...

  def on_deal_btn_click(self,event):
    print("Deal Button Clicked!")
    
  def on_stay_btn_click(self,event):
    print("Stay Button Clicked!")
    
  def on_dbl_down_button_click(self,event):
    print("Double Down Button Clicked!")
    
  def on_place_bet_button_click(self):
    print("Place Bet Button Clicked!")
    
  def on_max_bet_button_click(self):
    print("Place Max Bet Button Clicked!")

  def on_bet_increase_click(self):
    print("Bet Increase Button Clicked!")
    
  def on_bet_decrease_click(self):
    print("Bet Decrease Button Clicked!")
    
  def on_check_cards_click(self):
    print("Check Cards Button Clicked!")
    
  def on_check_dealers_card_click(self):
    print("Check Dealers Cards Button Clicked!")

