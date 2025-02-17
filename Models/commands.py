from __future__ import annotations
from abc import ABC, abstractmethod
import customtkinter as ctk


class Command(ABC):
  
  @abstractmethod
  def execute(self):
    pass


class ShowFrameCommand(Command):
  def __init__(
    self,
    app_controller,
    frame: ctk.CTkFrame,
    ) -> None:
    self._reciever = app_controller
    self._frame = frame
    
  def execute(self):
    print(f"ShowFrameCommand: Showing Frame {self._frame.__name__}")
    self._reciever.show_frame(self._frame)


class ChangeBackgroundCommand(Command):
  def __init__(
    self,
    app_controller,
    frame_id,
    color: str
    ) -> None:
    self._reciever = app_controller
    self._color = color
    self._frame = frame_id

  def execute(self):
    print(
      f"ChangeBackgroundCommand: Changing frame background from {self._frame} to {self._color}"
      )
    self._reciever.change_background_color(self._frame, self._color)

class ExternalDeviceCommand(Command):
  ''' Some command specific to a device. '''
  def __init__(
    self,
    app_controller
    ) -> None:
    self._reciever = app_controller
    
  def execute(self, command):
    print(f"ExternalDeviceCommand: {command}")
    # self._reciever.
    