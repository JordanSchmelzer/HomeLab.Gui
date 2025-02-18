import customtkinter as ctk
from Models.i_ui_subscriber import IUiSubscriber
from View.Styles.button_styles import ButtonStyles
from Models.commands import ChangeBackgroundCommand
import random
import threading
import time


class ThreadWidget():
  def __init__(self):
    ...
    

class DebugScreen(ctk.CTkFrame, IUiSubscriber):
  def __init__(
      self,
      parent,
      controller,
      ) -> None:
    super().__init__(
      master=parent,
      )
    self.setup_grid()
    self.create_widgets()
    self.controller = controller


  def setup_grid(self):
    for row in range(10):
      self.rowconfigure(row,weight=1)
    for col in range(10):
      self.columnconfigure(col,weight=1)
      

  def create_widgets(self):
    
    self.random_bg_button = ctk.CTkButton(
      self,
      text="Random Color Bg",
      command=lambda: self.button_click())
    self.random_bg_button.grid(
      row=0,column=0, 
      padx=5,pady=5,sticky='news')
    ButtonStyles.apply_styles(self.random_bg_button)
    

    self.toggle_button_on_state = False
    self.toggle_button=ctk.CTkButton(
      self,
      text="ToggleButton",
      command=lambda: self.toggle_button_click(self.toggle_button),
      )
    self.toggle_button.grid(
      row=0,column=1,
      padx=5,pady=5,sticky='news')
    ButtonStyles.apply_styles(self.toggle_button)
    print(self.toggle_button._fg_color)



  def toggle_button_click(self, widget: ctk.CTkBaseClass):
    if not self.toggle_button_on_state:
      self.toggle_button_on_state = True
      T = threading.Thread(
        target=self.thread_pulse_element,
        args=[widget])
      T.start()
    else:
      self.toggle_button_on_state = False
      
  def thread_pulse_element(
    self,
    widget = ctk.CTkBaseClass,
    color: str = "#C1666B",
    on_pulse_width_ms = 1000
    ) -> None:
    ''' Pulse Effect
      Summary:
      While remaining conscious of performance, alternate between
      a primary and secondary color for some duration. Check the class
      flag every 50 ms. This gives a responsive reset to the button
      quickly after its been pressed.
    '''
    base_color = "steelblue2"
    counter = 0
    color_on = True
    while self.toggle_button_on_state:
      if counter <= on_pulse_width_ms:
        if color_on:
          widget.configure(fg_color=color)
        else:
          widget.configure(fg_color=base_color)
      else:
        counter = 0
        if color_on:
          color_on = False
        else:
          color_on = True
      counter+=50
      time.sleep(.05)
    # Reset to starting color.
    widget.configure(fg_color=base_color)


  def button_click(self):
    self.controller.execute_command(
      ChangeBackgroundCommand(
        app_controller=self.controller,
        frame_id=self.__class__,
        color=self.generate_random_hex_color()
      )
    )
    
  def generate_random_hex_color(self) -> str:
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number = '#' + hex_number[2:].zfill(6)
    print(hex_number)
    return str(hex_number)
