import customtkinter as ctk
from View.app_container import app_view
from Models.commands import Command
from typing import List


class CommandHistory:
  def __init__(self):
    self.history: List[Command] = []
    
  def push(self, c: Command):
    self.history.append(c)
    
  def pop(self) -> Command:
    return self.history.pop()
          

class AppController(ctk.CTk):
  def __init__(
    self,
    view = None,
    ) -> None:
    super().__init__()
    self.view: app_view = app_view(self)
    self.history = CommandHistory()
    self.title("HomeLab")
    self.geometry("600x600")
    
    if self.view != None:
      self.view.show_start_frame()

    self._on_start = None
    self._on_finish = None


  def show_frame(self, frame: ctk.CTkFrame):
    self.view.show_frame(frame)


  def execute_command(self, command: Command):
    if isinstance(self._on_start, Command):
      self._on_start.execute()

    if (command.execute()):
      self.history.push(command)
      
    if isinstance(self._on_finish, Command):
      self._on_finish.execute()


  def run(self):
    self.mainloop()
  