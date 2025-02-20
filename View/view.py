import customtkinter as ctk
from View.home_screen import HomeScreen
from View.debug_screen import DebugScreen
from View.app_menu import AppMenu


class AppView(ctk.CTkFrame):
  def __init__(
    self,
    parent,
    ) -> None:
    super().__init__(master=parent)
    self.configure_layout()
    self.controller = parent
    self.frames = {}
    self.add_frames()
    
    self.pack(side="top",fill="both",expand=True)    

  def configure_layout(self):
    for row in range(10):
      self.rowconfigure(row,weight=1)
    for col in range(10):
      self.columnconfigure(col,weight=1)

  def add_frames(self):
    self.menu = AppMenu(self, self.controller)
    self.menu.grid(
      row=0, rowspan=10, 
      column=0, columnspan=1,
      padx=5, pady=5, sticky='news')

    for F in (
      HomeScreen,
      DebugScreen,
      ):
      frame = F(self, self.controller)
      self.frames[F] = frame
      frame.grid(
        row=0,rowspan=10,
        column=1, columnspan=9,
        padx=5,pady=5, sticky='news'
        )

  def show_frame(self, frame):
    _frame = self.frames[frame]
    _frame.tkraise()

  def get_frame(self, frame):
    return self.frames[frame]

  def show_start_frame(self):
    self.show_frame(HomeScreen)
      