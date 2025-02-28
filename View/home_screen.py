import customtkinter as ctk


class OkButton():
  def apply_styles(widget: ctk.CTkButton):
    widget.configure(
      fg_color='#04AA6D',
      font=('System',20))

class NOkButton():
  def apply_styles(widget: ctk.CTkButton):
    widget.configure(
      fg_color="#f44336",
      font=('System',20))


class HomeScreen(ctk.CTkFrame):
  def __init__(
      self,
      parent: ctk.CTkFrame,
      controller):
    super().__init__(master=parent,)
    self._controller = controller
    self._create_widgets()
  
  def _create_widgets(self):
    for row in range(10):
      self.rowconfigure(row,weight=1)
    for col in range(10):
      self.columnconfigure(col,weight=1)

    label = ctk.CTkLabel(self, text="Jordans Device Management", font=("System", 24))
    label.grid(row=0, columnspan=10, column=0,sticky='news')
    
    # Device Panel
    device_panel = ctk.CTkScrollableFrame(self, label_text="Device Management")
    device_panel.grid(row=1, rowspan=9, column=0, padx=5,pady=5,sticky='news')

    # Device Panel -> Add / Remove Buttons
    add_remove_device_widget = ctk.CTkFrame(master=device_panel)
    add_remove_device_widget.rowconfigure(0, weight=1)
    add_remove_device_widget.columnconfigure(0, weight=1)
    add_remove_device_widget.columnconfigure(1, weight=1)

    add_button = ctk.CTkButton(master=add_remove_device_widget,text="Add", command= lambda: ...)
    add_button.grid(row=0, column=0, padx=5, pady=5, sticky='news')
    OkButton.apply_styles(add_button)
    
    remove_button = ctk.CTkButton(master=add_remove_device_widget,text="Remove", command= lambda: ...)
    remove_button.grid(row=0,column=1,padx=5,pady=5, sticky='news')
    NOkButton.apply_styles(remove_button)

    add_remove_device_widget.pack()

    # Device Panel -> Device List
    for x in range(20):
      filler = ctk.CTkButton(
        master=device_panel,
        height=50, font = ('System', 14), text=f"Device {x}")
      filler.pack(pady=5, padx=20, fill=ctk.BOTH)

    # Device Info Panel
    device_info_frame = ctk.CTkScrollableFrame(self, label_text="Showing Device Info")
    devices = {}
    
    # Device Info Panel -> Device Details
    for x in range(4):
      device_info_frame.rowconfigure(x, weight=1)
    device_info_frame.columnconfigure(0, weight=1)

    device_info_frame.grid(row=1, rowspan=9, column=1,columnspan=9, sticky='news',padx=20,pady=20)
    
    info1 = DeviceInfoCard(device_info_frame,"Device Id", "1006101")
    info1.grid(row=0,column=0,padx=5,pady=5,sticky='news')
    
    info2 = DeviceInfoCard(device_info_frame,"Device Name", "Example Card")
    info2.grid(row=1,column=0,padx=5,pady=5,sticky='news')
    
    info3 = DeviceInfoCard(device_info_frame,"Device Description", "A card class implimented in the devices panel.")
    info3.grid(row=2,column=0,padx=5,pady=5,sticky='news')
    
    info4 = DeviceInfoCard(device_info_frame,"Device Type", "For display")
    info4.grid(row=3,column=0,padx=5,pady=5,sticky='news')


class DeviceInfoCard(ctk.CTkFrame):
  def __init__(self, parent, lbl, data):
    super().__init__(parent)
    self._lbl = lbl
    self._data = data
    
    self._create_widgets()

  def _create_widget_layout(self):
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0,weight=1)
    self.columnconfigure(1,weight=1)

  def _create_widgets(self):    
    self._create_widget_layout()

    self.id_lbl = ctk.CTkLabel(self,text=f"{self._lbl}:")
    self.id_lbl.grid(row=0, column=0, padx=5,pady=5,sticky='ne')

    self.id_value = ctk.CTkLabel(self, text=f"{self._data}")
    self.id_value.grid(row=0, column=1,padx=5,pady=5,sticky='nw')
