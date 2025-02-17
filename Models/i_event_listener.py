from __future__ import annotations
from abc import ABC, abstractmethod


class IEventListener(ABC):
  
  @abstractmethod
  def update():
    ...  
