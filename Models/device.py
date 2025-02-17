import socket
import threading
from queue import Queue
from Models.i_event_listener import IEventListener
from Models.commands import ShowFrameCommand


class ThreadByteStreamCommunication:
  # This would watch the thread and raises communication events
  # It does that by putting a message into a queue
  # Then a worker therad processes messages in the queue.
  # Messages can be good or bad, the queue needs to take care of what to do
  ...


class ThreadEventWorker:
  # This worker queue determines what to do with a message.
  # typically this will be trigering an event
  ''' Probably something like this.
    prop device = RemoteDevice
    prop events = x.events_manager
    
    q = device.queue.pop()
    message = q.get()
    if message.ok():
      events.notify("message")
  '''
  ...


class Message():
  # This is a message from the socket
  # There is a validate method called ok()
  # Other functions can determine what to do with that.
  def __init__(
    self,
    message
    ) -> None:
    self._message = message
    self._message_code
    self._message_code_desc
    
  def ok(self) -> bool:
    # There could be some c
    match self._message:
      case "hello":
        self._message_code = 200
        self._message_code_desc = "Hello"
        return True
      case _:
        self._message_code = 400
        self._message_code_desc = "invalid"
        return False
      


class GuiCommandRequestListener(IEventListener):
  # Listen for an event that needs the gui to do something.
  def __init__(
  self,
  gui_controller,
  ) -> None:
    self._reciever = gui_controller

  def update(self, data):
    self._reciever.execute_command(
      ShowFrameCommand(self._reciever,data))
    

class MessageManager():
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


class RemoteDevice():
  # Is a Publisher
  def __init__(
    self,
    host:str='localhost',
    port:int=50001,
    device_type:str="Generic Device",
    ) -> None:
    self._host = host
    self._port = port
    self._device_type = device_type
    
    self.events = MessageManager()
    self.events.subscribe(
      "",GuiCommandRequestListener)
    
    self.messages = []

  def get_socket(self) -> socket.socket:
    try:
      sock = socket.socket(
        family = socket.AF_INET,
        type = socket.SOCK_STREAM,
      )
      addr = (self._host, self._port)
      sock.connect(addr)
      print(f"Connected to {self._host} on port {self._port}")
      return sock
    except socket.error as e:
      print(f'socket error: {e}')
      return None
    
