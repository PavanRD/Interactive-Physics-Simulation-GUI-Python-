import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from A_four_bar_animation import launch_animation
from B_non_grishof import launch_non_grashof_animation
from C_slider_crank import launch_crank_slider_animation

# 1. The Grashof Logic Engine
def check_grashof(e1, e2, e3, e4):
    try:
        l1 = float(e1.get())
        l2 = float(e2.get())
        l3 = float(e3.get())
        l4 = float(e4.get())
        
        links = sorted([l1, l2, l3, l4])
        
        S = links[0]
        P = links[1]
        Q = links[2]
        L = links[3]
        
        if L >= S + P + Q:
            messagebox.showerror("Geometry Error", "These links cannot form a closed loop!")
            return
        
        if S + L <= P + Q:
            launch_animation(l1, l2, l3, l4)
        else:
            launch_non_grashof_animation(l1, l2, l3, l4)
            
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all link lengths.")


def open_four_bar_window():
    four_bar_win = Toplevel(root) 
    four_bar_win.title("Four Bar Mechanism - Inputs")
    four_bar_win.geometry("300x350")
    
    Label(four_bar_win, text="Enter Link Lengths:", font=("Arial", 12, "bold")).pack(pady=10)
    
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
    
    check_btn = Button(four_bar_win, text="Check Mechanism", 
                       command=lambda: check_grashof(entry1, entry2, entry3, entry4),
                       width=20, bg="lightgray")
    check_btn.pack(pady=20)


def check_crank_slider(e_r, e_l):
    try:
        r = float(e_r.get())
        l = float(e_l.get())
        
        launch_crank_slider_animation(r, l)
            
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for r and l.")


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


# ==================== PLOTS SECTION ====================

def open_plots_window():
    plots_win = Toplevel(root)
    plots_win.title("Kinematic Analysis Plots")
    plots_win.geometry("400x300")
    
    Label(plots_win, text="Select Analysis Type:", font=("Arial", 14, "bold")).pack(pady=20)
    
    btn_fourbar_plots = Button(plots_win, text="Four-Bar Mechanism Analysis", 
                               command=open_fourbar_analysis, 
                               width=30, height=2, bg="lightblue")
    btn_fourbar_plots.pack(pady=10)
    
    btn_slider_plots = Button(plots_win, text="Crank-Slider Analysis", 
                             command=open_slider_analysis, 
                             width=30, height=2, bg="lightgreen")
    btn_slider_plots.pack(pady=10)


def open_fourbar_analysis():
    """Four-bar mechanism kinematic analysis"""
    analysis_win = Toplevel(root)
    analysis_win.title("Four-Bar Mechanism - Kinematic Analysis")
    analysis_win.geometry("450x550")
    
    Label(analysis_win, text="Four-Bar Mechanism Analysis", 
          font=("Arial", 12, "bold")).pack(pady=10)
    
    # Input fields - NOW BLANK by default
    Label(analysis_win, text="Link Lengths (mm):").pack()
    
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
    
    Label(analysis_win, text="θ₂ (degrees):").pack()
    e_theta = Entry(analysis_win)
    e_theta.pack(pady=3)
    
    Label(analysis_win, text="ω₂ (rad/s):").pack()
    e_omega = Entry(analysis_win)
    e_omega.pack(pady=3)
    
    Label(analysis_win, text="α₂ (rad/s²):").pack()
    e_alpha = Entry(analysis_win)
    e_alpha.pack(pady=3)
    
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
        e_theta.delete(0, END)
        e_theta.insert(0, "45")
        e_omega.delete(0, END)
        e_omega.insert(0, "2.0")
        e_alpha.delete(0, END)
        e_alpha.insert(0, "0.0")
    
    btn_example = Button(btn_frame, text="Load Example", command=load_example,
                        width=15, bg="lightyellow")
    btn_example.pack(side=LEFT, padx=5)
    
    btn_generate = Button(btn_frame, text="Static Analysis", 
                         command=lambda: generate_fourbar_plots(
                             float(e_l1.get()), float(e_l2.get()), 
                             float(e_l3.get()), float(e_l4.get()),
                             float(e_theta.get()), float(e_omega.get()), 
                             float(e_alpha.get())),
                         width=15, bg="orange")
    btn_generate.pack(side=LEFT, padx=5)
    
    # NEW: Animated Analysis button
    btn_animated = Button(analysis_win, text="🎬 Animated Analysis (All Angles)", 
                         command=lambda: generate_fourbar_animated(
                             float(e_l1.get()), float(e_l2.get()), 
                             float(e_l3.get()), float(e_l4.get()),
                             float(e_omega.get()), float(e_alpha.get())),
                         width=30, height=2, bg="lightcoral")
    btn_animated.pack(pady=10)


