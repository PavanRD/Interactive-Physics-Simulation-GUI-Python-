import numpy as np
from tkinter import *
from tkinter import messagebox # Added to show a popup if the user types letters instead of numbers

# --------------------------------------------------------------
# 1. The Grashof Logic Engine
def check_grashof(e1, e2, e3, e4):
    try:
        # Get the text from the entry boxes and turn them into decimal numbers (floats)
        l1 = float(e1.get())
        l2 = float(e2.get())
        l3 = float(e3.get())
        l4 = float(e4.get())
        
        # Put them in a list and sort them from smallest to largest
        links = sorted([l1, l2, l3, l4])
        
        S = links[0] # Shortest
        P = links[1] # Intermediate 1
        Q = links[2] # Intermediate 2
        L = links[3] # Longest
        
        # The Grashof Test
        if S + L <= P + Q:
            open_grashof_satisfied_window()
        else:
            open_grashof_unsatisfied_window()
            
    except ValueError:
        # If the user leaves a box blank or types "abc", this prevents the app from crashing
        messagebox.showerror("Input Error", "Please enter valid numbers for all link lengths.")

# --------------------------------------------------------------
# 2. The Result Windows
def open_grashof_satisfied_window():
    sat_win = Toplevel(root)
    sat_win.title("Grashof Satisfied")
    sat_win.geometry("400x200")
    Label(sat_win, text="✅ Grashof Condition Satisfied!\n\nAt least one link can rotate a full 360°.", 
          fg="green", font=("Arial", 12)).pack(pady=50)

def open_grashof_unsatisfied_window():
    unsat_win = Toplevel(root)
    unsat_win.title("Grashof Not Satisfied")
    unsat_win.geometry("400x200")
    Label(unsat_win, text="❌ Grashof Condition NOT Satisfied.\n\nThis is a non-Grashof mechanism (triple rocker).", 
          fg="red", font=("Arial", 12)).pack(pady=50)

# --------------------------------------------------------------
# 3. The Input Window
def open_four_bar_window():
    four_bar_win = Toplevel(root) 
    four_bar_win.title("Four Bar Mechanism - Inputs")
    four_bar_win.geometry("300x350")
    
    Label(four_bar_win, text="Enter Link Lengths:", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Creating the 4 input fields
    Label(four_bar_win, text="L1 (Ground):").pack()
    entry1 = Entry(four_bar_win)
    entry1.pack(pady=5)
    
    Label(four_bar_win, text="L2:").pack()
    entry2 = Entry(four_bar_win)
    entry2.pack(pady=5)
    
    Label(four_bar_win, text="L3:").pack()
    entry3 = Entry(four_bar_win)
    entry3.pack(pady=5)
    
    Label(four_bar_win, text="L4:").pack()
    entry4 = Entry(four_bar_win)
    entry4.pack(pady=5)
    
    # The command uses 'lambda' so we can pass our 4 entry boxes into the check_grashof function
    check_btn = Button(four_bar_win, text="Check Mechanism", 
                       command=lambda: check_grashof(entry1, entry2, entry3, entry4),
                       width=20, bg="lightgray")
    check_btn.pack(pady=20)

# --------------------------------------------------------------
# 4. The Plots Window (Placeholder for now)
def open_plots_window():
    plots_win = Toplevel(root)
    plots_win.title("Plots")
    plots_win.geometry("400x300")
    Label(plots_win, text="Matplotlib Graphs will go here!").pack(pady=50)

# --------------------------------------------------------------
# 5. Main Window Setup
root = Tk()
root.title("Main Menu")
root.geometry("400x300")

Label(root, text="Select an Option:", font=("Arial", 14)).pack(pady=30)

btn_four_bar = Button(root, text="Four Bar Mechanism", command=open_four_bar_window, width=25, height=2)
btn_four_bar.pack(pady=10)

btn_plots = Button(root, text="Plots", command=open_plots_window, width=25, height=2)
btn_plots.pack(pady=10)

root.mainloop()