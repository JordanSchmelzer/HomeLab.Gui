from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
  ''' The Command interface declares a method
  '''
  
  @abstractmethod
  def execute(self) -> None:
    pass


class SimpleCommand(Command):
  ''' Some commands can implement simple operations on their own.
  '''
  def __init__(self, payload: str) -> None:
    self._payload = payload
    
  def execute(self) -> None:
    print("Simple Command")
  
    
class ComplexCommand(Command):
  ''' Some commands can delegate more complex operations to other
    objects, called "receivers."
  '''

  def __init__(self, receiver: Receiver, some_arg):
    '''
    Complex commands can accept one or several receiver objects along
    with any context data via the constructior.
    '''
    
    self._receiver = receiver
    self._some_arg = some_arg
    
  def execute(self):
    ''' Commands can delegate to any methods of a reciever.
    '''
    print("ComplexCommand: complex stuff done by a reciever")
    self._reciever.do_something()


class Receiver:
  '''
  The Receiver classes contain some important business logic. They know how to
  perform all kinds of operations, associated with carrying out a request. In
  fact, any class may serve as a Receiver.
  '''
  
  def do_something():
    ...
  
class Invoker:
  '''
  The Invoker is associated with one or several commands. It sends a request
  to the command.
  '''
  _on_start = None
  _on_finish = None
  
  # Init commands
  def set_on_start(self,command:Command):
    self._on_start = command
    
  def set_on_finish(self,command:Command):
    self._on_finish = command
    
  def do_something(self):
    '''
    The Invoker does not depend on concrete command or reciever class.
    The Invoker passes a request to the reciever indireclty by executing
    a command.
    '''
    print("Invoker: Is there something to do before I do something?")
    if isinstance(self._on_start, Command):
      self._on_start.execute() 
      
    print("Invoker: doing something")
    
    print("Invoker: Anything to do at the end.")
    if isinstance(self._on_finish, Command):
      self._on_finish.execute()
      
if __name__ == "__main__":
  ''' The Client code can parameterize an invoker with any commands.
  '''
  invoker = Invoker()
  invoker.set_on_start(SimpleCommand())
  receiver = Receiver()
  invoker.set_on_finish(ComplexCommand(receiver,"some arg"))
  
  invoker.do_something()
  