def open_slider_analysis():
    """Crank-slider mechanism kinematic analysis"""
    analysis_win = Toplevel(root)
    analysis_win.title("Crank-Slider - Kinematic Analysis")
    analysis_win.geometry("450x450")
    
    Label(analysis_win, text="Crank-Slider Analysis", 
          font=("Arial", 12, "bold")).pack(pady=10)
    
    Label(analysis_win, text="Link Lengths (mm):").pack()
    
    Label(analysis_win, text="Crank Radius (r):").pack()
    e_r = Entry(analysis_win)
    e_r.pack(pady=3)
    
    Label(analysis_win, text="Connecting Rod (l):").pack()
    e_l = Entry(analysis_win)
    e_l.pack(pady=3)
    
    Label(analysis_win, text="θ (degrees):").pack()
    e_theta = Entry(analysis_win)
    e_theta.pack(pady=3)
    
    Label(analysis_win, text="ω (rad/s):").pack()
    e_omega = Entry(analysis_win)
    e_omega.pack(pady=3)
    
    Label(analysis_win, text="α (rad/s²):").pack()
    e_alpha = Entry(analysis_win)
    e_alpha.pack(pady=3)
    
    # Buttons frame
    btn_frame = Frame(analysis_win)
    btn_frame.pack(pady=10)
    
    # Load Example button
    def load_example():
        e_r.delete(0, END)
        e_r.insert(0, "50")
        e_l.delete(0, END)
        e_l.insert(0, "150")
        e_theta.delete(0, END)
        e_theta.insert(0, "45")
        e_omega.delete(0, END)
        e_omega.insert(0, "2.0")
        e_alpha.delete(0, END)
        e_alpha.insert(0, "0.0")
    
    btn_example = Button(btn_frame, text="Load Example", command=load_example,
                        width=15, bg="lightyellow")
    btn_example.pack(side=LEFT, padx=5)
    
    btn_generate = Button(btn_frame, text="Static Analysis", 
                         command=lambda: generate_slider_plots(
                             float(e_r.get()), float(e_l.get()),
                             float(e_theta.get()), float(e_omega.get()), 
                             float(e_alpha.get())),
                         width=15, bg="orange")
    btn_generate.pack(side=LEFT, padx=5)
    
    # NEW: Animated Analysis button
    btn_animated = Button(analysis_win, text="🎬 Animated Analysis (All Angles)", 
                         command=lambda: generate_slider_animated(
                             float(e_r.get()), float(e_l.get()),
                             float(e_omega.get()), float(e_alpha.get())),
                         width=30, height=2, bg="lightcoral")
    btn_animated.pack(pady=10)


# ============ ANIMATED FOUR-BAR ANALYSIS ============

