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
    # Matches the numbers inside v(...)
    coords = v_str.replace('v(', '').replace(')', '').split(',')
    return (parse_maude_num(coords[0]), parse_maude_num(coords[1]))

def extract_drones(text):
    """Uses your preferred regex logic to pull data from the Maude string."""
    drones = {}
    drone_pattern = re.compile(r"< d\((\d+)\) : Drone \| (.*?) >", re.DOTALL)
    
    for match in drone_pattern.finditer(text):
        d_id = match.group(1)
        attr_block = match.group(2)
        
        # Using the explicit regex patterns from your working code
        try:
            pos_match = re.search(r"pos:\s*(v\([^)]+\))", attr_block)
            goal_match = re.search(r"goalPos:\s*(v\([^)]+\))", attr_block)
            est_match = re.search(r"estPos:\s*(v\([^)]+\))", attr_block)
            belief_match = re.search(r"belief:\s*([\d/.]+)", attr_block)
            speed_match = re.search(r"speed:\s*([\d/.]+)", attr_block)

            drones[d_id] = {
                'pos': parse_maude_vector(pos_match.group(1)) if pos_match else (0.0, 0.0),
                'goal': parse_maude_vector(goal_match.group(1)) if goal_match else (0.0, 0.0),
                'est': parse_maude_vector(est_match.group(1)) if est_match else (0.0, 0.0),
                'belief': parse_maude_num(belief_match.group(1)) if belief_match else 0.0,
                'speed': parse_maude_num(speed_match.group(1)) if speed_match else 0.0
            }
        except Exception as e:
            print(f"Warning: Could not parse attributes for drone {d_id}: {e}")
            
    return drones

def visualize_flight(initial_str, final_str):
    start_data = extract_drones(initial_str)
    end_data = extract_drones(final_str)
    
    plt.figure(figsize=(12, 8))
    
    for d_id in start_data:
        # DATA FROM INPUT (Initial)
        s_pos = start_data[d_id]['pos']
        goal = start_data[d_id]['goal']
        
        # Plot Start (Gray Circle) and Goal (Green Star) from INPUT
        plt.scatter(s_pos[0], s_pos[1], color='gray', marker='o', s=80, alpha=0.4, label=f"Start d({d_id})")
        plt.scatter(goal[0], goal[1], color='green', marker='*', s=200, label=f"Goal d({d_id})")

        if d_id in end_data:
            # DATA FROM OUTPUT (Final)
            d = end_data[d_id]
            actual_pos = d['pos']
            est_pos = d['est']
            
            # 1. Trajectory Arrow: Start(Input) -> Actual(Output)
            plt.arrow(s_pos[0], s_pos[1], actual_pos[0]-s_pos[0], actual_pos[1]-s_pos[1], 
                      head_width=0.15, head_length=0.15, fc='blue', ec='blue', alpha=0.6, length_includes_head=True)
            
            # 2. Actual Position (Blue Triangle)
            plt.scatter(actual_pos[0], actual_pos[1], color='blue', marker='>', s=100, label=f"Actual d({d_id})")
            
            # 3. Estimated Position (Orange Dot)
            plt.scatter(est_pos[0], est_pos[1], color='orange', marker='o', s=120, edgecolors='black', label=f"Estimate d({d_id})")
            
            # 4. Error Line: Actual <---> Estimate
            plt.plot([actual_pos[0], est_pos[0]], [actual_pos[1], est_pos[1]], color='red', linestyle=':', alpha=0.6, linewidth=2)

            # Label with stats
            label_text = f"ID: d({d_id})\nSpd: {d['speed']:.2f}\nBelief: {d['belief']*100:.1f}%"
            plt.text(est_pos[0] + 0.1, est_pos[1] + 0.1, label_text, fontsize=9, fontweight='bold', bbox=dict(facecolor='orange', alpha=0.2))

        else:
            # CRASHED (Present in input, missing in output)
            plt.scatter(s_pos[0], s_pos[1], color='red', marker='x', s=250, linewidth=4)
            plt.text(s_pos[0], s_pos[1] + 0.3, "CRASHED", color='red', fontweight='bold', ha='center')

    plt.title("Drone Tracking: Input (Start/Goal) vs Output (Actual/Estimate)")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.show()

# --- EXAMPLE DATA ---
# This matches your specific request: Goal and Start from Input, Actual/Est from Output.

initial_config = """

{ < d(1) : Drone | pos: v(10,10), estPos: v(0,0), goalPos: v(5,7), belief: 1, speed: 0, heading: stop, inbox: emptyMsg, none > , 0 }
"""

final_config = """

< d(1) : Drone | pos: v(14361/1000, 18581/1000),estPos: v(4361/1000, 5581/1000),goalPos: v(5, 7),belief: 7/10,speed: 23/100,heading: N,inbox:
    emptyMsg >
"""

visualize_flight(initial_config, final_config)