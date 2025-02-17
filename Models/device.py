import socket
from queue import Queue
from Models.i_event_listener import IEventListener
from Models.commands import ShowFrameCommand


class DataEventManager(IEventListener):
  
  
  def update():
    ...



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
    
    self.subscribers = {}
    
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
    
