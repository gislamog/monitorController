import tkinter as tk
from tkinter import ttk
import screen_brightness_control as sbc
from screeninfo import get_monitors
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image, ImageDraw
import threading


class BrightnessControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Brightness Controller")
        self.geometry("400x200")
        self.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.monitors = get_monitors()
        self.sliders = []

        for i, monitor in enumerate(self.monitors):
            label = ttk.Label(self, text=f"Monitor {i + 1}")
            label.pack(pady=5)

            current_brightness = sbc.get_brightness(display=i)[0]
            slider = ttk.Scale(self, from_=0, to=100, orient='horizontal',
                               command=lambda val, i=i: self.set_brightness(i, val))
            slider.set(current_brightness)
            slider.pack(fill='x', padx=10, pady=5)
            self.sliders.append(slider)

        # Start the system tray icon in a separate thread
        self.icon_thread = threading.Thread(target=self.setup_tray_icon, daemon=True)
        self.icon_thread.start()

    def set_brightness(self, monitor_index, value):
        try:
            sbc.set_brightness(int(float(value)), display=monitor_index)
        except Exception as e:
            print(f"Failed to set brightness for Monitor {monitor_index + 1}: {e}")

    def setup_tray_icon(self):
        # Import an image for the icon
        image = Image.open(r"C:\Users\Paradox\PycharmProjects\monitorController\icon.png")

        # Define the tray icon menu
        menu = Menu(
            Item('Open Brightness Controller', self.show_window),
            Item('Exit', self.exit_app)
        )

        # Create the icon
        icon = Icon("Brightness Controller", image, "Brightness Controller", menu)
        icon.run()

    def show_window(self, icon=None, item=None):
        self.deiconify()

    def hide_window(self):
        self.withdraw()

    def exit_app(self, icon=None, item=None):
        self.quit()
        icon.stop()


if __name__ == '__main__':
    app = BrightnessControllerApp()
    app.mainloop()
