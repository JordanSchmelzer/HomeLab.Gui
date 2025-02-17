from __future__ import annotations
from abc import ABC, abstractmethod


class IUiSubscriber(ABC):

  @abstractmethod
  def update(context):
    ...