def generate_fourbar_animated(L1, L2, L3, L4, omega2, alpha2):
    """Generate animated position, velocity, and acceleration diagrams"""
    try:
        plot_win = Toplevel(root)
        plot_win.title("Four-Bar Animated Analysis")
        plot_win.geometry("1400x550")
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5))
        fig.suptitle(f'Four-Bar Animated Analysis (ω₂={omega2} rad/s, α₂={alpha2} rad/s²)', 
                     fontsize=12, fontweight='bold')
        
        # Animation state
        anim_running = [True]  # Use list to make it mutable in nested function
        current_frame = [0]
        
        # Generate angles
        angles = np.linspace(0, 2*np.pi, 180)
        
        def update_frame(frame_num):
            if not anim_running[0]:
                return
            
            theta2 = angles[frame_num]
            current_frame[0] = frame_num
            
            pos = fourbar_position(L1, L2, L3, L4, theta2)
            if pos is None:
                return
            
            vel = fourbar_velocity(L1, L2, L3, L4, theta2, omega2, pos)
            acc = fourbar_acceleration(L1, L2, L3, L4, theta2, omega2, alpha2, pos, vel)
            
            # Clear and redraw all axes
            ax1.clear()
            ax2.clear()
            ax3.clear()
            
            plot_fourbar_position(ax1, L1, L2, L3, L4, pos)
            ax1.set_title(f'Position (θ₂={np.degrees(theta2):.1f}°)', fontweight='bold')
            
            plot_fourbar_velocity(ax2, vel)
            ax2.set_title(f'Velocity (VB={vel["VB_mag"]:.1f} mm/s)', fontweight='bold')
            
            plot_fourbar_acceleration(ax3, acc)
            ax3.set_title(f'Acceleration (aB={acc["aB_mag"]:.1f} mm/s²)', fontweight='bold')
            
            result_label.config(text=f"Frame {frame_num+1}/180 | θ₂={np.degrees(theta2):.1f}° | "
                                    f"ω₃={vel['omega3']:.3f} rad/s | α₃={acc['alpha3']:.3f} rad/s²")
        
        # Control buttons
        control_frame = Frame(plot_win)
        control_frame.pack(side=BOTTOM, pady=5)
        
        def play_pause():
            anim_running[0] = not anim_running[0]
            btn_play.config(text="⏸ Pause" if anim_running[0] else "▶ Play")
            if anim_running[0]:
                anim.event_source.start()
            else:
                anim.event_source.stop()
        
        def reset():
            anim_running[0] = False
            anim.event_source.stop()
            update_frame(0)
            btn_play.config(text="▶ Play")
        
        btn_play = Button(control_frame, text="⏸ Pause", command=play_pause, width=12, bg="lightgreen")
        btn_play.pack(side=LEFT, padx=5)
        
        btn_reset = Button(control_frame, text="⏮ Reset", command=reset, width=12, bg="lightblue")
        btn_reset.pack(side=LEFT, padx=5)
        
        result_label = Label(plot_win, text="", font=("Courier", 10), bg="lightyellow")
        result_label.pack(side=BOTTOM, pady=5)
        
        canvas = FigureCanvasTkAgg(fig, master=plot_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        anim = animation.FuncAnimation(fig, update_frame, frames=len(angles),
                                      interval=50, repeat=True, blit=False)
        
    except Exception as e:
        messagebox.showerror("Error", f"Animation failed: {str(e)}")


# ============ ANIMATED CRANK-SLIDER ANALYSIS ============

def generate_slider_animated(r, l, omega, alpha):
    """Generate animated position, velocity, and acceleration diagrams"""
    try:
        plot_win = Toplevel(root)
        plot_win.title("Crank-Slider Animated Analysis")
        plot_win.geometry("1400x550")
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5))
        fig.suptitle(f'Crank-Slider Animated Analysis (ω={omega} rad/s, α={alpha} rad/s²)', 
                     fontsize=12, fontweight='bold')
        
        anim_running = [True]
        current_frame = [0]
        
        angles = np.linspace(0, 2*np.pi, 180)
        
        def update_frame(frame_num):
            if not anim_running[0]:
                return
            
            theta = angles[frame_num]
            current_frame[0] = frame_num
            
            pos = slider_position(r, l, theta)
            vel = slider_velocity(r, l, theta, omega, pos)
            acc = slider_acceleration(r, l, theta, omega, alpha, pos, vel)
            
            ax1.clear()
            ax2.clear()
            ax3.clear()
            
            plot_slider_position(ax1, r, l, pos, theta)
            ax1.set_title(f'Position (θ={np.degrees(theta):.1f}°, x={pos["x"]:.1f}mm)', fontweight='bold')
            
            plot_slider_velocity(ax2, r, omega, theta, vel)
            ax2.set_title(f'Velocity (v={vel["v"]:.1f} mm/s)', fontweight='bold')
            
            plot_slider_acceleration(ax3, r, omega, alpha, theta, acc)
            ax3.set_title(f'Acceleration (a={acc["a"]:.1f} mm/s²)', fontweight='bold')
            
            result_label.config(text=f"Frame {frame_num+1}/180 | θ={np.degrees(theta):.1f}° | "
                                    f"φ={np.degrees(pos['phi']):.1f}° | ω_rod={vel['omega_rod']:.3f} rad/s")
        
        control_frame = Frame(plot_win)
        control_frame.pack(side=BOTTOM, pady=5)
        
        def play_pause():
            anim_running[0] = not anim_running[0]
            btn_play.config(text="⏸ Pause" if anim_running[0] else "▶ Play")
            if anim_running[0]:
                anim.event_source.start()
            else:
                anim.event_source.stop()
        
        def reset():
            anim_running[0] = False
            anim.event_source.stop()
            update_frame(0)
            btn_play.config(text="▶ Play")
        
        btn_play = Button(control_frame, text="⏸ Pause", command=play_pause, width=12, bg="lightgreen")
        btn_play.pack(side=LEFT, padx=5)
        
        btn_reset = Button(control_frame, text="⏮ Reset", command=reset, width=12, bg="lightblue")
        btn_reset.pack(side=LEFT, padx=5)
        
        result_label = Label(plot_win, text="", font=("Courier", 10), bg="lightcyan")
        result_label.pack(side=BOTTOM, pady=5)
        
        canvas = FigureCanvasTkAgg(fig, master=plot_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        anim = animation.FuncAnimation(fig, update_frame, frames=len(angles),
                                      interval=50, repeat=True, blit=False)
        
    except Exception as e:
        messagebox.showerror("Error", f"Animation failed: {str(e)}")


# ============ STATIC PLOT FUNCTIONS (Original) ============

def generate_fourbar_plots(L1, L2, L3, L4, theta2_deg, omega2, alpha2):
    """Generate static position, velocity, and acceleration diagrams"""
    try:
        theta2 = np.radians(theta2_deg)
        
        pos = fourbar_position(L1, L2, L3, L4, theta2)
        if pos is None:
            messagebox.showerror("Error", "Cannot assemble mechanism at this angle!")
            return
        
        vel = fourbar_velocity(L1, L2, L3, L4, theta2, omega2, pos)
        acc = fourbar_acceleration(L1, L2, L3, L4, theta2, omega2, alpha2, pos, vel)
        
        plot_win = Toplevel(root)
        plot_win.title("Four-Bar Analysis Results")
        plot_win.geometry("1400x500")
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5))
        fig.suptitle(f'Four-Bar Analysis (θ₂={theta2_deg}°, ω₂={omega2} rad/s, α₂={alpha2} rad/s²)', 
                     fontsize=12, fontweight='bold')
        
        plot_fourbar_position(ax1, L1, L2, L3, L4, pos)
        plot_fourbar_velocity(ax2, vel)
        plot_fourbar_acceleration(ax3, acc)
        
        canvas = FigureCanvasTkAgg(fig, master=plot_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        results_text = f"""Position: θ₂={theta2_deg:.1f}°, θ₃={np.degrees(pos['theta3']):.1f}°, θ₄={np.degrees(pos['theta4']):.1f}°
Velocity: VB={vel['VB_mag']:.1f} mm/s, VC={vel['VC_mag']:.1f} mm/s, ω₃={vel['omega3']:.3f} rad/s, ω₄={vel['omega4']:.3f} rad/s
Acceleration: aB={acc['aB_mag']:.1f} mm/s², aC={acc['aC_mag']:.1f} mm/s², α₃={acc['alpha3']:.3f} rad/s², α₄={acc['alpha4']:.3f} rad/s²"""
        
        result_label = Label(plot_win, text=results_text, font=("Courier", 9), 
                            justify=LEFT, bg="lightyellow")
        result_label.pack(pady=5)
        
    except Exception as e:
        messagebox.showerror("Error", f"Analysis failed: {str(e)}")


def generate_slider_plots(r, l, theta_deg, omega, alpha):
    """Generate static diagrams for crank-slider"""
    try:
        theta = np.radians(theta_deg)
        
        pos = slider_position(r, l, theta)
        vel = slider_velocity(r, l, theta, omega, pos)
        acc = slider_acceleration(r, l, theta, omega, alpha, pos, vel)
        
        plot_win = Toplevel(root)
        plot_win.title("Crank-Slider Analysis Results")
        plot_win.geometry("1400x500")
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5))
        fig.suptitle(f'Crank-Slider Analysis (θ={theta_deg}°, ω={omega} rad/s, α={alpha} rad/s²)', 
                     fontsize=12, fontweight='bold')
        
        plot_slider_position(ax1, r, l, pos, theta)
        plot_slider_velocity(ax2, r, omega, theta, vel)
        plot_slider_acceleration(ax3, r, omega, alpha, theta, acc)
        
        canvas = FigureCanvasTkAgg(fig, master=plot_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        results_text = f"""Position: x={pos['x']:.1f} mm, φ={np.degrees(pos['phi']):.1f}°
Velocity: v={vel['v']:.1f} mm/s, ω_rod={vel['omega_rod']:.3f} rad/s
Acceleration: a={acc['a']:.1f} mm/s², α_rod={acc['alpha_rod']:.3f} rad/s²"""
        
        result_label = Label(plot_win, text=results_text, font=("Courier", 9), 
                            justify=LEFT, bg="lightcyan")
        result_label.pack(pady=5)
        
    except Exception as e:
        messagebox.showerror("Error", f"Analysis failed: {str(e)}")


# ============ Analysis Functions (Same as before) ============

def fourbar_position(L1, L2, L3, L4, theta2):
    Ax, Ay = 0, 0
    Dx, Dy = L1, 0
    Bx = L2 * np.cos(theta2)
    By = L2 * np.sin(theta2)
    
    K1 = L1 / L2
    K2 = L1 / L4
    K3 = (L2**2 - L3**2 + L4**2 + L1**2) / (2 * L2 * L4)
    
    A = np.cos(theta2) - K1 - K2 * np.cos(theta2) + K3
    B = -2 * np.sin(theta2)
    C = K1 - (K2 + 1) * np.cos(theta2) + K3
    
    discriminant = B**2 - 4*A*C
    if discriminant < 0:
        return None
    
    theta4 = 2 * np.arctan2(-B + np.sqrt(discriminant), 2*A)
    
    K4 = L1 / L3
    K5 = (L4**2 - L1**2 - L2**2 - L3**2) / (2 * L2 * L3)
    
    D = np.cos(theta2) - K1 + K4 * np.cos(theta2) + K5
    E = -2 * np.sin(theta2)
    F = K1 + (K4 - 1) * np.cos(theta2) + K5
    
    discriminant = E**2 - 4*D*F
    if discriminant < 0:
        return None
    
    theta3 = 2 * np.arctan2(-E + np.sqrt(discriminant), 2*D)
    
    Cx = Dx - L4 * np.cos(theta4)
    Cy = Dy + L4 * np.sin(theta4)
    
    return {
        'A': (Ax, Ay), 'B': (Bx, By), 'C': (Cx, Cy), 'D': (Dx, Dy),
        'theta3': theta3, 'theta4': theta4
    }


def fourbar_velocity(L1, L2, L3, L4, theta2, omega2, pos):
    theta3 = pos['theta3']
    theta4 = pos['theta4']
    
    VBx = -omega2 * L2 * np.sin(theta2)
    VBy = omega2 * L2 * np.cos(theta2)
    VB = np.sqrt(VBx**2 + VBy**2)
    
    omega3 = (omega2 * L2 * np.sin(theta4 - theta2)) / (L3 * np.sin(theta3 - theta4))
    omega4 = (omega2 * L2 * np.sin(theta2 - theta3)) / (L4 * np.sin(theta4 - theta3))
    
    VCx = -omega4 * L4 * np.sin(theta4)
    VCy = omega4 * L4 * np.cos(theta4)
    VC = np.sqrt(VCx**2 + VCy**2)
    
    return {
        'VB': (VBx, VBy), 'VB_mag': VB,
        'VC': (VCx, VCy), 'VC_mag': VC,
        'omega3': omega3, 'omega4': omega4
    }


def fourbar_acceleration(L1, L2, L3, L4, theta2, omega2, alpha2, pos, vel):
    theta3 = pos['theta3']
    theta4 = pos['theta4']
    omega3 = vel['omega3']
    omega4 = vel['omega4']
    
    aBx = -omega2**2 * L2 * np.cos(theta2) - alpha2 * L2 * np.sin(theta2)
    aBy = -omega2**2 * L2 * np.sin(theta2) + alpha2 * L2 * np.cos(theta2)
    
    num = (omega2**2 * L2 * np.cos(theta2) + omega4**2 * L4 * np.cos(theta4) - 
           omega3**2 * L3 * np.cos(theta3))
    den = L3 * np.sin(theta3)
    denom_alpha = (den * np.cos(theta4) - L4 * np.sin(theta4) * np.cos(theta3))
    
    alpha3 = ((alpha2 * L2 * np.sin(theta2) - num * np.cos(theta4)) / 
             denom_alpha) if abs(denom_alpha) > 1e-6 else 0
    
    alpha4 = ((alpha2 * L2 * np.sin(theta2) + alpha3 * L3 * np.sin(theta3) - 
              omega2**2 * L2 * np.cos(theta2) + omega3**2 * L3 * np.cos(theta3)) / 
             (L4 * np.sin(theta4))) if abs(np.sin(theta4)) > 1e-6 else 0
    
    aCBx = -omega3**2 * L3 * np.cos(theta3) - alpha3 * L3 * np.sin(theta3)
    aCBy = -omega3**2 * L3 * np.sin(theta3) + alpha3 * L3 * np.cos(theta3)
    
    aCx = aBx + aCBx
    aCy = aBy + aCBy
    
    return {
        'aB': (aBx, aBy), 'aB_mag': np.sqrt(aBx**2 + aBy**2),
        'aC': (aCx, aCy), 'aC_mag': np.sqrt(aCx**2 + aCy**2),
        'alpha3': alpha3, 'alpha4': alpha4
    }


def slider_position(r, l, theta):
    x = r * np.cos(theta) + np.sqrt(l**2 - r**2 * np.sin(theta)**2)
    phi = np.arcsin((r * np.sin(theta)) / l)
    return {'x': x, 'phi': phi}


def slider_velocity(r, l, theta, omega, pos):
    phi = pos['phi']
    v = -r * omega * np.sin(theta) - l * (r * omega * np.cos(theta) / (l * np.cos(phi))) * np.sin(phi)
    omega_rod = (r * omega * np.cos(theta)) / (l * np.cos(phi))
    return {'v': v, 'omega_rod': omega_rod}


def slider_acceleration(r, l, theta, omega, alpha, pos, vel):
    phi = pos['phi']
    omega_rod = vel['omega_rod']
    
    alpha_rod = ((r * alpha * np.cos(theta) - r * omega**2 * np.sin(theta) + 
                 l * omega_rod**2 * np.sin(phi)) / (l * np.cos(phi)))
    
    a = (-r * alpha * np.sin(theta) - r * omega**2 * np.cos(theta) - 
         l * alpha_rod * np.sin(phi) - l * omega_rod**2 * np.cos(phi))
    
    return {'a': a, 'alpha_rod': alpha_rod}


# ============ Plotting Functions ============

def plot_fourbar_position(ax, L1, L2, L3, L4, pos):
    A, B, C, D = pos['A'], pos['B'], pos['C'], pos['D']
    
    ax.plot([A[0], D[0]], [A[1], D[1]], 'o-', linewidth=8, color='gray', markersize=10)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'o-', linewidth=5, color='blue', markersize=10)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'o-', linewidth=5, color='green', markersize=10)
    ax.plot([C[0], D[0]], [C[1], D[1]], 'o-', linewidth=5, color='orange', markersize=10)
    
    ax.text(A[0]-15, A[1]-15, 'A', fontsize=11, fontweight='bold')
    ax.text(B[0]-15, B[1]+15, 'B', fontsize=11, fontweight='bold')
    ax.text(C[0]+15, C[1]+15, 'C', fontsize=11, fontweight='bold')
    ax.text(D[0]+15, D[1]-15, 'D', fontsize=11, fontweight='bold')
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')


