def center_window(parent, child, width, height):
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
    child.geometry(f"{width}x{height}+{x}+{y}")