import customtkinter as ctk
from Models.commands import ShowFrameCommand
from View.home_screen import HomeScreen
from View.debug_screen import DebugScreen
from View.game_frame import GameFrame


class AppMenu(ctk.CTkFrame):
  def __init__(self,parent,controller) -> None:
    super().__init__(master=parent)
    self.controller = controller
    self.create_widgets()

  def create_widgets(self):
    for row in range(10):
      self.rowconfigure(row,weight=1)
    self.columnconfigure(0,weight=1)    
    
    self.home_button = ctk.CTkButton(
      master=self,
      text="Device Manager",
      command= lambda: self.home_button_click())
    self.home_button.grid(row=0,column = 0,sticky='news',padx=5,pady=5)
    

    self.placeholder1_button = ctk.CTkButton(
      master=self,
      text="Cards", command= lambda: self.game_button_click())
    self.placeholder1_button.grid( row=2,column = 0,sticky='news',padx=5,pady=5)    
 

    self.debug_button = ctk.CTkButton(
      master=self,
      text="Debug Button",
      command= lambda: self.debug_button_click())
    self.debug_button.grid(row=1,column = 0,sticky='news',padx=5,pady=5)


  def home_button_click(self):
    self.controller.execute_command(ShowFrameCommand(self.controller, HomeScreen))

  def debug_button_click(self):
    self.controller.execute_command(ShowFrameCommand(self.controller, DebugScreen))
    
  def game_button_click(self):
    self.controller.execute_command(ShowFrameCommand(self.controller, GameFrame))

    