def plot_fourbar_velocity(ax, vel):
    VBx, VBy = vel['VB']
    VCx, VCy = vel['VC']
    
    vel_max = max(abs(VBx), abs(VBy), abs(VCx), abs(VCy)) * 1.3
    
    ax.plot(0, 0, 'ko', markersize=10)
    ax.arrow(0, 0, VBx*0.9, VBy*0.9, head_width=vel_max*0.08, head_length=vel_max*0.06,
             fc='blue', ec='blue', linewidth=2.5)
    ax.arrow(0, 0, VCx*0.9, VCy*0.9, head_width=vel_max*0.08, head_length=vel_max*0.06,
             fc='green', ec='green', linewidth=2.5)
    ax.plot([VBx, VCx], [VBy, VCy], '--', color='orange', linewidth=2.5)
    
    ax.text(VBx/2, VBy/2+vel_max*0.08, 'VB', fontsize=10, color='blue', fontweight='bold')
    ax.text(VCx/2, VCy/2-vel_max*0.08, 'VC', fontsize=10, color='green', fontweight='bold')
    
    ax.set_xlim(-vel_max, vel_max)
    ax.set_ylim(-vel_max, vel_max)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Vx (mm/s)')
    ax.set_ylabel('Vy (mm/s)')


def plot_fourbar_acceleration(ax, acc):
    aBx, aBy = acc['aB']
    aCx, aCy = acc['aC']
    
    acc_max = max(abs(aBx), abs(aBy), abs(aCx), abs(aCy)) * 1.3
    
    ax.plot(0, 0, 'ko', markersize=10)
    ax.arrow(0, 0, aBx*0.9, aBy*0.9, head_width=acc_max*0.08, head_length=acc_max*0.06,
             fc='blue', ec='blue', linewidth=2.5)
    ax.arrow(0, 0, aCx*0.9, aCy*0.9, head_width=acc_max*0.08, head_length=acc_max*0.06,
             fc='green', ec='green', linewidth=2.5)
    ax.plot([aBx, aCx], [aBy, aCy], color='orange', linewidth=2.5)
    
    ax.text(aBx/2, aBy/2+acc_max*0.08, 'aB', fontsize=10, color='blue', fontweight='bold')
    ax.text(aCx/2, aCy/2-acc_max*0.08, 'aC', fontsize=10, color='green', fontweight='bold')
    
    ax.set_xlim(-acc_max, acc_max)
    ax.set_ylim(-acc_max, acc_max)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('ax (mm/s²)')
    ax.set_ylabel('ay (mm/s²)')


