import numpy as np # [cite: 1]
from tkinter import * # [cite: 2]
import matplotlib.pyplot as plt # [cite: 3]
import matplotlib.animation as animation # [cite: 4]
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # [cite: 6]

class FourBarApp:
    # Notice we added l1, l2, l3, l4 to the initialization so it receives the numbers
    def __init__(self, master, l1, l2, l3, l4): # [cite: 14]
        self.L1 = l1
        self.L2 = l2
        self.L3 = l3
        self.L4 = l4
        
        # Plot Setup
        self.fig = plt.figure(1) # [cite: 16]
        plt.clf()
        self.link, = plt.plot([], [], 'r-', linewidth=4) # [cite: 17]
        self.link1, = plt.plot([], [], 'b-', linewidth=4)
        self.joints, = plt.plot([], [], marker='o', ls="", markersize=10) # [cite: 18]
        
        self.plot1 = FigureCanvasTkAgg(self.fig, master=master).get_tk_widget() # [cite: 20]
        
        # Buttons
        self.buton1 = Button(master, text="Start", command=self.start) # [cite: 31]
        self.buton2 = Button(master, text="Stop", command=self.stop) # [cite: 32]
        
        # Labels to show the lengths that were passed in
        self.output1 = Label(master, text=f"L1: {self.L1}") # [cite: 34]
        self.output2 = Label(master, text=f"L2: {self.L2}") # [cite: 35]
        self.output3 = Label(master, text=f"L3: {self.L3}") # [cite: 36]
        self.output4 = Label(master, text=f"L4: {self.L4}") # [cite: 37]
        self.warning = Label(master, text="") # [cite: 38]
        self.warning = Label(master, text="Grashof Mechanism", fg="blue", font=("Arial", 12, "bold"))
        
        # UI Placement
        self.plot1.place(x=0, y=0, height=500, width=800) # [cite: 41]
        self.output1.place(x=100, y=500, height=20, width=100) # [cite: 42]
        self.output2.place(x=250, y=500, height=20, width=100) # [cite: 44]
        self.output3.place(x=400, y=500, height=20, width=100) # [cite: 46]
        self.output4.place(x=550, y=500, height=20, width=100) # [cite: 48]
        
        self.warning.place(x=100, y=550, height=20, width=600) # [cite: 50]
        self.buton1.place(x=100, y=600, height=30, width=200) # [cite: 52]
        self.buton2.place(x=500, y=600, height=30, width=200) # [cite: 53]
        
        # Animation Setup
        frames = self.generate_frames()
        self.anim = animation.FuncAnimation(self.fig, self.animate, frames, interval=10, blit=False) # [cite: 55]
        self.k = 0 # [cite: 57]
    
    def generate_frames(self):
        L1, L2, L3, L4 = self.L1, self.L2, self.L3, self.L4
        links = sorted([L1, L2, L3, L4])
        S, L, P, Q = links[0], links[3], links[1], links[2]
        
        # If Grashof AND L2 or L1 is the shortest, L2 can spin a full 360 degrees
        if (S + L <= P + Q) and (S == L1 or S == L2):
            return np.arange(0, 2*np.pi, 0.01)
            
        # Otherwise (Double Rocker or Non-Grashof), calculate the swing limits!
        else:
            # Calculate cos(theta) at the folded and extended limits
            cos_t1 = (L1**2 + L2**2 - (L3 - L4)**2) / (2 * L1 * L2)
            cos_t2 = (L1**2 + L2**2 - (L3 + L4)**2) / (2 * L1 * L2)
            
            # Clip values between -1 and 1 to prevent NumPy float errors
            cos_t1 = max(-1.0, min(1.0, cos_t1))
            cos_t2 = max(-1.0, min(1.0, cos_t2))
            
            # Convert to radians
            t_min = np.arccos(cos_t1)
            t_max = np.arccos(cos_t2)
            
            if t_min > t_max:
                t_min, t_max = t_max, t_min
                
            # Create an array that swings UP to the max, and then DOWN to the min
            swing_up = np.arange(t_min, t_max, 0.02)
            swing_down = np.arange(t_max, t_min, -0.02)
            return np.concatenate((swing_up, swing_down))

    def calculate(self, theta2): # [cite: 60]
        L1, L2, L3, L4 = self.L1, self.L2, self.L3, self.L4 # [cite: 61, 62, 63, 64]
        BD = np.sqrt(L1**2 + L2**2 - 2*L1*L2*np.cos(theta2)) # [cite: 65]

        cos_alfa = (L3**2 + L4**2 - BD**2) / (2*L3*L4)
        cos_alfa = np.clip(cos_alfa, -1.0, 1.0) # Forces imperfect math strictly into the [-1, 1] range
        alfa = np.arccos(cos_alfa)

        #alfa = np.arccos((L3**2 + L4**2 - BD**2) / (2*L3*L4)) # [cite: 66]
        theta3 = 2*np.arctan((-L2*np.sin(theta2) + L4*np.sin(alfa)) / (L1 + L3 - L2*np.cos(theta2) - L4*np.cos(alfa))) # [cite: 67]
        theta4 = 2*np.arctan((L2*np.sin(theta2) - L3*np.sin(alfa)) / (L4 - L1 + L2*np.cos(theta2) - L3*np.cos(alfa))) # [cite: 68]
        
        A = [0, 0] # [cite: 70]
        B = [L2*np.cos(theta2), L2*np.sin(theta2)] # [cite: 71]
        C = [L2*np.cos(theta2) + L3*np.cos(theta3), L2*np.sin(theta2) + L3*np.sin(theta3)] # [cite: 72]
        D = [L1, 0] # [cite: 73]
        return BD, alfa, theta3, theta4, A, B, C, D # [cite: 74]

    def axis_setter(self):
        # 1. Simulate the entire movement to get all coordinates
        t2 = self.generate_frames()
        BD, alfa, theta3, theta4, A, B, C, D = self.calculate(t2)
        
        # 2. Gather every single X and Y coordinate the joints will ever touch
        # A is always [0,0] and D is always [L1, 0]
        all_x = np.concatenate(([0, self.L1], B[0], C[0]))
        all_y = np.concatenate(([0, 0], B[1], C[1]))
        
        # 3. Find the absolute extremes (nanmax/nanmin ignore math errors from extreme angles)
        max_x = np.nanmax(all_x)
        min_x = np.nanmin(all_x)
        max_y = np.nanmax(all_y)
        min_y = np.nanmin(all_y)
        
        # 4. Create a dynamic padding/margin so the mechanism never touches the edge
        # We base the padding on the size of the largest link
        padding = max(self.L1, self.L2, self.L3, self.L4) * 0.2
        
        upper_x = max_x + padding
        lower_x = min_x - padding
        upper_y = max_y + padding
        lower_y = min_y - padding
        
        return upper_x, lower_x, upper_y, lower_y

    def start(self): # [cite: 99]
        try:
            upper_x, lower_x, upper_y, lower_y = self.axis_setter() # [cite: 105]
            plt.axis([lower_x, upper_x, lower_y, upper_y]) # [cite: 106]
            plt.gca().set_aspect('equal', adjustable='box') # [cite: 107]
            self.k = 1 # [cite: 108]
            self.anim.event_source.start() # [cite: 109]
            self.warning.config(text="Grashof Mechanism", background="white") # [cite: 110]
        except: # [cite: 111]
            self.warning.config(text="Math error during rotation.", background="red", font=("Courier", 14)) # [cite: 112]
            self.stop() # [cite: 113]
        return self.k # [cite: 114]

    def stop(self): # [cite: 117]
        self.k = 0 # [cite: 118]
        return self.k # [cite: 119]

    def animate(self, theta2): # [cite: 122]
        if self.k == 0: # [cite: 123]
            self.anim.event_source.stop() # [cite: 124]
        else: # [cite: 125]
            BD, alfa, theta3, theta4, A, B, C, D = self.calculate(theta2) # [cite: 126]
            x = [A[0], B[0], C[0], D[0]] # [cite: 127]
            y = [A[1], B[1], C[1], D[1]] # [cite: 128]
            x1=[D[0],A[0]]
            y1=[D[1],A[1]]
            self.link.set_data(x, y) # [cite: 132]
            self.joints.set_data(x, y) # [cite: 133]
            self.link1.set_data(x1,y1)
        return self.link, self.joints # [cite: 134]

# This is the function we will call from your main file!
def launch_animation(l1, l2, l3, l4):
    window = Toplevel() # Toplevel makes it a popup child window rather than a primary root window
    window.geometry("800x800") # [cite: 10]
    window.title("Four Bar Animation") # [cite: 11]
    app = FourBarApp(window, l1, l2, l3, l4) # Passes the variables into the App [cite: 136]