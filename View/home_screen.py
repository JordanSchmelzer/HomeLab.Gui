import customtkinter as ctk
from View.devices import DevicesPanel


class HomeScreen(ctk.CTkFrame):
  def __init__(
      self,
      parent: ctk.CTkFrame,
      controller):
    super().__init__(master=parent,)
    self._controller = controller
    
    self._create_widgets()
    

  def _setup_grid(self):
    for row in range(10):
      self.rowconfigure(row,weight=1)
    for col in range(10):
      self.columnconfigure(col,weight=1)
    

  def _create_widgets(self):
    self._setup_grid()    

    self.label = ctk.CTkLabel(self, text="HomeScreen")
    self.label.grid(row=0,column=0,sticky='news')
    
    self.devices = DevicesPanel(self, self._controller)
    self.devices.grid(row=1,column=0, padx=5,pady=5,sticky='news')
    