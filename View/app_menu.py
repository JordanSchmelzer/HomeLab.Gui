import customtkinter as ctk
from Models.commands import HomeCommand
from Models.commands import DebugCommand


class app_menu(ctk.CTkFrame):
  def __init__(
    self,
    parent,
    controller,
    ) -> None:
    super().__init__(
      master=parent,
    )
    self.controller = controller
    self.create_layout()
    self.create_widgets()


  def create_layout(self):
    for row in range(10):
      self.rowconfigure(row,weight=1)
    for col in range(0):
      self.columnconfigure(col,weight=1)
      

  def create_widgets(self):
    self.home_button = ctk.CTkButton(
      master=self,
      text="HomeLab",
      command= lambda: self.home_button_click()
      )
    self.home_button.grid(row=0,column=0,sticky='news',padx=5,pady=5)
 
    self.debug_button = ctk.CTkButton(
      master=self,
      text="Debug",
      command= lambda: self.debug_button_click()
      )
    self.debug_button.grid(row=1,column=0,sticky='news',padx=5,pady=5)
    
    self.placeholder1_button = ctk.CTkButton(
      master=self,
      text="Debug",
      command= lambda: self.placeholder1_button_click()
      )
    self.placeholder1_button.grid(row=2,column=0,sticky='news',padx=5,pady=5)    
    
    self.placeholder2_button = ctk.CTkButton(
      master=self,
      text="Debug",
      command= lambda: self.placeholder2_button_click()
      )
    self.placeholder2_button.grid(row=3,column=0,sticky='news',padx=5,pady=5)
  

  def home_button_click(self):
    self.controller.execute_command(HomeCommand(self.controller))


  def debug_button_click(self):
    self.controller.execute_command(DebugCommand(self.controller))
    

  def placeholder1_button_click(self):
    self.controller.execute_command(DebugCommand(self.controller))
     
    
  def placeholder2_button_click(self):
    self.controller.execute_command(DebugCommand(self.controller))
    