import tkinter as tk
from system_monitor import SystemMonitorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()