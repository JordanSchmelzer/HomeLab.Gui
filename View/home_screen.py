import customtkinter as ctk


class HomeScreen(ctk.CTkFrame):
  def __init__(
      self,
      parent: ctk.CTkFrame,
      controller):
    super().__init__(
      master=parent
      )
    self.controller = controller
    self.setup_grid()
    self.create_widgets()
    

  def setup_grid(self):
    for row in range(10):
      self.rowconfigure(row,weight=1)
    for col in range(10):
      self.columnconfigure(col,weight=1)
    

  def create_widgets(self):
    for row in range(2):
      for col in range(2):
        button = ctk.CTkButton(self, text=f'r.{row}, c.{col}')
        button.grid(row=row,column=col, sticky='news')
    