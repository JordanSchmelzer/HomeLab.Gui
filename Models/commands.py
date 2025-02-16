from __future__ import annotations
from abc import ABC, abstractmethod
from View.debug_screen import DebugScreen
from View.home_screen import HomeScreen


class Command(ABC):
  
  @abstractmethod
  def execute(self):
    pass


class HomeCommand(Command):
  def __init__(self, app_controller):
    self._reciever = app_controller

  def execute(self):
    print(f"HomeCommand: Showing Frame {HomeScreen.__name__}")
    self._reciever.show_frame(HomeScreen)
    

class DebugCommand(Command):
  def __init__(self, app_controller):
    self._reciever = app_controller
    
  def execute(self):
    print(f"DebugCommand: Showing Frame {DebugScreen.__name__}")
    self._reciever.show_frame(DebugScreen)
