import customtkinter as ctk
from Models.commands import Command, ExternalDeviceCommand
from View.game_frame import GameFrame
from View.home_screen import HomeScreen
from View.debug_screen import DebugScreen
from View.app_menu import AppMenu


class ExternalDeviceListener():
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
      GameFrame
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
      

class AppController(ctk.CTk):
  # Subject & Invoker
  def __init__(
    self,
    view: AppView = None,
    title = "HomeLab",
    width = 1000,
    height = 600,
    ) -> None:
    super().__init__()
    self.view: AppView = AppView(self)
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
  