def plot_slider_position(ax, r, l, pos, theta):
    A = [0, 0]
    B = [r * np.cos(theta), r * np.sin(theta)]
    C = [pos['x'], 0]
    
    ax.plot([-r*0.5, pos['x']+l*0.3], [0, 0], 'k--', linewidth=1, alpha=0.5)
    ax.plot([A[0], B[0]], [A[1], B[1]], 'o-', linewidth=5, color='blue', markersize=10)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'o-', linewidth=5, color='green', markersize=10)
    ax.plot(C[0], C[1], 's', color='red', markersize=15)
    
    ax.text(A[0]-15, A[1]-15, 'A', fontsize=11, fontweight='bold')
    ax.text(B[0]-15, B[1]+15, 'B', fontsize=11, fontweight='bold')
    ax.text(C[0], C[1]+15, 'C', fontsize=11, fontweight='bold')
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')


def plot_slider_velocity(ax, r, omega, theta, vel):
    VBx = -r * omega * np.sin(theta)
    VBy = r * omega * np.cos(theta)
    VCx = vel['v']
    
    vel_max = max(abs(VBx), abs(VBy), abs(VCx)) * 1.3
    
    ax.plot(0, 0, 'ko', markersize=10)
    ax.arrow(0, 0, VBx*0.9, VBy*0.9, head_width=vel_max*0.08, head_length=vel_max*0.06,
             fc='blue', ec='blue', linewidth=2.5)
    ax.arrow(0, 0, VCx*0.9, 0, head_width=vel_max*0.08, head_length=vel_max*0.06,
             fc='green', ec='green', linewidth=2.5)
    ax.plot([VBx, VCx], [VBy, 0], '--', color='orange', linewidth=2.5)
    
    ax.text(VBx/2, VBy/2+vel_max*0.08, 'VB', fontsize=10, color='blue', fontweight='bold')
    ax.text(VCx/2, -vel_max*0.08, 'VC', fontsize=10, color='green', fontweight='bold')
    
    ax.set_xlim(-vel_max, vel_max)
    ax.set_ylim(-vel_max, vel_max)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Vx (mm/s)')
    ax.set_ylabel('Vy (mm/s)')


