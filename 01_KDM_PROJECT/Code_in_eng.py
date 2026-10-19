import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Library used to embed Matplotlib into Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#--------------------------------------------------------------
# Window settings
window = Tk()
window.geometry("800x800")
window.title("Four Bar Animation")
#--------------------------------------------------------------
class App:
    def __init__(self, master):
        # Plot Settings
        self.fig = plt.figure(1) # Figure 1 is named fig.
        self.link,   = plt.plot([], [], 'r-', linewidth=4) # Graph parameters created for the link
        self.joints, = plt.plot([], [],marker='o', ls="" ,markersize=10) # Graph parameters created for the joint
        # 1) Creating the plot (plot1 name is variable) - 1st plot registered to fig is taken:
        self.plot1 = FigureCanvasTkAgg(self.fig, master=window).get_tk_widget()
        # 2) Creating the entry box:
        self.input_var1 = IntVar()
        self.input_var2 = IntVar()
        self.input_var3 = IntVar()
        self.input_var4 = IntVar()
        self.input1 = Entry(window,textvariable=self.input_var1)
        self.input2 = Entry(window,textvariable=self.input_var2)
        self.input3 = Entry(window,textvariable=self.input_var3)
        self.input4 = Entry(window,textvariable=self.input_var4)
        # 3) Creating the button:
        self.button1 = Button(window,text="Start",command = self.start)
        self.button2 = Button(window,text="Stop",command = self.stop)
        # 4) Creating the label:
        self.output1 = Label(window,text="L1:")
        self.output2 = Label(window,text="L2:")
        self.output3 = Label(window,text="L3:")
        self.output4 = Label(window,text="L4:")
        self.warning = Label(window,text="")
        self.label = Label(window,text="Designed by Berke Ogulcan Parlak")
        # Positions
        self.plot1.place(x=0,y=0,height=500,width=800)
        self.output1.place(x=0,y=500,height=20,width=100)
        self.input1.place(x=100,y=500,height=20,width=100)
        self.output2.place(x=200,y=500,height=20,width=100)
        self.input2.place(x=300,y=500,height=20,width=100)
        self.output3.place(x=400,y=500,height=20,width=100)
        self.input3.place(x=500,y=500,height=20,width=100)
        self.output4.place(x=600,y=500,height=20,width=100)
        self.input4.place(x=700,y=500,height=20,width=100)
        self.warning.place(x=100,y=550,height=20,width=600)
        self.label.place(x=550,y=660,height=20,width=300)
        self.button1.place(x=100,y=600,height=30,width=200)
        self.button2.place(x=500,y=600,height=30,width=200)
        # 5) Creating the animation
        self.anim = animation.FuncAnimation(self.fig, self.animate, np.arange(0, 2*np.pi, 0.01) , interval=10,blit=False)
        # Start/stop animation variable
        self.k = 0 # If k = 0 stop the animation, if 1 start it.
        #--------------------------------------------------------------
        # Function defined to calculate variable values depending on Theta2:
    def calculate(self,theta2):
        L1 = self.L1
        L2 = self.L2
        L3 = self.L3
        L4 = self.L4
        BD = np.sqrt(L1**2+L2**2-2*L1*L2*np.cos(theta2))
        alpha = np.arccos((L3**2+L4**2-BD**2)/(2*L3*L4))
        theta3 = 2*np.arctan((-L2*np.sin(theta2)+L4*np.sin(alpha))/(L1+L3-L2*np.cos(theta2)-L4*np.cos(alpha)))
        theta4 = 2*np.arctan((L2*np.sin(theta2)-L3*np.sin(alpha))/(L4-L1+L2*np.cos(theta2)-L3*np.cos(alpha)))
        # x and y positions of A, B, C, D joints
        A = [0,0]
        B = [L2*np.cos(theta2),L2*np.sin(theta2)]
        C = [L2*np.cos(theta2)+L3*np.cos(theta3),L2*np.sin(theta2)+L3*np.sin(theta3)]
        D = [L1,0]
        return BD,alpha,theta3,theta4,A,B,C,D
        #--------------------------------------------------------------
        # Automatic axis setter
    def axis_setter(self):
        L1 = self.L1 # L1 is taken from within self.
        t2 = np.arange(0, 2*np.pi, 0.01)
        BD,alpha,theta3,theta4,A,B,C,D = self.calculate(t2)
        B = np.array(B)
        C = np.array(C)
        K = C.max(axis=1)
        M = C.min(axis=1)
        Cx_max = K[0]
        Cy_max = K[1]
        Cx_min = M[0]
        Cy_min = M[1]
        F = [np.amin(B),M[0]]
        G = [np.amin(B),M[1]]
        upper_x = L1 + abs(Cx_max-L1) + 0.5
        lower_x = np.amin(F) -0.5
        upper_y = Cy_max  + 0.5
        lower_y = np.amin(G) -0.5
        del BD,alpha,theta3,theta4,A,B,C,D,t2
        return upper_x,lower_x,upper_y,lower_y
        #--------------------------------------------------------------
        # When the Start button is pressed:
    def start(self): # Since the k variable is registered within self, it is enough to take self as input instead of self.k!
        self.L1 = self.input_var1.get()
        self.L2 = self.input_var2.get()
        self.L3 = self.input_var3.get()
        self.L4 = self.input_var4.get()
        try:
            upper_x,lower_x,upper_y,lower_y = self.axis_setter()
            plt.axis([lower_x, upper_x,lower_y, upper_y]) # Set the axis
            plt.gca().set_aspect('equal', adjustable='box')
            self.k = 1
            self.anim.event_source.start() # Enters the animate loop
            self.warning.config(text = "",background="white")
        except:
            self.warning.config(text = "Link lengths are not suitable, please change." ,background="red",font=("Courier", 14))
            self.stop()
        return self.k
        #--------------------------------------------------------------
        # When the Stop button is pressed:
    def stop(self):
        self.k = 0 # Stop the animation
        return self.k
        #--------------------------------------------------------------
        # Animation part theta2 = 0:0.01:2pi
    def animate(self,theta2):
        if (self.k==0):
            self.anim.event_source.stop() # Exits the animate loop
        else:
            BD,alpha,theta3,theta4,A,B,C,D = self.calculate(theta2) # Instantaneous parameter values of the mechanism
            x = [A[0],B[0],C[0],D[0]] # X positions of the joints
            y = [A[1],B[1],C[1],D[1]] # Y positions of the joints
            #      Why aren't we using delete here?
            #      -Because x and y are not vectors but scalars (Instantaneous position of the mechanism)
            #      -By saying line.set_data(x,y), we ensure that the mechanism only takes the instantaneous position.
            self.link.set_data(x, y) # Instantaneous position of the links plotted
            self.joints.set_data(x, y) # Instantaneous position of the joints plotted
        return self.link, self.joints
        #-------------------------------------------------------------
# When the Stop button is pressed:
    def stop(self): 
        self.k = 0 # Stop the animation
        return self.k
#--------------------------------------------------------------
# Animation part theta2 = 0:0.01:2pi
    def animate(self,theta2):
        if (self.k==0):
            self.anim.event_source.stop() # Exits the animate loop
        else:
            BD,alpha,theta3,theta4,A,B,C,D = self.calculate(theta2) # Instantaneous parameter values of the mechanism
            x = [A[0],B[0],C[0],D[0]] # X positions of the joints
            y = [A[1],B[1],C[1],D[1]] # Y positions of the joints
                #      Why aren't we using delete here?
                #      -Because x and y are not vectors but scalars (Instantaneous position of the mechanism)
                #      -By saying line.set_data(x,y), we ensure that the mechanism only takes the instantaneous position.
            self.link.set_data(x, y) # Instantaneous position of the links plotted
            self.joints.set_data(x, y) # Instantaneous position of the joints plotted
        return self.link, self.joints
#--------------------------------------------------------------

App(window) # App is active
mainloop()  # Window continuously open in loop