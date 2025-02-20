import customtkinter as ctk

# french violet 731DD8
# verdigris 48A9A6
# Timberwolf E4DFDA
# Ecru D4B483
# Indian red C1666B

class StyleWidget():
  def apply_styles(widget: ctk.CTkBaseClass):
    match type(widget):
      case ctk.CTkButton:
        widget.configure(
          corner_radius=50,
          border_width = 3
          )
        
      case ctk.CTkLabel:
        widget.configure()
        
      case ctk.CTkEntry:
        widget.configure()
        
      case _:
        ...
