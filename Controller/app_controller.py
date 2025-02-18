from tkinter import Button
import customtkinter as ctk
from View.app_container import app_view
from Models.commands import Command, ExternalDeviceCommand
from Models.i_event_listener import IEventListener
from typing import List
from View.Styles.button_styles import ButtonStyles


class ExternalDeviceListener(IEventListener):
  def __init__(
    self,
    connection
    ) -> None:
    self.connection = connection
    
  def update(self):
    self.connection


class EventsManager():
  ''' Handle events  '''
  def __init__(self):
    ''' Initialize the dictionary to store listeners for each event type. '''
    self.listeners = {}

  def subscribe(  
    self,
    event_type,
    listener,
    ) -> None:
    ''' Add listener to the event type. '''
    if event_type not in self.listeners:
      self.listeners[event_type] = []
    self.listeners[event_type].append(listener)

  def unsubscribe(
    self,
    event_type,
    listener,
    ) -> None:
    ''' Remove listener from event type. '''
    if event_type not in self.listeners and listener in self.listeners[event_type]:
      self.listeners[event_type].remove(listener)
    
  def notify(
     self,
     event_type,
     data,
     ) -> None:
    ''' Notify all listeners subscribed to the event type '''
    if event_type in self.listeners:
      for listener in self.listeners[event_type]:
        listener.update(data)


class CommandHistory:
  def __init__(self):
    self.history: List[Command] = []
    
  def push(self, c: Command):
    self.history.append(c)
    
  def pop(self) -> Command:
    return self.history.pop()
          

class AppController(ctk.CTk):
  # Subject & Invoker
  def __init__(
    self,
    view: app_view = None,
    title = "HomeLab",
    width = 1000,
    height = 600,
    ) -> None:
    super().__init__()
    self.view: app_view = app_view(self)
    self.history = CommandHistory()
    self.title(title)
    self.geometry(f"{width}x{height}")
    
    if self.view != None:
      self.view.show_start_frame()
   
    self.active_frame: ctk.CTkFrame = None

    # Event Listeners
    self.events = EventsManager()
    self.register_event_listeners()

    # Invoker Commands
    self._on_start = None
    self._on_finish = None
    
  def register_event_listeners(self):
    self.events.subscribe(ExternalDeviceCommand,self.events)

  def execute_command(self, command: Command):
    if isinstance(self._on_start, Command):
      self._on_start.execute()

    if (command.execute()):
      self.history.push(command)
      
    if isinstance(self._on_finish, Command):
      self._on_finish.execute()
      
  ## COMMAND METHODS
  def show_frame(self, frame: ctk.CTkFrame):
    self.view.show_frame(frame)

  def change_background_color(self, frame_id, color):
    frame = self.view.get_frame(frame_id)
    frame.configure(fg_color=color)
  

  def run(self):
    self.mainloop()
  