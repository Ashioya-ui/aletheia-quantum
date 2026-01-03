import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set style to dark background for high-contrast "Quantum Lab" aesthetic
plt.style.use('dark_background')

def render_fafo_braid():
    """
    Renders the Sigma-X Braiding Sequence (Bridge-8) in 3D Spacetime.
    Sequence: (s1 s2 s1^-1)^4 s3^2
    """
    print("--- ALETHEIA BRAID RENDERER ---")
    print("Generating spacetime trajectory for Sigma-X...")

    # Configuration
    num_anyons = 4
    
    # Initialize paths: Dictionary of lists [x, y, t] for each particle
    # X = Spatial Position on Nanowire
    # Y = Topological Depth (Over/Under)
    # T = Time
    paths = {0: [], 1: [], 2: [], 3: []}
    
    # SLOT TRACKING (Red Team Fix):
    # Instead of checking float positions, we track which particle ID is in which slot.
    # slots[0] = Particle ID at position 0, etc.
    slots = [0, 1, 2, 3]
    
    # The Sigma-X Sequence
    # (Index of swap [0,1,2], Direction +1/-1)
    # s1 swaps slots 0&1, s2 swaps 1&2, s3 swaps 2&3
    block = [(0, 1), (1, 1), (0, -1)]
    tail = [(2, 1), (2, 1)]
    sequence = (block * 4) + tail
    
    time_per_move = 1.0
    t_current = 0.0
    
    # Initial state recording
    for slot_idx, particle_id in enumerate(slots):
        paths[particle_id].append([float(slot_idx), 0.0, 0.0])

    # Process the Braid
    for step_idx, (swap_slot_idx, sign) in enumerate(sequence):
        
        # Identify particles involved in this swap
        # Left particle is at swap_slot_idx
        # Right particle is at swap_slot_idx + 1
        p_left_id = slots[swap_slot_idx]
        p_right_id = slots[swap_slot_idx + 1]
        
        # Interpolation steps (Higher = Smoother curves)
        sub_steps = 50
        
        for i in range(1, sub_steps + 1):
            progress = i / sub_steps
            t_now = t_current + progress * time_per_move
            
            # Parametric Swap Logic (180 degree rotation in 3D)
            theta = progress * np.pi
            center_x = swap_slot_idx + 0.5
            
            # Calculate positions relative to center
            # Cosine gives the X transition (0.5 -> -0.5)
            dx = 0.5 * np.cos(theta)
            
            # Sine gives the Y (Depth) arc. 
            # Sign determines Over (+Y) vs Under (-Y)
            dy = sign * 0.5 * np.sin(theta)
            
            # Left Particle moves Right (Start at -0.5, End at +0.5)
            # x = center - dx (since cos(0)=1, center-0.5 = start)
            x_L = center_x - dx
            y_L = dy # Arcs up/down based on sign
            
            # Right Particle moves Left
            x_R = center_x + dx
            y_R = -dy # Inverse arc
            
            paths[p_left_id].append([x_L, y_L, t_now])
            paths[p_right_id].append([x_R, y_R, t_now])
            
            # Non-moving particles: Linear interpolation in Time only
            for particle_id in range(num_anyons):
                if particle_id != p_left_id and particle_id != p_right_id:
                    # Find current integer slot of this particle
                    current_pos = float(slots.index(particle_id))
                    paths[particle_id].append([current_pos, 0.0, t_now])
        
        # Update Slot Array (The Swap)
        slots[swap_slot_idx], slots[swap_slot_idx + 1] = slots[swap_slot_idx + 1], slots[swap_slot_idx]
        
        t_current += time_per_move

    # Plotting
    fig = plt.figure(figsize=(12, 10))
    # Make plot background transparent for dark mode blending
    fig.patch.set_alpha(0.0) 
    
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('none') # Transparent axis background
    
    # Neon Color Palette
    colors = ['#FF0055', '#00FFFF', '#FFFF00', '#9D00FF']
    
    for p in range(num_anyons):
        data = np.array(paths[p])
        # Plot: X=Pos, Y=Time, Z=Depth
        # We map Data Z -> Plot Y (Time vertical)
        # We map Data Y -> Plot Z (Depth)
        ax.plot(data[:, 0], data[:, 2], data[:, 1], 
                linewidth=2.5, color=colors[p], label=f'Anyon {p+1}', alpha=0.9)

    # Styling
    ax.set_xlabel('Nanowire Position', color='white')
    ax.set_ylabel('Time (arb. units)', color='white')
    ax.set_zlabel('Topological Depth', color='white')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    
    # Remove pane fills for clean look
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Set Grid Color
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0.2)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0.2)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0.2)

    ax.set_title('Aletheia Sigma-X Sequence (Bridge-8)', color='white', fontsize=16, pad=20)
    
    # Optimal View Angle
    ax.view_init(elev=25, azim=-60)
    
    plt.legend(facecolor='black', edgecolor='white', labelcolor='white')
    
    output_filename = "sigma_x_braid_dark.png"
    print(f"Rendering complete. Saving to '{output_filename}'...")
    plt.savefig(output_filename, dpi=300, facecolor='black')
    # plt.show() # Uncomment to view interactively

if __name__ == "__main__":
    render_fafo_braid()