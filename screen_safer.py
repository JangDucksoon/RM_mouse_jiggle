import os
import sys
import pyautogui
import time
import random
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class MouseMoverApp:
    def __init__(self, root):
        self.get_image_path()

        self.root = root
        self.root.title("Hala Madrid!!!!")
        self.root.geometry("500x450")
        self.root.iconbitmap(os.path.join(self.image_path, 'rm_ico.ico'))
        self.running = False
        self.thread = None
        self.input_interval = 250

        self.background_image = Image.open(self.image_path + '\\rm_logo.png')
        self.background_image = self.background_image.resize((500, 450), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(root, width=500, height=450)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        self.interval_label = tk.Label(root, text="Interval (seconds):", bg='white')
        self.canvas.create_window(10, 30, window=self.interval_label, anchor="w")

        self.interval_scale = tk.Scale(root, from_=1, to=600, orient=tk.HORIZONTAL, bg='white', highlightthickness=0)
        self.interval_scale.set(self.input_interval)
        self.canvas.create_window(10, 80, window=self.interval_scale, anchor="w")

        self.set_interval_button = tk.Button(root, text="Set Interval", command=self.set_interval, bg='white')
        self.canvas.create_window(10, 130, window=self.set_interval_button, anchor="w")

        self.start_button = tk.Button(root, text="Start", command=self.start, bg='white')
        self.canvas.create_window(490, 30, window=self.start_button, anchor="e")

        self.stop_button = tk.Button(root, text="Stop", command=self.stop, bg='white')
        self.canvas.create_window(490, 70, window=self.stop_button, anchor="e")

        self.status_label = tk.Label(root, text="Status: Stopped", bg='white')
        self.canvas.create_window(490, 110, window=self.status_label, anchor="e")

    def get_image_path(self):
        try:
            self.image_path = os.path.join(sys._MEIPASS, 'images')
        except AttributeError:
            self.image_path = os.path.abspath('./images')

    def set_interval(self):
        if not self.running:
            new_interval = self.interval_scale.get()
            self.input_interval = new_interval
            messagebox.showinfo("Info", f"Interval set to {new_interval} seconds.")
        else:
            messagebox.showinfo("Info", "Cannot change interval while running.")

    def start(self):
        if not self.running:
            self.running = True
            self.interval_scale.config(state='disabled')
            self.set_interval_button.config(state='disabled')
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
            self.status_label.config(text=f"Status: Running (Interval: {self.input_interval} seconds)")
        else:
            messagebox.showinfo("Info", "Mouse mover is already running.")

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            self.interval_scale.config(state='normal')
            self.set_interval_button.config(state='normal')
            self.status_label.config(text="Status: Stopped")
        else:
            messagebox.showinfo("Info", "Mouse mover is not running.")

    def run(self):
        while self.running:
            pyautogui.FAILSAFE = True
            screenW, screenH = pyautogui.size()
            ran_w = random.randint(1, screenW)
            ran_h = random.randint(1, screenH)

            pyautogui.moveTo(ran_w, ran_h, 0.3)
            pyautogui.typewrite(" ", 1)
            
            for _ in range(self.input_interval):
                if not self.running:
                    break
                time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMoverApp(root)
    root.mainloop()