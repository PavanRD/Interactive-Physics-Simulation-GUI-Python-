import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class NonGrashofApp:
    def __init__(self, master, l1, l2, l3, l4):
        self.L1 = l1
        self.L2 = l2
        self.L3 = l3
        self.L4 = l4
        
        # Plot Setup
        self.fig = plt.figure(1)
        plt.clf() # Wipes the canvas clean to prevent ghosting
        self.link, = plt.plot([], [], 'r-', linewidth=4)
        self.joints, = plt.plot([], [], marker='o', ls="", markersize=10)
        
        self.plot1 = FigureCanvasTkAgg(self.fig, master=master).get_tk_widget()
        
        # Buttons & Labels
        self.buton1 = Button(master, text="Start", command=self.start)
        self.buton2 = Button(master, text="Stop", command=self.stop)
        
        self.output1 = Label(master, text=f"L1: {self.L1}")
        self.output2 = Label(master, text=f"L2: {self.L2}")
        self.output3 = Label(master, text=f"L3: {self.L3}")
        self.output4 = Label(master, text=f"L4: {self.L4}")
        self.warning = Label(master, text="Non-Grashof Mechanism (Triple Rocker)", fg="blue", font=("Arial", 12, "bold"))

        
        # Layout Placements
        self.plot1.place(x=0, y=0, height=500, width=800)
        self.output1.place(x=100, y=500, height=20, width=100)
        self.output2.place(x=250, y=500, height=20, width=100)
        self.output3.place(x=400, y=500, height=20, width=100)
        self.output4.place(x=550, y=500, height=20, width=100)
        
        self.warning.place(x=100, y=550, height=20, width=600)
        self.buton1.place(x=100, y=600, height=30, width=200)
        self.buton2.place(x=500, y=600, height=30, width=200)
        
        # Generate the frames to bounce back and forth
        frames = self.generate_frames()
        self.anim = animation.FuncAnimation(self.fig, self.animate, frames, interval=10, blit=False)
        self.k = 0

    def generate_frames(self):
        L1, L2, L3, L4 = self.L1, self.L2, self.L3, self.L4
        
        # Limit 1: L3 and L4 are folded over each other
        cos_t1 = (L1**2 + L2**2 - (L3 - L4)**2) / (2 * L1 * L2)
        # Limit 2: L3 and L4 are fully extended
        cos_t2 = (L1**2 + L2**2 - (L3 + L4)**2) / (2 * L1 * L2)
        
        # Clip values to stay within -1 and 1 (prevents float math errors)
        cos_t1 = max(-1.0, min(1.0, cos_t1))
        cos_t2 = max(-1.0, min(1.0, cos_t2))
        
        # Convert cosines to radians
        t_min = np.arccos(cos_t1)
        t_max = np.arccos(cos_t2)
        
        if t_min > t_max:
            t_min, t_max = t_max, t_min
            
        # Create the back-and-forth bounce arrays
        swing_up = np.arange(t_min, t_max, 0.02)
        swing_down = np.arange(t_max, t_min, -0.02)
        
        # Combine them into one continuous animation loop
        return np.concatenate((swing_up, swing_down))

    def calculate(self, theta2):
        L1, L2, L3, L4 = self.L1, self.L2, self.L3, self.L4
        
        BD = np.sqrt(L1**2 + L2**2 - 2*L1*L2*np.cos(theta2))
        
        # Safety check: Force the internal math strictly between -1.0 and 1.0
        # This completely eliminates the arccos warning at the extreme dead centers!
        cos_alfa = (L3**2 + L4**2 - BD**2) / (2*L3*L4)
        cos_alfa = np.clip(cos_alfa, -1.0, 1.0) 
        alfa = np.arccos(cos_alfa)
        
        theta3 = 2*np.arctan((-L2*np.sin(theta2) + L4*np.sin(alfa)) / (L1 + L3 - L2*np.cos(theta2) - L4*np.cos(alfa)))
        theta4 = 2*np.arctan((L2*np.sin(theta2) - L3*np.sin(alfa)) / (L4 - L1 + L2*np.cos(theta2) - L3*np.cos(alfa)))
        
        A = [0, 0]
        B = [L2*np.cos(theta2), L2*np.sin(theta2)]
        C = [L2*np.cos(theta2) + L3*np.cos(theta3), L2*np.sin(theta2) + L3*np.sin(theta3)]
        D = [L1, 0]
        
        return BD, alfa, theta3, theta4, A, B, C, D

    def axis_setter(self):
        # Universal Camera: looks at all possible coordinates and draws a box
        t2 = self.generate_frames()
        BD, alfa, theta3, theta4, A, B, C, D = self.calculate(t2)
        
        B = np.array(B)
        C = np.array(C)
        
        all_x = np.concatenate(([0, self.L1], B[0], C[0]))
        all_y = np.concatenate(([0, 0], B[1], C[1]))
        
        padding = max(self.L1, self.L2, self.L3, self.L4) * 0.2
        
        upper_x = np.nanmax(all_x) + padding
        lower_x = np.nanmin(all_x) - padding
        upper_y = np.nanmax(all_y) + padding
        lower_y = np.nanmin(all_y) - padding
        
        return upper_x, lower_x, upper_y, lower_y

    def start(self):
        try:
            upper_x, lower_x, upper_y, lower_y = self.axis_setter()
            plt.axis([lower_x, upper_x, lower_y, upper_y])
            plt.gca().set_aspect('equal', adjustable='box')
            self.k = 1
            self.anim.event_source.start()
            self.warning.config(fg="blue")
        except Exception as e:
            self.warning.config(text=f"Error: {e}", fg="red")
            self.stop()
        return self.k

    def stop(self):
        self.k = 0
        return self.k

    def animate(self, theta2):
        if self.k == 0:
            self.anim.event_source.stop()
        else:
            BD, alfa, theta3, theta4, A, B, C, D = self.calculate(theta2)
            x = [A[0], B[0], C[0], D[0]]
            y = [A[1], B[1], C[1], D[1]]
            self.link.set_data(x, y)
            self.joints.set_data(x, y)
        return self.link, self.joints

# The launcher function to call from your main file
def launch_non_grashof_animation(l1, l2, l3, l4):
    window = Toplevel()
    window.geometry("800x800")
    window.title("Non-Grashof Animation")
    app = NonGrashofApp(window, l1, l2, l3, l4)