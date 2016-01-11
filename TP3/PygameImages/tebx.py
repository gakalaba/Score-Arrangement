import ctypes  # An included library with Python install.
ctypes.windll.user32.MessageBoxA(0, "Your text", "Your title", 1)