def plot_slider_acceleration(ax, r, omega, alpha, theta, acc):
    aBx = -r * omega**2 * np.cos(theta) - r * alpha * np.sin(theta)
    aBy = -r * omega**2 * np.sin(theta) + r * alpha * np.cos(theta)
    aCx = acc['a']
    
    acc_max = max(abs(aBx), abs(aBy), abs(aCx)) * 1.3
    
    ax.plot(0, 0, 'ko', markersize=10)
    ax.arrow(0, 0, aBx*0.9, aBy*0.9, head_width=acc_max*0.08, head_length=acc_max*0.06,
             fc='blue', ec='blue', linewidth=2.5)
    ax.arrow(0, 0, aCx*0.9, 0, head_width=acc_max*0.08, head_length=acc_max*0.06,
             fc='green', ec='green', linewidth=2.5)
    ax.plot([aBx, aCx], [aBy, 0], color='orange', linewidth=2.5)
    
    ax.text(aBx/2, aBy/2+acc_max*0.08, 'aB', fontsize=10, color='blue', fontweight='bold')
    ax.text(aCx/2, -acc_max*0.08, 'aC', fontsize=10, color='green', fontweight='bold')
    
    ax.set_xlim(-acc_max, acc_max)
    ax.set_ylim(-acc_max, acc_max)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('ax (mm/s²)')
    ax.set_ylabel('ay (mm/s²)')


# ==================== MAIN WINDOW ====================

root = Tk()
root.title("Main Menu")
root.geometry("400x350")

Label(root, text="Select an Option:", font=("Arial", 14)).pack(pady=30)

btn_four_bar = Button(root, text="Four Bar Mechanism", command=open_four_bar_window, width=25, height=2)
btn_four_bar.pack(pady=10)

btn_crank_slider = Button(root, text="Crank-Slider Mechanism", command=open_crank_slider_window, width=25, height=2)
btn_crank_slider.pack(pady=10)

btn_plots = Button(root, text="Plots (Kinematic Analysis)", command=open_plots_window, width=25, height=2)
btn_plots.pack(pady=10)

root.mainloop()