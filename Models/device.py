import socket
import threading
import queue
import select
import time
from queue import Queue
from Controller.app_controller import EventsManager
from Models.i_event_listener import IEventListener
from Models.commands import ShowFrameCommand
from abc import ABC, abstractmethod


class IThreadObserver(ABC):
  @abstractmethod
  def update(self, message):
    ...    

class IMessage(ABC):
  def __init__(self,message) -> None:
    ...
    
  @abstractmethod
  def ok(self):
    ...
    
  @abstractmethod
  def execute(self):
    ...

class ByteOrientedMessage(IMessage):
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
    
  def execute():
    ...
    
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

class MessageRecievedListener(IEventListener):
  
  def __init__(
  self,
  gui_controller,
  ) -> None:
    self._reciever = gui_controller
  '''
  This thing gets an update and decides what to do.
  '''
  def _process_message(data: IMessage):
    return True if data.ok() else False

  def update(self, data):
    if self._process_message():
      self._reciever.execute_command(
        ShowFrameCommand(self._reciever,data))

class TcpDevice():
  '''  '''
  def __init__(
    self,
    controller,
    host:str='localhost',
    port:int=50001,
    ) -> None:
    self._controller = controller
    self._host = host
    self._port = port
    
    self._events = MessageManager()
    self._events.subscribe(ByteOrientedMessage,MessageRecievedListener(self._controller))
    
    self._messages = Queue(10)
    self._message_producer = ThreadByteOrientedMessageListener(
      queue=self._messages,
      host = self._host,
      port= self._port,)
    self._message_worker = ThreadMessageQueueWorker(
      message_queue=self._messages,
      events=self._events,)
    
  def listen(self):
    self._message_producer.start()
    self._message_worker.start()

  def stop(self):
    self._message_producer.stop()
    self._message_worker.stop()
    
class ThreadByteOrientedMessageListener(threading.Thread):
  def __init__(
  self,
  queue: queue.Queue,
  host: str,
  port: int,
  ) -> None:
    super().__init__()
    self._queue = queue
    self._stop_event = threading.Event()
    self._stopped = threading.Event()
    self._port = port
    self._host = host
    
  def run(self):
    self._stop_event.clear()
    sock = None
    
    while not self._stop_event.is_set():
      try:
        if sock == None:
          sock = self.get_socket()

        ...

        time.sleep(1)
      except socket.error:
        sock = None
        
    self._stopped.set()       
      
  def stop(self):
    self._stop_event.set()
    self._stop_event.wait()

  def start(self):
    if not self.is_alive():
      self._stop_event.clear()
      super().start()
    
  def get_socket(self) -> socket.socket:
    try:
      sock = socket.socket(
        family = socket.AF_INET,
        type = socket.SOCK_STREAM,)
      addr = (self._host, self._port)
      sock.connect(addr)
      print(f"Connected to {self._host} on port {self._port}")
      return sock
    except socket.error as e:
      print(f'socket error: {e}')
      return None

  def clear_socket(
    self,
    sock: socket.socket,
    buffer_size = 4096,
    timeout = 0.5,
    ) -> None:
    print("Clearing socket buffer of bytes.")
    while True:
      try:
        readable, _, _ = select([sock],[],[], timeout)
        if readable:
          data = sock.recv(buffer_size)
          if not data:
            print("Socket buffer is clear.")
            break
          else:
            print(f"Read {len(data)} bytes from the socket.")
        else:
          print("Socket buffer is clear.")
          break
      except socket.error as e:
        print(f"clear_socket error: {e}")
        break
  
class ThreadMessageQueueWorker(threading.Thread):
  ''' Observer Event Producer
    Worker Thread Responsible For Processing Message Queue.
    Produce Events Based On Message Contents.
  '''
  def __init__(
    self,
    message_queue: queue.Queue,
    listeners
    ) -> None:
    super().__init__()
    self._message_queue = message_queue
    self._stop_event = threading.Event()
    self._stopped = threading.Event()
    self._listeners: EventsManager = listeners

  def run(self):
    self._stopped.clear()
    while not self._stop_event.is_set():
      try:
        message: IMessage = self._message_queue.get()
        
        ## Do some stuff with the message
        ## Might even send data to other listeners as needed
        self._listeners.notify(MessageRecievedListener, message)
        
      except queue.Empty:
        continue
    self._stopped.set()

  def stop(self):
    self._stop_event.set()
    self._stopped.wait()
  
  def start(self):
    if not self.is_alive():
      self._stop_event.clear()
      super().start()
      
