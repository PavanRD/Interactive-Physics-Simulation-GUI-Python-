import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CrankSliderApp:
    def __init__(self, master, r, l):
        self.r = r  # Crank radius
        self.l = l  # Connecting rod length
        
        # Plot Setup
        self.fig = plt.figure(1)
        plt.clf()  # Wipe canvas clean
        
        # We will draw the sliding axis as a massive line like your professor asked
        self.axis_line, = plt.plot([-1000, 1000], [0, 0], 'k--', linewidth=1) 
        
        self.link, = plt.plot([], [], 'b-', linewidth=4) # Blue lines for the links
        self.joints, = plt.plot([], [], marker='o', color='black', ls="", markersize=8) # Black dots for joints
        self.slider, = plt.plot([], [], marker='s', color='red', ls="", markersize=20) # Red square for the slider block
        
        self.plot1 = FigureCanvasTkAgg(self.fig, master=master).get_tk_widget()
        
        # Buttons & Labels
        self.buton1 = Button(master, text="Start", command=self.start)
        self.buton2 = Button(master, text="Stop", command=self.stop)
        
        self.output1 = Label(master, text=f"Crank Radius (r): {self.r}")
        self.output2 = Label(master, text=f"Connecting Rod (l): {self.l}")
        self.warning = Label(master, text="In-Line Crank-Slider Mechanism", fg="green", font=("Arial", 12, "bold"))
        
        # Layout Placements
        self.plot1.place(x=0, y=0, height=500, width=800)
        self.output1.place(x=200, y=500, height=20, width=150)
        self.output2.place(x=450, y=500, height=20, width=150)
        
        self.warning.place(x=100, y=550, height=20, width=600)
        self.buton1.place(x=100, y=600, height=30, width=200)
        self.buton2.place(x=500, y=600, height=30, width=200)
        
        # Animation Setup
        self.anim = animation.FuncAnimation(self.fig, self.animate, np.arange(0, 2*np.pi, 0.05), interval=20, blit=False)
        self.k = 0

    def calculate(self, theta):
        # A is the crank center, B is the crank pin, C is the slider pin
        A = [0, 0]
        B = [self.r * np.cos(theta), self.r * np.sin(theta)]
        
        # Slider X coordinate formula
        x_slider = self.r * np.cos(theta) + np.sqrt(self.l**2 - (self.r**2) * (np.sin(theta)**2))
        C = [x_slider, 0]
        
        return A, B, C

    def axis_setter(self):
        # The furthest right the slider goes is r + l
        max_x = self.r + self.l
        # The furthest left the slider goes is l - r
        min_x = self.l - self.r
        # The highest/lowest the crank goes is r and -r
        max_y = self.r
        min_y = -self.r
        
        padding = max(self.r, self.l) * 0.3
        
        upper_x = max_x + padding
        lower_x = min(min_x, -self.r) - padding # Make sure the crank circle isn't cut off
        upper_y = max_y + padding
        lower_y = min_y - padding
        
        return upper_x, lower_x, upper_y, lower_y

    def start(self):
        try:
            if self.l < self.r:
                self.warning.config(text="Error: Connecting rod must be longer than crank!", fg="red")
                return self.k
                
            upper_x, lower_x, upper_y, lower_y = self.axis_setter()
            plt.axis([lower_x, upper_x, lower_y, upper_y])
            plt.gca().set_aspect('equal', adjustable='box')
            self.k = 1
            self.anim.event_source.start()
            self.warning.config(fg="green")
        except Exception as e:
            self.warning.config(text=f"Error: {e}", fg="red")
            self.stop()
        return self.k

    def stop(self):
        self.k = 0
        return self.k

    def animate(self, theta):
        if self.k == 0:
            self.anim.event_source.stop()
        else:
            A, B, C = self.calculate(theta)
            
            # Update the links and joints
            x = [A[0], B[0], C[0]]
            y = [A[1], B[1], C[1]]
            
            self.link.set_data(x, y)
            self.joints.set_data(x, y)
            
            # Update the slider block independently
            self.slider.set_data([C[0]], [C[1]])
            
        return self.link, self.joints, self.slider, self.axis_line

# The launcher function to call from your main file
def launch_crank_slider_animation(r, l):
    window = Toplevel()
    window.geometry("800x800")
    window.title("Crank Slider Animation")
    app = CrankSliderApp(window, r, l)