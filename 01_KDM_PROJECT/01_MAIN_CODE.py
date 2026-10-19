import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import messagebox # Added to show a popup if the user types letters instead of numbers
# Library used to embed Matplotlib into Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from A_four_bar_animation import launch_animation
from B_non_grishof import launch_non_grashof_animation
from C_slider_crank import launch_crank_slider_animation

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
        
        if L >= S + P + Q:
            messagebox.showerror("Geometry Error", "These links cannot form a closed loop! The longest link must be shorter than the sum of the other three.")
            return
        
        # The Grashof Test
        if S + L <= P + Q:
            launch_animation(l1, l2, l3, l4)
        else:
            launch_non_grashof_animation(l1, l2, l3, l4)
            
    except ValueError:
        # If the user leaves a box blank or types "abc", this prevents the app from crashing
        messagebox.showerror("Input Error", "Please enter valid numbers for all link lengths.")


#animation
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
    
    Label(four_bar_win, text="L2 (Crank):").pack()
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


# Crank-Slider Logic Engine
def check_crank_slider(e_r, e_l):
    try:
        r = float(e_r.get())
        l = float(e_l.get())
        
        # Launch the animation directly
        launch_crank_slider_animation(r, l)
            
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for r and l.")

# Crank-Slider Input Window
def open_crank_slider_window():
    cs_win = Toplevel(root) 
    cs_win.title("Crank-Slider Mechanism - Inputs")
    cs_win.geometry("300x250")
    
    Label(cs_win, text="Enter Link Lengths:", font=("Arial", 12, "bold")).pack(pady=10)
    
    Label(cs_win, text="Crank Radius (r):").pack()
    entry_r = Entry(cs_win)
    entry_r.pack(pady=5)
    
    Label(cs_win, text="Connecting Rod (l):").pack()
    entry_l = Entry(cs_win)
    entry_l.pack(pady=5)
    
    check_btn = Button(cs_win, text="Launch Animation", 
                       command=lambda: check_crank_slider(entry_r, entry_l),
                       width=20, bg="lightgray")
    check_btn.pack(pady=20)



# plots 
def open_plots_window():
    plots_win = Toplevel(root)
    plots_win.title("Plots")
    plots_win.geometry("600x600")
    
    Label(plots_win, text="Matplotlib Graphs will go here!").pack(pady=20)


# Main Window Setup
root = Tk()
root.title("Main Menu")
root.geometry("400x350") # Made the window slightly taller to fit the 3rd button

Label(root, text="Select an Option:", font=("Arial", 14)).pack(pady=30)

btn_four_bar = Button(root, text="Four Bar Mechanism", command=open_four_bar_window, width=25, height=2)
btn_four_bar.pack(pady=10)

btn_crank_slider = Button(root, text="Crank-Slider Mechanism", command=open_crank_slider_window, width=25, height=2)
btn_crank_slider.pack(pady=10)

btn_plots = Button(root, text="Plots", command=open_plots_window, width=25, height=2)
btn_plots.pack(pady=10)

root.mainloop()