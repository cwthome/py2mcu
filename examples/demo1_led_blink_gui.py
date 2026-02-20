import tkinter as tk
from tkinter import messagebox
import sys

running = True

def loop():
    if not running:
        sys.exit()

def set_led(status):
    if status:
        fg="white"
        bg="red"
        status = "Led ON"
    else:
        fg="black"
        bg="white"
        status = "Led OFF"
    led.config(fg=fg, bg=bg, text=status)
    root.update()

root = tk.Tk()
root.title("demo1_led_blink.py")
root.geometry("350x150")

led = tk.Label(root, text="???", font=("Arial", 50))
led.pack()

def on_closing():
    """Function to be called when the user tries to close the window."""
    if messagebox.askokcancel("Quit", "Do you want to quit?"): #
        global running
        running = False
        root.destroy()
        root.quit()
        sys.exit()

# Bind the custom function to the window close event
root.protocol("WM_DELETE_WINDOW", on_closing) #

if __name__ == "__main__":
    root.mainloop()  # 只在这个线程里调用
