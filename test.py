import re
import matplotlib.pyplot as plt

def parse_maude_num(s):
    """Converts Maude numbers/fractions to floats."""
    s = s.strip()
    if '/' in s:
        num, den = s.split('/')
        return float(num) / float(den)
    return float(s)

def parse_maude_vector(v_str):
    """Parses v(x, y) into (x, y) tuple."""
    # Clean up any potential whitespace inside the vector string
    v_str = v_str.replace(' ', '').replace('\n', '')
    coords = v_str.replace('v(', '').replace(')', '').split(',')
    return (parse_maude_num(coords[0]), parse_maude_num(coords[1]))

def extract_drones(text):
    """Improved regex to handle multiple drones across lines."""
    drones = {}
    # Matches the whole drone object block
    drone_pattern = re.compile(r"< d\((\d+)\) : Drone \| (.*?) >", re.DOTALL)
    
    for match in drone_pattern.finditer(text):
        d_id = match.group(1)
        attr_block = match.group(2)
        
        # Look for attributes specifically, allowing for flexible spacing/newlines
        pos_match = re.search(r"pos\s*:\s*(v\([^)]+\))", attr_block)
        est_match = re.search(r"estPos\s*:\s*(v\([^)]+\))", attr_block)
        goal_match = re.search(r"goalPos\s*:\s*(v\([^)]+\))", attr_block)
        if pos_match:
            drones[d_id] = {
                'pos': parse_maude_vector(pos_match.group(1)),
                'est': parse_maude_vector(est_match.group(1)) if est_match else (0.0, 0.0),
                'goal': parse_maude_vector(goal_match.group(1)) if goal_match else (0.0, 0.0)
            }
            
    return drones

def visualize_flight(initial_str, final_str):
    start_data = extract_drones(initial_str)
    end_data = extract_drones(final_str)
    
    plt.figure(figsize=(15, 15))
    plt.xlim(0, 40)
    plt.ylim(0, 40)
    
    # --- Recovery Zone ---
    recovery_zone = plt.Circle((15, 15), 8, color='green', fill=True, alpha=0.1, linestyle='--')
    plt.gca().add_patch(recovery_zone)
    plt.scatter(15, 15, color='green', marker='+', s=100, alpha=0.5)
    
    for d_id in start_data:
        s_pos = start_data[d_id]['pos']
        g_pos = start_data[d_id]['goal']

        # Plot Start
        plt.scatter(s_pos[0], s_pos[1], color='gray', marker='o', s=80, alpha=0.5)
        plt.text(s_pos[0], s_pos[1] + 1.0, f"d({d_id}) Start", fontsize=8, color='gray', ha='center')

        plt.scatter(g_pos[0], g_pos[1], color='red', marker='*', s=150, edgecolors='black', label="Goal" if d_id == '1' else "")
        plt.text(g_pos[0], g_pos[1] + 1.2, f"d({d_id}) Goal", fontsize=8, color='red', ha='center', fontweight='bold')

        if d_id in end_data:
            d = end_data[d_id]
            actual_pos = d['pos']
            est_pos = d['est']
            
            # Line: Start -> Actual
            plt.plot([s_pos[0], actual_pos[0]], [s_pos[1], actual_pos[1]], color='blue', alpha=0.3, linewidth=2)
            
            # Actual Pos
            plt.scatter(actual_pos[0], actual_pos[1], color='blue', marker='>', s=100)
            plt.text(actual_pos[0], actual_pos[1] + 1.0, f"d({d_id}) Act", fontsize=9, color='blue', fontweight='bold', ha='center')
            
            # Estimated Pos
            plt.scatter(est_pos[0], est_pos[1], color='orange', marker='o', s=100, edgecolors='black')
            plt.text(est_pos[0], est_pos[1] - 1.5, f"d({d_id}) Est", fontsize=9, color='darkorange', fontweight='bold', ha='center')
            
            # Error line (Actual to Estimated)
            plt.plot([actual_pos[0], est_pos[0]], [actual_pos[1], est_pos[1]], color='red', linestyle=':', alpha=0.5)
        else:
            # Crashed
            plt.scatter(s_pos[0], s_pos[1], color='red', marker='x', s=200, linewidth=3)
            plt.text(s_pos[0], s_pos[1] - 1.8, f"d({d_id}) CRASHED", color='red', fontweight='bold', ha='center')

    plt.title("Drone Tracking Map (40x40)")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.gca().set_aspect('equal')
    plt.show()

# --- SPREAD OUT DATA FOR VISIBILITY ---
initial_config = """
{ < d(1) : Drone | pos : v(10, 10), estPos : v(10, 10), goalPos : v(25, 25), 
>            belief : 1/1, speed : 0/1, heading : stop, inbox : emptyMsg > , 0 }"""

final_config = """
{< d(1) : Drone | pos : v(15, 15), estPos : v(20, 20), goalPos : v(25, 25), belief : 49/50, speed : 1, heading
    : SE, inbox : emptyMsg >, 20}
    """

visualize_flight(initial_config, final_config)
# rew [20] { < d(1) : Drone | pos : v(10, 10), estPos : v(10, 10), goalPos : v(12, 12), 
#            belief : 1/1, speed : 0/1, heading : stop, inbox : emptyMsg > , 0 } .