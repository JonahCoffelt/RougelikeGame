import numpy as  np

class Node():
    def __init__(self, x, y, walkable, g=0, h=0, parent=None):
        self.x = x
        self.y = y

        self.walkable = walkable

        self.g = g
        self.h = h
        self.f = g + h

        self.parent = parent

def make_node_map(map, grid_size, x_pos, y_pos):
    node_map = np.empty(shape=(grid_size + 1) ** 2, dtype=Node)
    for y in range(grid_size + 1):
        for x in range(grid_size + 1):
            if (x + x_pos - grid_size//2) >= 0 and (x + x_pos - grid_size//2) < 31 and (y + y_pos - grid_size//2) >= 0 and (y + y_pos - grid_size//2) < 31:
                walkable = not bool(map[int(y + y_pos - grid_size//2)][int(x + x_pos - grid_size//2)] == 1)
                node_map[int(x + y * (grid_size + 1))] = Node(x, y, walkable)
            else:
                node_map[int(x + y * (grid_size + 1))] = Node(x, y, True)

    return node_map

def pathfind(node_map, start_pos, end_pos):
    open_set = np.array([])
    current_node = node_map[int(start_pos[0] + start_pos[1] * np.sqrt(len(node_map)))]
    closed_set = np.array([current_node])

    while current_node.x != end_pos[0] or current_node.y != end_pos[1]:
        for y in range(-1, 2):
            for x in range(-1, 2):
                if (x or y) and current_node.x + x >= 0 and current_node.x + x < np.sqrt(len(node_map)) and current_node.y + y >= 0 and current_node.y + y < np.sqrt(len(node_map)):
                    node = node_map[int(current_node.x + x + (current_node.y + y) * np.sqrt(len(node_map)))]
                    if node.walkable and (node_map[int(current_node.x + (current_node.y + y) * np.sqrt(len(node_map)))].walkable or node_map[int(current_node.x + x + (current_node.y) * np.sqrt(len(node_map)))].walkable):
                        if not (node in closed_set) and not (node in open_set):
                            node.g = np.sqrt((node.y - start_pos[1])**2 + (node.x - start_pos[0])**2)
                            node.h = np.sqrt((node.y - end_pos[1])**2 + (node.x - end_pos[0])**2)
                            node.f = node.g + node.h
                            node.parent = current_node
                            open_set = np.append(open_set, node)
                        if node in open_set and current_node.g < node.parent.g:
                            node.parent = current_node

        if len(open_set):
            f_vals = np.array([node.f for node in open_set])
            i_val = np.argmin(f_vals)

            closed_set = np.append(closed_set, open_set[i_val])
            open_set = np.delete(open_set, i_val)
            current_node = closed_set[-1]
        else:
            return []

    path = []

    while current_node.parent:
        path.append(current_node.parent)
        current_node = current_node.parent
    
    return path



