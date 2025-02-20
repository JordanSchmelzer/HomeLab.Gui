import customtkinter as ctk


class AddRemoveDeviceWidget(ctk.CTkFrame):
  def __init__(self, master, controller) -> None:
    self._master = master
    self._controller = controller
    super().__init__(master=master)
    self._create_widgets()


  def _create_grid(self) -> None:
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)


  def _create_widgets(self) -> None:
    self._create_grid()

    self.add_button = ctk.CTkButton(master=self,text="Add",
      command= lambda: ...)
    self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky='news')
    
    self.remove_button = ctk.CTkButton(master=self,text="Remove",
      command= lambda: ...)
    self.remove_button.grid(row=0,column=1,padx=5,pady=5, sticky='news')


class DevicesPanel(ctk.CTkScrollableFrame):
  def __init__(self, master, controller ) -> None:  
    self._controller = controller
    self._master = master
    super().__init__(
      master=master,
      orientation="vertical",
      label_text="Managed Devices",
      )
    
    self._create_widgets()

  def _create_widgets(self) -> None:
    
    self.add_remove_cmds = AddRemoveDeviceWidget(master=self, controller=self._controller)
    self.add_remove_cmds.pack()    

    for x in range(20):
      filler = ctk.CTkButton(master=self)
      filler.pack()


  def add_widget(self) -> None:
    ...
    

  def remove_widget(self) -> None:
    ...
