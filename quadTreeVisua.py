import matplotlib.pyplot as plt
import re

def parse_maude_num(s):
    if '/' in s:
        n, d = s.split('/')
        return float(n) / float(d)
    return float(s)

def visualize_splits(maude_output):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 1. Find the Root Box to set the boundaries
    root_match = re.search(r"box\(\s*([\d/]+)\s*,\s*([\d/]+)\s*,\s*([\d/]+)\s*,\s*([\d/]+)\s*\)", maude_output)
    if not root_match:
        print("No box found in output.")
        return
    
    rx1, ry1, rx2, ry2 = map(parse_maude_num, root_match.groups())
    
    # Draw the main boundary
    ax.plot([rx1, rx2, rx2, rx1, rx1], [ry1, ry1, ry2, ry2, ry1], 'k-', lw=2)

    # 2. Find every NODE and draw the split lines through its center
    # We look for: node(box(x1, y1, x2, y2), ...
    node_pattern = r"node\(box\(\s*([\d/]+)\s*,\s*([\d/]+)\s*,\s*([\d/]+)\s*,\s*([\d/]+)\s*\)"
    nodes = re.findall(node_pattern, maude_output)
    
    for x1, y1, x2, y2 in nodes:
        x1, y1, x2, y2 = map(parse_maude_num, [x1, y1, x2, y2])
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Draw the Vertical Split
        ax.plot([mid_x, mid_x], [y1, y2], color='blue', linestyle='--', lw=1, alpha=0.6)
        # Draw the Horizontal Split
        ax.plot([x1, x2], [mid_y, mid_y], color='blue', linestyle='--', lw=1, alpha=0.6)

    # 3. Plot the Drones
    drone_pattern = r"<\s*d\((\d+)\)\s*:\s*Drone\s*\|\s*pos:\s*v\(\s*([\d/]+)\s*,\s*([\d/]+)\s*\)"
    drones = re.findall(drone_pattern, maude_output)

    for d_id, dx, dy in drones:
        x, y = parse_maude_num(dx), parse_maude_num(dy)
        ax.plot(x, y, 'ro', markersize=6)
        ax.text(x + 0.1, y + 0.1, f"D{d_id}", fontsize=10, color='red', weight='bold')

    ax.set_xlim(rx1 - 0.5, rx2 + 0.5)
    ax.set_ylim(ry1 - 0.5, ry2 + 0.5)
    ax.set_aspect('equal')
    plt.title("Quadtree Spatial Partitioning (Center Splits)")
    plt.grid(False)
    plt.show()

# --- PASTE YOUR MAUDE RESULT HERE ---
result_string = """
node(box(0, 0, 10, 10), empty, leaf(< d(3) : Drone | pos: v(9, 9),estPos: v(0, 0),goalPos: v(0, 0),belief: 0,speed: 0,heading: N,inbox: emptyMsg >), node(box(0, 0, 5, 5), empty, empty, node(box(0, 0, 5/2, 5/2), leaf(< d(2) : Drone | pos: v(1, 2),estPos: v(0, 0), goalPos: v(0, 0),belief: 0,speed: 0,heading: N,inbox: emptyMsg >), empty, leaf(< d(1) : Drone | pos: v(1, 1),estPos: v(0, 0),goalPos: v(0, 0),belief: 0,speed: 0,heading: N,inbox: emptyMsg >), empty), empty), leaf(< d(4) : Drone | pos: v(9, 1),estPos: v(0, 0),goalPos: v(0, 0),belief: 0,speed: 0,heading: N,inbox: emptyMsg >))
"""

visualize_splits(result_string)