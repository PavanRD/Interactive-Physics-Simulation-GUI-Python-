"""
Coupler Curve Analysis Module
For a given distance and angle with respect to the coupler orientation,
produces:
1. Coupler curve (path traced by the point)
2. Velocity vs angle plot
3. Acceleration vs angle plot
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import messagebox


class CouplerCurveAnalysis:
    def __init__(self, L1, L2, L3, L4, omega2, alpha2):
        """
        Initialize four-bar mechanism for coupler analysis
        """
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.L4 = L4
        self.omega2 = omega2
        self.alpha2 = alpha2
    
    def calculate_positions(self, theta2):
        """Calculate positions of all points"""
        Ax, Ay = 0, 0
        Dx, Dy = self.L1, 0
        Bx = self.L2 * np.cos(theta2)
        By = self.L2 * np.sin(theta2)
        
        K1 = self.L1 / self.L2
        K2 = self.L1 / self.L4
        K3 = (self.L2**2 - self.L3**2 + self.L4**2 + self.L1**2) / (2 * self.L2 * self.L4)
        
        A = np.cos(theta2) - K1 - K2 * np.cos(theta2) + K3
        B = -2 * np.sin(theta2)
        C = K1 - (K2 + 1) * np.cos(theta2) + K3
        
        discriminant = B**2 - 4*A*C
        if discriminant < 0:
            return None
        
        theta4 = 2 * np.arctan2(-B + np.sqrt(discriminant), 2*A)
        
        K4 = self.L1 / self.L3
        K5 = (self.L4**2 - self.L1**2 - self.L2**2 - self.L3**2) / (2 * self.L2 * self.L3)
        
        D = np.cos(theta2) - K1 + K4 * np.cos(theta2) + K5
        E = -2 * np.sin(theta2)
        F = K1 + (K4 - 1) * np.cos(theta2) + K5
        
        discriminant = E**2 - 4*D*F
        if discriminant < 0:
            return None
        
        theta3 = 2 * np.arctan2(-E + np.sqrt(discriminant), 2*D)
        
        Cx = Dx - self.L4 * np.cos(theta4)
        Cy = Dy + self.L4 * np.sin(theta4)
        
        return {
            'A': (Ax, Ay), 'B': (Bx, By), 'C': (Cx, Cy), 'D': (Dx, Dy),
            'theta3': theta3, 'theta4': theta4
        }
    
    def get_coupler_point(self, theta2, distance, angle_offset_deg):
        """
        Get position of a point on the coupler link
        distance: distance from point B along the coupler
        angle_offset_deg: angle offset from BC line (in degrees)
        """
        pos = self.calculate_positions(theta2)
        if pos is None:
            return None, None
        
        Bx, By = pos['B']
        theta3 = pos['theta3']
        
        # Convert angle offset to radians
        angle_offset = np.radians(angle_offset_deg)
        
        # Angle of the coupler point
        angle = theta3 + angle_offset
        
        # Position of coupler point
        Px = Bx + distance * np.cos(angle)
        Py = By + distance * np.sin(angle)
        
        return Px, Py
    
    def calculate_coupler_velocity(self, theta2, distance, angle_offset_deg):
        """Calculate velocity of coupler point"""
        pos = self.calculate_positions(theta2)
        if pos is None:
            return None
        
        theta3 = pos['theta3']
        theta4 = pos['theta4']
        
        # Calculate omega3
        denom3 = self.L3 * np.sin(theta3 - theta4)
        omega3 = (self.omega2 * self.L2 * np.sin(theta4 - theta2)) / denom3 if abs(denom3) > 1e-6 else 0
        
        # Velocity of point B
        VBx = -self.omega2 * self.L2 * np.sin(theta2)
        VBy = self.omega2 * self.L2 * np.cos(theta2)
        
        # Convert angle offset to radians
        angle_offset = np.radians(angle_offset_deg)
        angle = theta3 + angle_offset
        
        # Velocity of coupler point
        VPx = VBx - omega3 * distance * np.sin(angle)
        VPy = VBy + omega3 * distance * np.cos(angle)
        
        VP = np.sqrt(VPx**2 + VPy**2)
        
        return VP, omega3
    
    def calculate_coupler_acceleration(self, theta2, distance, angle_offset_deg):
        """Calculate acceleration of coupler point"""
        pos = self.calculate_positions(theta2)
        if pos is None:
            return None
        
        theta3 = pos['theta3']
        theta4 = pos['theta4']
        
        # Calculate angular velocities
        denom3 = self.L3 * np.sin(theta3 - theta4)
        denom4 = self.L4 * np.sin(theta4 - theta3)
        
        omega3 = (self.omega2 * self.L2 * np.sin(theta4 - theta2)) / denom3 if abs(denom3) > 1e-6 else 0
        omega4 = (self.omega2 * self.L2 * np.sin(theta2 - theta3)) / denom4 if abs(denom4) > 1e-6 else 0
        
        # Acceleration of B
        aBx = -self.omega2**2 * self.L2 * np.cos(theta2) - self.alpha2 * self.L2 * np.sin(theta2)
        aBy = -self.omega2**2 * self.L2 * np.sin(theta2) + self.alpha2 * self.L2 * np.cos(theta2)
        
        # Calculate alpha3
        num = (self.omega2**2 * self.L2 * np.cos(theta2) + 
               omega4**2 * self.L4 * np.cos(theta4) - 
               omega3**2 * self.L3 * np.cos(theta3))
        den = self.L3 * np.sin(theta3)
        denom_alpha = (den * np.cos(theta4) - self.L4 * np.sin(theta4) * np.cos(theta3))
        
        alpha3 = ((self.alpha2 * self.L2 * np.sin(theta2) - num * np.cos(theta4)) / 
                 denom_alpha) if abs(denom_alpha) > 1e-6 else 0
        
        # Convert angle offset to radians
        angle_offset = np.radians(angle_offset_deg)
        angle = theta3 + angle_offset
        
        # Acceleration of coupler point
        # Radial component
        aPr_x = -omega3**2 * distance * np.cos(angle)
        aPr_y = -omega3**2 * distance * np.sin(angle)
        
        # Tangential component
        aPt_x = -alpha3 * distance * np.sin(angle)
        aPt_y = alpha3 * distance * np.cos(angle)
        
        aPx = aBx + aPr_x + aPt_x
        aPy = aBy + aPr_y + aPt_y
        
        aP = np.sqrt(aPx**2 + aPy**2)
        
        return aP, alpha3
    
    def generate_coupler_data(self, distance, angle_offset_deg, num_points=360):
        """Generate complete coupler curve and kinematic data"""
        angles = np.linspace(0, 2*np.pi, num_points)
        
        Px_list = []
        Py_list = []
        velocities = []
        accelerations = []
        valid_angles = []
        
        for theta2 in angles:
            Px, Py = self.get_coupler_point(theta2, distance, angle_offset_deg)
            if Px is not None:
                Px_list.append(Px)
                Py_list.append(Py)
                
                vel = self.calculate_coupler_velocity(theta2, distance, angle_offset_deg)
                acc = self.calculate_coupler_acceleration(theta2, distance, angle_offset_deg)
                
                if vel is not None:
                    velocities.append(vel[0])
                    valid_angles.append(np.degrees(theta2))
                else:
                    velocities.append(0)
                    valid_angles.append(np.degrees(theta2))
                
                if acc is not None:
                    accelerations.append(acc[0])
                else:
                    accelerations.append(0)
        
        return {
            'Px': np.array(Px_list),
            'Py': np.array(Py_list),
            'velocities': np.array(velocities),
            'accelerations': np.array(accelerations),
            'angles': np.array(valid_angles)
        }


def open_coupler_analysis_window(root):
    """Open window for coupler curve analysis input"""
    analysis_win = Toplevel(root)
    analysis_win.title("Coupler Curve Analysis")
    analysis_win.geometry("450x600")
    
    Label(analysis_win, text="Coupler Curve Analysis", 
          font=("Arial", 12, "bold")).pack(pady=10)
    
    Label(analysis_win, text="Four-Bar Link Lengths (mm):").pack()
    
    Label(analysis_win, text="L1 (Ground):").pack()
    e_l1 = Entry(analysis_win)
    e_l1.pack(pady=3)
    
    Label(analysis_win, text="L2 (Crank):").pack()
    e_l2 = Entry(analysis_win)
    e_l2.pack(pady=3)
    
    Label(analysis_win, text="L3 (Coupler):").pack()
    e_l3 = Entry(analysis_win)
    e_l3.pack(pady=3)
    
    Label(analysis_win, text="L4 (Rocker):").pack()
    e_l4 = Entry(analysis_win)
    e_l4.pack(pady=3)
    
    Label(analysis_win, text="ω₂ (rad/s):").pack()
    e_omega = Entry(analysis_win)
    e_omega.pack(pady=3)
    
    Label(analysis_win, text="α₂ (rad/s²):").pack()
    e_alpha = Entry(analysis_win)
    e_alpha.pack(pady=3)
    
    Label(analysis_win, text="Coupler Point Parameters:", 
          font=("Arial", 11, "bold")).pack(pady=10)
    
    Label(analysis_win, text="Distance from B (mm):").pack()
    e_distance = Entry(analysis_win)
    e_distance.pack(pady=3)
    
    Label(analysis_win, text="Angle Offset from Coupler (degrees):").pack()
    e_angle_offset = Entry(analysis_win)
    e_angle_offset.pack(pady=3)
    
    # Buttons frame
    btn_frame = Frame(analysis_win)
    btn_frame.pack(pady=10)
    
    # Load Example button
    def load_example():
        e_l1.delete(0, END)
        e_l1.insert(0, "200")
        e_l2.delete(0, END)
        e_l2.insert(0, "80")
        e_l3.delete(0, END)
        e_l3.insert(0, "180")
        e_l4.delete(0, END)
        e_l4.insert(0, "150")
        e_omega.delete(0, END)
        e_omega.insert(0, "2.0")
        e_alpha.delete(0, END)
        e_alpha.insert(0, "0.0")
        e_distance.delete(0, END)
        e_distance.insert(0, "90")  # Midpoint of coupler
        e_angle_offset.delete(0, END)
        e_angle_offset.insert(0, "0")
    
    btn_example = Button(btn_frame, text="Load Example", command=load_example,
                        width=15, bg="lightyellow")
    btn_example.pack(side=LEFT, padx=5)
    
    btn_generate = Button(btn_frame, text="Generate Analysis", 
                         command=lambda: generate_coupler_plots(
                             float(e_l1.get()), float(e_l2.get()), 
                             float(e_l3.get()), float(e_l4.get()),
                             float(e_omega.get()), float(e_alpha.get()),
                             float(e_distance.get()), float(e_angle_offset.get())),
                         width=15, bg="orange")
    btn_generate.pack(side=LEFT, padx=5)


def generate_coupler_plots(L1, L2, L3, L4, omega2, alpha2, distance, angle_offset_deg):
    """Generate coupler curve with velocity and acceleration vs angle plots"""
    try:
        mechanism = CouplerCurveAnalysis(L1, L2, L3, L4, omega2, alpha2)
        
        print(f"Generating coupler curve...")
        print(f"Distance from B: {distance} mm")
        print(f"Angle offset: {angle_offset_deg}°")
        
        data = mechanism.generate_coupler_data(distance, angle_offset_deg)
        
        # Create plots window
        plot_win = Toplevel()
        plot_win.title("Coupler Curve Analysis Results")
        plot_win.geometry("1400x500")
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5))
        fig.suptitle(f'Coupler Curve Analysis (Distance={distance}mm, Offset={angle_offset_deg}°)', 
                     fontsize=12, fontweight='bold')
        
        # ========== COUPLER CURVE ==========
        ax1.plot(data['Px'], data['Py'], 'b-', linewidth=2.5, label='Coupler Path')
        ax1.plot(data['Px'][0], data['Py'][0], 'go', markersize=12, 
                label='Start', markeredgecolor='darkgreen', markeredgewidth=2)
        ax1.plot(data['Px'][-1], data['Py'][-1], 'ro', markersize=12, 
                label='End', markeredgecolor='darkred', markeredgewidth=2)
        
        # Draw mechanism at a few positions
        sample_angles = [0, 90, 180, 270]
        for angle_deg in sample_angles:
            theta2 = np.radians(angle_deg)
            pos = mechanism.calculate_positions(theta2)
            if pos is not None:
                A, B, C, D = pos['A'], pos['B'], pos['C'], pos['D']
                Px, Py = mechanism.get_coupler_point(theta2, distance, angle_offset_deg)
                
                alpha_val = 0.3
                ax1.plot([A[0], D[0]], [A[1], D[1]], 'gray', linewidth=4, alpha=alpha_val)
                ax1.plot([A[0], B[0]], [A[1], B[1]], 'b', linewidth=2, alpha=alpha_val)
                ax1.plot([B[0], C[0]], [B[1], C[1]], 'g', linewidth=2, alpha=alpha_val)
                ax1.plot([C[0], D[0]], [C[1], D[1]], 'orange', linewidth=2, alpha=alpha_val)
                
                if Px is not None:
                    ax1.plot(Px, Py, 'o', color='purple', markersize=6, alpha=0.5)
        
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.set_title('Coupler Curve', fontweight='bold')
        ax1.set_xlabel('X (mm)')
        ax1.set_ylabel('Y (mm)')
        ax1.legend(loc='best', fontsize=9)
        
        # ========== VELOCITY vs ANGLE ==========
        ax2.plot(data['angles'], data['velocities'], 'b-', linewidth=2.5)
        ax2.fill_between(data['angles'], data['velocities'], alpha=0.3)
        
        # Mark max and min
        max_vel_idx = np.argmax(data['velocities'])
        min_vel_idx = np.argmin(data['velocities'])
        
        ax2.plot(data['angles'][max_vel_idx], data['velocities'][max_vel_idx], 
                'ro', markersize=10, label=f'Max: {data["velocities"][max_vel_idx]:.1f} mm/s')
        ax2.plot(data['angles'][min_vel_idx], data['velocities'][min_vel_idx], 
                'go', markersize=10, label=f'Min: {data["velocities"][min_vel_idx]:.1f} mm/s')
        
        ax2.grid(True, alpha=0.3)
        ax2.set_title('Coupler Point Velocity vs Crank Angle', fontweight='bold')
        ax2.set_xlabel('Crank Angle θ₂ (degrees)')
        ax2.set_ylabel('Velocity (mm/s)')
        ax2.legend(loc='best', fontsize=9)
        ax2.set_xlim([0, 360])
        
        # ========== ACCELERATION vs ANGLE ==========
        ax3.plot(data['angles'], data['accelerations'], 'r-', linewidth=2.5)
        ax3.fill_between(data['angles'], data['accelerations'], alpha=0.3, color='red')
        
        # Mark max and min
        max_acc_idx = np.argmax(data['accelerations'])
        min_acc_idx = np.argmin(data['accelerations'])
        
        ax3.plot(data['angles'][max_acc_idx], data['accelerations'][max_acc_idx], 
                'ro', markersize=10, label=f'Max: {data["accelerations"][max_acc_idx]:.1f} mm/s²')
        ax3.plot(data['angles'][min_acc_idx], data['accelerations'][min_acc_idx], 
                'go', markersize=10, label=f'Min: {data["accelerations"][min_acc_idx]:.1f} mm/s²')
        
        ax3.grid(True, alpha=0.3)
        ax3.set_title('Coupler Point Acceleration vs Crank Angle', fontweight='bold')
        ax3.set_xlabel('Crank Angle θ₂ (degrees)')
        ax3.set_ylabel('Acceleration (mm/s²)')
        ax3.legend(loc='best', fontsize=9)
        ax3.set_xlim([0, 360])
        
        canvas = FigureCanvasTkAgg(fig, master=plot_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        # Display statistics
        stats_text = f"""Statistics: Vel: Max={np.max(data['velocities']):.1f}, Min={np.min(data['velocities']):.1f}, Avg={np.mean(data['velocities']):.1f} mm/s | Acc: Max={np.max(data['accelerations']):.1f}, Min={np.min(data['accelerations']):.1f}, Avg={np.mean(data['accelerations']):.1f} mm/s²"""
        
        result_label = Label(plot_win, text=stats_text, font=("Courier", 8), 
                            justify=LEFT, bg="lightgreen")
        result_label.pack(pady=5)
        
        print("\n✓ Coupler curve analysis complete!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Analysis failed: {str(e)}")


# For testing standalone
if __name__ == "__main__":
    root = Tk()
    root.title("Coupler Curve Analysis - Test")
    root.geometry("300x200")
    
    Label(root, text="Coupler Curve Analysis Module", 
          font=("Arial", 12, "bold")).pack(pady=30)
    
    btn = Button(root, text="Open Coupler Analysis", 
                command=lambda: open_coupler_analysis_window(root),
                width=25, height=2, bg="lightblue")
    btn.pack(pady=10)
    
    root.mainloop()