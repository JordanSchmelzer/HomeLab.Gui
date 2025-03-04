import customtkinter as ctk
from random import randint
import time
from dataclasses import dataclass


@dataclass
class GameState:
  deck = []
  player_hand = []
  dealer_hand = []
  player_bet = 0
  player_bank = 200000
  max_bet = 5000
  current_bet = 0
  doubled_down = False
  bets_placed = False
  show_face_down_card = False
  dealer_dealt = False
  player_stay = False
  game_over = False
  dealt_rounds = 0
  command_slots = {}
  dealer_stands_at = 17


class GameFrame(ctk.CTkFrame):
  def __init__(self, parent, controller):
    super().__init__(master=parent)
    self._controller = controller
    self.rowconfigure(0,weight=1)
    self.columnconfigure(0,weight=1)

    self._state = GameState()
    self._state.deck = self.new_deck()
   
    self._canvas = ctk.CTkCanvas(self, bg='white',height=500,width=500,bd=3,relief='groove')

    self._canvas.grid(row=0,column=0, padx=5,pady=5)
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
    deck_size = deck.__len__() - 1
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
  

  def on_canvas_click(self, event):
    # rect = x1, y1, x2, y2
    # Controls Clicked?
    for slot in self._state.command_slots:
      if self.is_inside_rect(event, self._state.command_slots[slot]["coords"]):
        self._state.command_slots[slot]["func"]()


  def draw(self):
    self._canvas.delete('all')
    self.draw_ui()
    self.draw_cards()


  def draw_cards(self):
    # Draw the deck
    card_width = 75
    card_ratio = 3.5 / 2.5
    card_height = card_width * card_ratio
    self._canvas.create_rectangle((0,0),(card_width,card_height), fill='purple', tags=["deck"])    

    # Draw Dealers Cards
    padx = 20
    pady = 50
    y1 = 250 - card_height - 20
    y2 = y1 + card_height
    start_x = 100
    for index in range(self._state.dealer_hand.__len__()):
      #print(self._state.dealer_hand.__len__(), index)
      x1 = start_x + (index * card_width) + (padx * index)
      coords = (x1, y1, x1+card_width, y2),
      #print(f"x1:{x1} y1:{y1} x2:{x1+card_width} y2:{y2}")

      if index == 0 and not self._state.show_face_down_card:
        # You just see the back of the card
        self._canvas.create_rectangle(coords,fill="purple")
      else:
        self._canvas.create_rectangle(coords,fill="white")
        
    # Draw Players Cards
    padx = 20
    pady = 10
    y1 = 270
    y2 = y1 + card_height
    start_x = 100
    for index in range(self._state.player_hand.__len__()):
      x1 = start_x + (index * card_width) + (padx * index)
      coords = (x1, y1, x1+card_width, y2),
      #print(f"x1:{x1} y1:{y1} x2:{x1+card_width} y2:{y2}")
      card: str = self._state.player_hand[index]
      self._canvas.create_rectangle(coords,fill="white")
      
      # Draw Suit
      if card[1] == "c":
        x = x1 + 5
        y = y1 + 20
        size = 10
        # Draw the three circles of the club
        circle_radius = size // 3
        # Top Oval
        self._canvas.create_oval(x - circle_radius - 5, y - circle_radius - 5 , x + circle_radius, y + circle_radius - 5, fill='black')
        # Left Oval
        self._canvas.create_oval(x - size//2, y - size//2 - circle_radius, x - size//2 + 2 * circle_radius, y - size//2 + 2 * circle_radius, fill='black')
        # Right Oval
        self._canvas.create_oval(x + size//2 - 2 * circle_radius, y - size//2 - circle_radius, x + size//2, y - size//2 + 2 * circle_radius, fill='black')

        # Draw the stem of the club
        self._canvas.create_rectangle(x - size // 10, y, x + size // 10, y + size // 2, fill='black')
        
      elif card[1] == "d":
        # Draw Diamonds
        # Calculate the points for the diamond shape
        x = x1 + 5
        y = y1 + 20
        size = 10
        points = [
            x, y + size // 4,
            x + size // 2, y - size // 2,
            x + size, y + size // 4,
            x + size // 2, y + size,
        ]
        self._canvas.create_polygon(points, fill='red', smooth=False)
        
        x = x1 + card_width - 5 - size
        y = y2 - 15 - size
        size = 10
        points = [
            x, y + size // 4,
            x + size // 2, y - size // 2,
            x + size, y + size // 4,
            x + size // 2, y + size,
        ]
        self._canvas.create_polygon(points, fill='red', smooth=False)
        
      elif card[1] == "h":
        size = 10
        x = x1 + 5
        y = y1 + 20
        # Calculate the points for the heart shape
        top_left = x - size // 2, y - size // 4
        top_right = x + size // 2, y - size // 4
        bottom = x, y + size // 2
    
        # Create the left half of the heart
        self._canvas.create_arc(top_left[0], top_left[1], top_right[0], y + size // 4, start=0, extent=180, style=ctk.ARC)
    
        # Create the right half of the heart
        self._canvas.create_arc(top_left[0], top_left[1], top_right[0], y + size // 4, start=180, extent=180, style=ctk.ARC)
    
        # Draw the bottom triangle of the heart
        points = [
            top_left[0], y,
            top_right[0], y,
            bottom[0], bottom[1]
        ]
        self._canvas.create_polygon(points, fill='red')
        
      elif card[1] == "s":
        size = 10
        x = x1 + 5
        y = y1 + 20
        # Coordinates for the spade shape
        spade_coords = [
            x, y,
            x - size * 0.5, y + size * 0.6,
            x, y + size,
            x + size * 0.5, y + size * 0.6,
            x, y
        ]
        # Coordinates for the spade stem
        stem_coords = [
            x - size * 0.1, y + size,
            x + size * 0.1, y + size,
            x + size * 0.1, y + size * 1.4,
            x - size * 0.1, y + size * 1.4
        ]
        # Draw the spade shape
        self._canvas.create_polygon(spade_coords, fill='black', smooth=True)
        # Draw the stem of the spade
        self._canvas.create_polygon(stem_coords, fill='black')

      # Draw Value
      self._canvas.create_text(x1 + 10, y1 + 10, text=card[0] if card[0] !="1" else "10", anchor='c')
      self._canvas.create_text((x1 + card_width) - 10, y2 - 10, text=card[0] if card[0] !="1" else "10", anchor='c')


  def draw_ui(self):
    self._state.command_slots = {}
    padx = 20
    pady = 10
    width = 100
    y1 = 420
    y2 = 500
    start_x = 0

    # Score Box, Current Bet
    if self._state.bets_placed:
      self._canvas.create_text(450,10,text=f"Bet: {self._state.current_bet}", anchor='c')
    else:
      self._canvas.create_text(250,350,text=f"Your Bet: {self._state.current_bet}",anchor='c')
    
    # Line that splits board
    self._canvas.create_line((0,250),(500,250),dash=1)

    for slot_num in range(5):
      x1 = start_x + (slot_num * width) + (padx * slot_num)
      self._state.command_slots.update({
        slot_num: {
          "coords": (x1, y1, x1 + width, y2),
          "func": None
          }
        })

    if not self._state.bets_placed:
      # Draw Place Bet Button
      index = 0
      x1, y1, x2, y2 = self._state.command_slots[index]["coords"]
      self._state.command_slots[index]["func"] = self.on_place_bet_button_click
      self._canvas.create_rectangle((x1,y1,x2,y2), fill='#04a5e5', tags=["controls","place_bet_button"])
      self._canvas.create_text((x1 + ((x2 - x1)/2),y1 + ((y2 - y1) / 2)), text="Enter Bet", anchor='c', tags=["place_bet_button"])
      
      # Draw Max Bet Button
      index = 1
      x1, y1, x2, y2 = self._state.command_slots[index]["coords"]
      self._state.command_slots[index]["func"] = self.on_max_bet_button_click
      self._canvas.create_rectangle((x1,y1,x2,y2), fill='#df8e1d', tags=["controls","max_bet_button"])
      self._canvas.create_text((x1 + ((x2 - x1)/2),y1 + ((y2 - y1) / 2)), text="Max Bet", anchor="c", tags=["max_bet_button"])      

      # Draw Increase Bet Button
      index = 2
      x1, y1, x2, y2 = self._state.command_slots[index]["coords"]
      self._state.command_slots[index]["func"] = self.on_bet_increase_click
      self._canvas.create_rectangle((x1,y1,x2,y2), fill='#40a02b', tags=["controls","increase_bet_button"])
      self._canvas.create_text((x1 + ((x2 - x1)/2),y1 + ((y2 - y1) / 2)), text="Raise Bet", anchor="c", tags=["increase_bet_button"])
      
      # Draw Decrease Beet Button
      index = 3
      x1, y1, x2, y2 = self._state.command_slots[index]["coords"]
      self._state.command_slots[index]["func"] = self.on_bet_decrease_click
      self._canvas.create_rectangle((x1,y1,x2,y2), fill='#e64553', tags=["controls","decrease_bet_button"])
      self._canvas.create_text((x1 + ((x2 - x1)/2),y1 + ((y2 - y1) / 2)), text="Lower Bet", anchor="c", tags=["decrease_bet_button"])

    if self._state.bets_placed:
      # Draw Stay Button
      index = 0 
      x1, y1, x2, y2 = self._state.command_slots[index]["coords"]
      self._state.command_slots[index]["func"] = self.on_stay_btn_click
      self._canvas.create_rectangle((x1,y1,x2,y2), fill='green', tags=["controls","stay_button"])
      self._canvas.create_text((x1 + ((x2 - x1)/2),y1 + ((y2 - y1) / 2)), text="Stay", anchor="c", tags=["stay_button"])

      # Draw Hit Button
      index = 1
      x1, y1, x2, y2 = self._state.command_slots[index]["coords"]
      self._state.command_slots[index]["func"] = self.on_deal_btn_click
      self._canvas.create_rectangle((x1,y1,x2,y2), fill='#dd7878',tags=["controls","hit_button"])
      self._canvas.create_text((x1 + ((x2 - x1)/2),y1 + ((y2 - y1) / 2)), text="Hit", anchor="c", tags=["hit_button"])

    if self._state.dealer_dealt and self._state.dealt_rounds <= 2:
      # Draw Double Down Button
      index = 2
      x1, y1, x2, y2 = self._state.command_slots[index]["coords"]
      self._state.command_slots[index]["func"] = self.on_dbl_down_button_click
      self._canvas.create_rectangle((x1,y1,x2,y2), fill='red', tags=["controls","double_down_button"])
      self._canvas.create_text((x1 + ((x2 - x1)/2),y1 + ((y2 - y1) / 2)), text="Double Down", anchor="c", tags=["double_down_button"])
    
    if self._state.game_over:
      ...


  def is_inside_rect(self, event, button_cords) -> bool:
    margin = 10 # Margin to consider near the rectangle
    x1, y1, x2, y2 = button_cords
    return (x1 - margin <= event.x <= x2 + margin) and (y1 - margin <= event.y <= y2 + margin)


  @staticmethod
  def get_hand_value(hand:list) -> int:
    aces = 0
    value = 0
    for card in hand:
      match card[0]:
        case "A":
          # We'll determine the value last.
          aces += 1
        case "J":
          value+=10
        case "Q":
          value+=10
        case "K":
          value+=10
        case "1":
          value+=10
        case _:
          value+=int(card[0])
    for ace in range(aces):
      if 11 + value > 21:
        value +=1
      else:
        value +=11
    return value


  def on_deal_btn_click(self):
    print("Deal Button Clicked!")
    initial_count = self._state.player_hand.__len__()
    self._state.player_hand.append(self.deal(self._state.deck))
    self.draw()
    time.sleep(.2)    
    if self.get_hand_value(self._state.player_hand) >= 21:
      self.determine_winner()
      return

    assert self._state.player_hand.__len__() == initial_count + 1    
    for card in self._state.player_hand:
      assert card != None


  def next_round(self):
    # Shuffle the dealer and players cards back into the deck
    while self._state.player_hand:
      card = self._state.player_hand.pop()
      self._state.deck.append(card)
    while self._state.dealer_hand:
      card = self._state.dealer_hand.pop()
      self._state.deck.append(card)
    self.shuffle_deck(self._state.deck)
    # Reset relevant state flags
    self._state.current_bet = 0
    self._state.dealt_rounds = 0
    self._state.bets_placed = False
    self._state.doubled_down = False
    self._state.show_face_down_card = False
    self._state.game_over = False
    self._state.dealer_dealt = False
    # Redraw the screen
    self.draw()


  def determine_winner(self):
    dealer_hand_val = self.get_hand_value(self._state.dealer_hand)   
    player_hand_val = self.get_hand_value(self._state.player_hand)

    # determine if dealer win or lose
    if dealer_hand_val > 21 | dealer_hand_val < player_hand_val:
      # Dealer Bust / Player Win
      self._state.player_bank += self._state.current_bet
      if self._state.doubled_down:
        self._state.player_bank += self._state.current_bet
      
    if dealer_hand_val == player_hand_val:
      # Push
      ...
      
    if dealer_hand_val > player_hand_val:
      # Dealer Win
      self._state.player_bank -= self._state.current_bet
      if self._state.doubled_down:
        self._state.player_bank -= self._state.current_bet
      
    self.next_round()


  def on_stay_btn_click(self):
    print("Stay Button Clicked!")
    # Flip the hidden card and show player
    self._state.show_face_down_card = True
    self._draw()
    # Dealer draws until stay
    dealer_hand_val = self.get_hand_value(self._state.dealer_hand)
    while dealer_hand_val < self._state.dealer_stands_at:
      self._state.dealer_hand.append(self.deal(self._state.deck))
      dealer_hand_val = self.get_hand_value(self._state.dealer_hand)
      if dealer_hand_val <= self._state.dealer_stands_at:
        break
    self.determine_winner()
          

  def on_dbl_down_button_click(self):
    print("Double Down Button Clicked!")
    assert self._state.dealt_rounds <= 2
    assert self._state.player_bank - (self._state.current_bet * 2) >= 0
    self._state.doubled_down = True

    
  def on_place_bet_button_click(self):
    if not self._state.current_bet > 0:
      return

    # When bets placed, deal a card to player then dealer
    self._state.bets_placed = True
    # Update the UI Elements
    self.draw()
    # Deal to the dealer
    self._state.dealer_hand.append(self.deal(self._state.deck))
    time.sleep(0.1)
    self.draw()
    # Deal to the player
    self._state.player_hand.append(self.deal(self._state.deck))
    time.sleep(0.1)
    self.draw()
    # Deal to the dealer
    self._state.dealer_hand.append(self.deal(self._state.deck))
    time.sleep(0.1)
    self.draw()
    

  def on_max_bet_button_click(self):
    print("Place Max Bet Button Clicked!")
    self._state.current_bet = 5000
    self.draw()


  def on_bet_increase_click(self):
    print("Bet Increase Button Clicked!")
    
    if self._state.current_bet >= self._state.max_bet:
      return
    
    if 0 <= self._state.current_bet <100:
      self._state.current_bet+=10
      
    if 100 <= self._state.current_bet <500:
      self._state.current_bet+=50
      
    if 500<= self._state.current_bet <5000:
      self._state.current_bet+=500
    self.draw()
    

  def on_bet_decrease_click(self):
    print("Bet Decrease Button Clicked!")
    
    if self._state.current_bet == 0:
      return
    
    if 0 <= self._state.current_bet <100:
      self._state.current_bet-=10
      
    if 100 <= self._state.current_bet <500:
      self._state.current_bet-=50
      
    if 500<= self._state.current_bet <=5000:
      self._state.current_bet-=500
    
    self.draw()
    