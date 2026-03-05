import tkinter as tk
from tkinter import messagebox
import sys

running = True

# Global variables for GUI state
current_samples: list = [0] * 10
current_avg: int = 0
led_state: bool = False

def loop():
    if not running:
        sys.exit()

def set_led(status):
    global led_state
    led_state = status
    if status:
        fg = "white"
        bg = "red"
        status_text = "LED ON"
    else:
        fg = "black"
        bg = "white"
        status_text = "LED OFF"
    led.config(fg=fg, bg=bg, text=status_text)
    root.update()

def update_samples_display(samples):
    """Update the samples bar chart display"""
    global current_samples
    current_samples = samples
    
    # Clear existing bars
    for widget in bars_frame.winfo_children():
        widget.destroy()
    
    # Calculate average for threshold line
    avg = sum(samples) // len(samples) if samples else 0
    
    # Draw each sample as a vertical bar
    max_height = 40  # Max height for a bar in pixels
    for i, value in enumerate(samples):
        # Scale value (0-1023) to bar height (0-max_height)
        bar_height = int((value / 1023) * max_height) if value <= 1023 else max_height
        
        # Color based on threshold
        if value >= THRESHOLD:
            color = "orange"
        else:
            color = "lightblue"
        
        # Create bar
        bar = tk.Label(
            bars_frame,
            text="█" * max(1, bar_height // 2),
            font=("Courier", 8),
            fg=color,
            bg="white",
            width=4,
            anchor="sw"
        )
        bar.grid(row=0, column=i, padx=1)
        
        # Add value label below bar
        label = tk.Label(
            bars_frame,
            text=str(value),
            font=("Arial", 6),
            fg="gray",
            bg="white",
            width=4
        )
        label.grid(row=1, column=i, padx=1)

def update_avg_display(avg, threshold):
    """Update average and threshold display"""
    global current_avg
    current_avg = avg
    
    # Color based on threshold
    color = "red" if avg >= threshold else "green"
    avg_label.config(text=f"Average: {avg}", fg=color)
    
    # Threshold indicator
    if avg >= threshold:
        threshold_label.config(text=f"Threshold: {threshold} (EXCEEDED)", fg="red")
    else:
        threshold_label.config(text=f"Threshold: {threshold}", fg="gray")

# Constants from demo2
SAMPLE_SIZE = 10
THRESHOLD = 512

root = tk.Tk()
root.title("demo2_adc_average.py")
root.geometry("500x300")

# Title
title = tk.Label(root, text="ADC Average Demo", font=("Arial", 16, "bold"))
title.pack(pady=10)

# LED display
led = tk.Label(root, text="LED OFF", font=("Arial", 20), fg="black", bg="white")
led.pack(pady=5)

# Average and threshold display
info_frame = tk.Frame(root)
info_frame.pack(pady=5)

avg_label = tk.Label(info_frame, text="Average: 0", font=("Arial", 14), fg="green")
avg_label.pack(side=tk.LEFT, padx=20)

threshold_label = tk.Label(info_frame, text=f"Threshold: {THRESHOLD}", font=("Arial", 12), fg="gray")
threshold_label.pack(side=tk.LEFT, padx=20)

# Samples bar chart
bars_label = tk.Label(root, text="ADC Samples:", font=("Arial", 10, "bold"))
bars_label.pack(pady=5)

bars_frame = tk.Frame(root)
bars_frame.pack(pady=5)

# Initialize empty bars
for i in range(SAMPLE_SIZE):
    bar = tk.Label(
        bars_frame,
        text="",
        font=("Courier", 8),
        fg="lightgray",
        bg="white",
        width=4,
        anchor="sw"
    )
    bar.grid(row=0, column=i, padx=1)
    
    label = tk.Label(
        bars_frame,
        text="0",
        font=("Arial", 6),
        fg="gray",
        bg="white",
        width=4
    )
    label.grid(row=1, column=i, padx=1)

# Status bar
status_var = tk.StringVar(value="Ready")
status_bar = tk.Label(root, textvariable=status_var, font=("Arial", 9), bg="lightgray", anchor="w", padx=10)
status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=5)

def on_closing():
    """Function to be called when the user tries to close the window."""
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        global running
        running = False
        root.destroy()
        root.quit()
        sys.exit()

# Bind the custom function to the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    root.mainloop()  # 只在这个线程里调用