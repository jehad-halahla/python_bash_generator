import tkinter as tk
import subprocess
from tkinter import messagebox

def generate_manual():
    command = lb.get(lb.curselection())
    man_command = "man " + command
    result = subprocess.run(man_command, shell=True)
    if result.returncode == 0:
        messagebox.showinfo("Success", f"Manual generated for {command}")
    else:
        messagebox.showerror("Error", f"Failed to generate manual for {command}")

# Create the main window
root = tk.Tk()

# Create a listbox
lb = tk.Listbox(root)
lb.pack()

# Read the first 20 commands from the file
with open("commands.txt", "r") as file:
    for i, command in enumerate(file):
        if i == 20:
            break
        lb.insert(tk.END, command.strip())

# Create a button
button = tk.Button(root, text="Generate Manual", command=generate_manual)
button.pack()

# Run the main loop
root.mainloop()