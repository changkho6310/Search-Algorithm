import turtle

SQUARE = 21
FONT_SIZE = 13
FONT = ('Consoles', FONT_SIZE)
GRID_COLOR = "white"
INPUT_CLUSTERS_COLOR = "red"
FENCE_COLOR = "grey"
EXPANDED_COLOR = "green"
FRONTIER_COLOR = "yellow"
PATH_COLOR = "blue"


class Node:
    def __init__(self, x, y, parent=None, goal=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.h = 0
        self.g = 0
        self.g_and_h = 0
        if self.parent is not None:
            self.g = self.parent.g + 1
        if goal is not None:
            self.h = self.calc_h_manhattan(goal=goal)
            self.g_and_h = self.h + self.g

    def is_goal(self, goal):
        return self.x == goal.x and self.y == goal.y

    def calc_h_manhattan(self, goal):
        return abs(goal.x - self.x) + abs(goal.y - self.y)


def draw_fence_two_node(n1, n2):
    lst_fence = []
    if n1.x < n2.x:
        # Top Right
        if n1.y < n2.y:
            x = n1.x
            y = n1.y
            lst_fence.append(Node(x, y))
            while x < n2.x and y < n2.y:
                x += 1
                y += 1
                lst_fence.append(Node(x, y))

            while x < n2.x:
                x += 1
                lst_fence.append(Node(x, y))

            while y < n2.y:
                y += 1
                lst_fence.append(Node(x, y))

        # Bottom Right
        else:
            x = n1.x
            y = n1.y
            lst_fence.append(Node(x, y))
            while x < n2.x and y > n2.y:
                x += 1
                y -= 1
                lst_fence.append(Node(x, y))

            while x < n2.x:
                x += 1
                lst_fence.append(Node(x, y))

            while y > n2.y:
                y -= 1
                lst_fence.append(Node(x, y))
            pass
    else:
        # Top Left
        if n1.y < n2.y:
            x = n1.x
            y = n1.y
            lst_fence.append(Node(x, y))
            while x > n2.x and y < n2.y:
                x -= 1
                y += 1
                lst_fence.append(Node(x, y))

            while x > n2.x:
                x -= 1
                lst_fence.append(Node(x, y))

            while y < n2.y:
                y += 1
                lst_fence.append(Node(x, y))
        # Bottom Left
        else:
            x = n1.x
            y = n1.y
            lst_fence.append(Node(x, y))
            while x > n2.x and y > n2.y:
                x -= 1
                y -= 1
                lst_fence.append(Node(x, y))

            while x > n2.x:
                x -= 1
                lst_fence.append(Node(x, y))

            while y > n2.y:
                y -= 1
                lst_fence.append(Node(x, y))
    return lst_fence


def draw_4_fence_borders(lst_fence, max_x, max_y):
    for i in range(0, max_y + 1):
        lst_fence.append(Node(0, i))
        lst_fence.append(Node(max_x, i))

    for i in range(0, max_x + 1):
        lst_fence.append(Node(i, 0))
        lst_fence.append(Node(i, max_y))
    return lst_fence


def draw_fence(lst_fence, one_cluster):
    if len(one_cluster) == 0:
        return lst_fence
    if len(one_cluster) == 1:
        lst_fence.append(one_cluster.pop(0))
    else:
        previous_node = one_cluster.pop(0)
        first_node = previous_node
        last_node = None

        while one_cluster:
            current_node = one_cluster.pop(0)
            for item in draw_fence_two_node(previous_node, current_node):
                lst_fence.append(item)
            previous_node = current_node
            last_node = current_node

        for item in draw_fence_two_node(last_node, first_node):
            lst_fence.append(item)
    return lst_fence


def remove_duplicate_fence(lst_fence):
    lst_temp = []
    if lst_fence:
        lst_temp.append(lst_fence.pop(0))

    for i in lst_fence:
        will_add = True
        for j in lst_temp:
            if j.x == i.x and j.y == i.y:
                will_add = False
                break
        if will_add:
            lst_temp.append(i)
    return lst_temp


def get_list_nodes_of_clusters(lst_clusters):
    list_nodes_of_clusters = []
    for cluster in lst_clusters:
        for node in cluster:
            list_nodes_of_clusters.append(Node(node.x, node.y))
    return list_nodes_of_clusters


def read_file():
    with open("input.txt") as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        new_lines.append(line.strip('\n'))

    line_1 = new_lines.pop(0).split()
    max_x = int(line_1.pop(0))
    max_y = int(line_1.pop(0))

    line_2 = new_lines.pop(0).split()
    start_node = Node(int(line_2.pop(0)), int(line_2.pop(0)))
    goal_node = Node(int(line_2.pop(0)), int(line_2.pop(0)))

    lst_input_clusters = []
    total_cluster = int(new_lines.pop(0))
    for i in range(total_cluster):
        line_i = new_lines.pop(0).split()
        one_cluster = []
        while line_i != []:
            node = Node(int(line_i.pop(0)), int(line_i.pop(0)))
            one_cluster.append(node)
        lst_input_clusters.append(one_cluster)

    return max_x, max_y, start_node, goal_node, lst_input_clusters


def draw_start_and_goal(start, goal):
    # Draw START
    turtle.setpos(start.x * SQUARE, start.y * SQUARE)
    turtle.pencolor("black")
    turtle.fillcolor(PATH_COLOR)
    turtle.stamp()

    turtle.setpos(start.x * SQUARE, start.y * SQUARE - 10)
    turtle.pencolor("white")
    turtle.write("S", align="center", font=FONT)

    #   Draw GOAL
    turtle.setpos(goal.x * SQUARE, goal.y * SQUARE)
    turtle.pencolor("black")
    turtle.fillcolor(PATH_COLOR)
    turtle.stamp()

    turtle.setpos(goal.x * SQUARE, goal.y * SQUARE - 10)
    turtle.pencolor("white")
    turtle.write("G", align="center", font=FONT)

    # Clear color of shape and move it to another pos to hint it from GRID TABLE
    turtle.fillcolor("white")
    turtle.setpos(-300, -300)
    pass


def draw_grid(max_x, max_y, start_node, goal_node, lst_input_clusters):
    turtle.shape("square")
    turtle.shapesize(1, 1, 1)
    turtle.fillcolor(GRID_COLOR)
    turtle.penup()

    # Draw Ox
    for i in range(max_x + 1):
        turtle.setpos(i * SQUARE, -40)
        turtle.write(str(i), align="center", font=FONT)

    # Draw Oy
    for i in range(max_y + 1):
        turtle.setpos(-30, i * SQUARE - 10)
        turtle.write(str(i), align="center", font=FONT)

    # Draw Grid Square
    for i in range(max_y + 1):
        turtle.setpos(0, i * SQUARE)
        for j in range(max_x + 1):
            if j == 0:
                turtle.stamp()
                continue
            turtle.forward(SQUARE)
            turtle.stamp()

    # Get List Fence
    lst_fence = []
    list_nodes_of_clusters = get_list_nodes_of_clusters(lst_input_clusters)
    for cluster in lst_input_clusters:
        lst_fence = draw_fence(lst_fence=lst_fence, one_cluster=cluster)

    lst_fence = draw_4_fence_borders(lst_fence=lst_fence, max_x=max_x, max_y=max_y)

    lst_fence = remove_duplicate_fence(lst_fence=lst_fence)

    # Draw list fence
    for node_fence in lst_fence:
        turtle.setpos(node_fence.x * SQUARE, node_fence.y * SQUARE)
        turtle.fillcolor(FENCE_COLOR)
        turtle.stamp()

    # Draw Input Fence Node (RED)
    for node in list_nodes_of_clusters:
        turtle.setpos(node.x * SQUARE, node.y * SQUARE)
        turtle.fillcolor(INPUT_CLUSTERS_COLOR)
        turtle.stamp()

    #   Draw START and GOAL
    draw_start_and_goal(start=start_node, goal=goal_node)
    return lst_fence


def change_color(node, color):
    turtle.setpos(node.x * SQUARE, node.y * SQUARE)
    turtle.pencolor("black")
    turtle.fillcolor(color)
    turtle.stamp()


def get_solution(goal):
    path = []
    path_cost = goal.g

    tmp_node = goal
    while tmp_node.parent is not None:
        path.append(tmp_node)
        tmp_node = tmp_node.parent

    # START
    path.append(tmp_node)
    return path, path_cost


def get_neighbor(node, goal=None):
    lst_neighbor = []
    if goal is not None:
        # TOP
        lst_neighbor.append(Node(node.x, node.y + 1, parent=node, goal=goal))
        # RIGHT
        lst_neighbor.append(Node(node.x + 1, node.y, parent=node, goal=goal))
        # BOTTOM
        lst_neighbor.append(Node(node.x, node.y - 1, parent=node, goal=goal))
        # LEFT
        lst_neighbor.append(Node(node.x - 1, node.y, parent=node, goal=goal))
    else:
        # TOP
        lst_neighbor.append(Node(node.x, node.y + 1, parent=node))
        # RIGHT
        lst_neighbor.append(Node(node.x + 1, node.y, parent=node))
        # BOTTOM
        lst_neighbor.append(Node(node.x, node.y - 1, parent=node))
        # LEFT
        lst_neighbor.append(Node(node.x - 1, node.y, parent=node))
    return lst_neighbor


def add_node_to_expanded(node, expanded):
    expanded.append(node)
    change_color(node, EXPANDED_COLOR)
    return expanded


def add_node_to_frontier(node, frontier=[]):
    frontier.append(node)
    change_color(node, FRONTIER_COLOR)
    return frontier


def can_add_node_to_frontier(node, frontier=[], expanded=[], lst_fence=[]):
    for expanded_node in expanded:
        if node.x == expanded_node.x and node.y == expanded_node.y:
            return False

    for frontier_node in frontier:
        if node.x == frontier_node.x and node.y == frontier_node.y:
            return False

    for fence_node in lst_fence:
        if node.x == fence_node.x and node.y == fence_node.y:
            return False

    return True


def draw_path(path):
    for node in path:
        change_color(node, PATH_COLOR)


def clear_expanded_frontier_color(expanded=[], frontier=[]):
    for node in expanded:
        change_color(node, GRID_COLOR)
    for node in frontier:
        change_color(node, GRID_COLOR)


def get_min_node_by_g(lst):
    if lst:
        min_g = lst[0].g

    index_min_node = 0
    for i, item in enumerate(lst):
        if min_g > item.g:
            min_g = item.g
            index_min_node = i

    min_node = lst.pop(index_min_node)
    return min_node, lst


def get_min_node_by_h(lst):
    if lst:
        min_h = lst[0].h

    index_min_node = 0
    for i, item in enumerate(lst):
        if min_h > item.h:
            min_h = item.h
            index_min_node = i

    min_node = lst.pop(index_min_node)
    return min_node, lst


def get_min_node_by_g_and_h(lst):
    if lst:
        min_g_and_h = lst[0].g_and_h

    index_min_node = 0
    for i, item in enumerate(lst):
        if min_g_and_h > item.g_and_h:
            min_g_and_h = item.g_and_h
            index_min_node = i

    min_node = lst.pop(index_min_node)
    return min_node, lst


def get_node_from_frontier_ucs(frontier):
    node, frontier = get_min_node_by_g(lst=frontier)
    return node, frontier


def get_node_from_frontier_gbfs(frontier):
    node, frontier = get_min_node_by_h(lst=frontier)
    return node, frontier


def get_node_from_frontier_a_star(frontier):
    node, frontier = get_min_node_by_g_and_h(lst=frontier)
    return node, frontier


def update_node_in_frontier_ucs(node, frontier=[]):
    for item in frontier:
        if item.x == node.x and item.y == node.y and item.g > node.g:
            item = node
            draw_g_of_node(node)
            break
    return frontier


def update_node_in_frontier_gbfs(node, frontier=[]):
    for item in frontier:
        if item.x == node.x and item.y == node.y and item.h > node.h:
            item = node
            draw_h_of_node(node)
            break
    return frontier


def update_node_in_frontier_a_star(node, frontier=[]):
    for item in frontier:
        if item.x == node.x and item.y == node.y and item.g_and_h > node.g_and_h:
            item = node
            draw_g_and_h_of_node(item)
            break
    return frontier


def draw_g_of_node(node):
    turtle.pencolor("black")
    turtle.setpos(node.x * SQUARE, node.y * SQUARE - 10)
    turtle.write(str(node.g), align="center", font=FONT)


def draw_h_of_node(node):
    turtle.pencolor("black")
    turtle.setpos(node.x * SQUARE, node.y * SQUARE - 10)
    turtle.write(str(node.h), align="center", font=FONT)


def draw_g_and_h_of_node(node):
    turtle.pencolor("black")
    turtle.setpos(node.x * SQUARE, node.y * SQUARE - 10)
    turtle.write(str(node.g_and_h), align="center", font=FONT)


# Enqueue : Check before adding to frontier
def breadth_first_search(start, goal, lst_fence):
    found_goal = False
    frontier = []
    expanded = []

    if start.is_goal(goal=goal):
        expanded = add_node_to_expanded(goal, expanded)
        found_goal = True
    else:
        frontier = add_node_to_frontier(start, frontier)
        while frontier and found_goal is False:
            # FIFO
            node_to_expand = frontier.pop(0)
            lst_neighbor = get_neighbor(node_to_expand)
            expanded = add_node_to_expanded(node_to_expand, expanded)
            for item in lst_neighbor:
                # Check if node is goal
                # Enqueue : Check before adding to frontier
                if item.is_goal(goal=goal):
                    expanded = add_node_to_expanded(item, expanded)
                    goal.parent = item.parent
                    found_goal = True
                    break

                # Check a node can be added to frontier:
                # 1. Not in explored set
                # 2. Not in frontier
                # 3. Not in fence
                if can_add_node_to_frontier(node=item,
                                            frontier=frontier,
                                            expanded=expanded,
                                            lst_fence=lst_fence):
                    frontier = add_node_to_frontier(item, frontier)

        clear_expanded_frontier_color(expanded=expanded,
                                      frontier=frontier)

    # If failure
    if found_goal is False:
        draw_start_and_goal(start=start, goal=goal)
        return [], 0
    # If success
    else:
        path, path_cost = get_solution(goal)
        draw_path(path)
        draw_start_and_goal(start=start, goal=goal)
        return path, path_cost


# Dequeue : Check goal after getting node out of frontier
def uniform_cost_search(start, goal, lst_fence):
    found_goal = False
    frontier = []
    expanded = []

    frontier = add_node_to_frontier(start, frontier)
    while frontier and found_goal is False:
        node_to_expand, frontier = get_node_from_frontier_ucs(frontier=frontier)

        # Dequeue : Check if node is goal after getting node out of frontier
        if node_to_expand.is_goal(goal):
            goal.parent = node_to_expand.parent
            expanded = add_node_to_expanded(node_to_expand, expanded)
            found_goal = True
            break

        lst_neighbor = get_neighbor(node_to_expand)
        expanded = add_node_to_expanded(node_to_expand, expanded)
        draw_g_of_node(node=node_to_expand)
        for item in lst_neighbor:
            # Check a node can be added to frontier:
            # 1. Node is not in explored set or frontier
            # 2. Node is not in fence
            if can_add_node_to_frontier(node=item,
                                        frontier=frontier,
                                        expanded=expanded,
                                        lst_fence=lst_fence):
                frontier = add_node_to_frontier(node=item, frontier=frontier)
                draw_g_of_node(node=item)
            # Check a node can be updated in frontier:
            # 1. Node is not in explored set
            # 2. Node is not in fence
            # 3. Node is in frontier with lower path cost (g)
            elif can_add_node_to_frontier(node=item,
                                          lst_fence=lst_fence,
                                          expanded=expanded):
                frontier = update_node_in_frontier_ucs(item, frontier)

    clear_expanded_frontier_color(expanded=expanded,
                                  frontier=frontier)

    # If failure
    if found_goal is False:
        draw_start_and_goal(start=start, goal=goal)
        return [], 0
    # If success
    else:
        path, path_cost = get_solution(goal)
        draw_path(path)
        draw_start_and_goal(start=start, goal=goal)
        return path, path_cost


# Dequeue : Check goal after getting node out of frontier
def greedy_best_first_search(start, goal, lst_fence):
    found_goal = False
    frontier = []
    expanded = []

    start = Node(x=start.x, y=start.y, goal=goal)
    frontier = add_node_to_frontier(start, frontier)
    draw_h_of_node(node=start)
    while frontier and found_goal is False:
        node_to_expand, frontier = get_node_from_frontier_gbfs(frontier=frontier)

        # Dequeue : Check if node is goal after getting node out of frontier
        if node_to_expand.is_goal(goal):
            goal.parent = node_to_expand.parent
            expanded = add_node_to_expanded(node_to_expand, expanded)
            found_goal = True
            break

        lst_neighbor = get_neighbor(node=node_to_expand,
                                    goal=goal)
        expanded = add_node_to_expanded(node_to_expand, expanded)
        draw_h_of_node(node=node_to_expand)
        for item in lst_neighbor:
            # Check a node can be added to frontier:
            # 1. Node is not in explored set or frontier
            # 2. Node is not in fence
            if can_add_node_to_frontier(node=item,
                                        frontier=frontier,
                                        expanded=expanded,
                                        lst_fence=lst_fence):
                frontier = add_node_to_frontier(node=item, frontier=frontier)
                draw_h_of_node(node=item)
            # Check a node can be updated in frontier:
            # 1. Node is not in explored set
            # 2. Node is not in fence
            # 3. Node is in frontier with lower h
            elif can_add_node_to_frontier(node=item,
                                          lst_fence=lst_fence,
                                          expanded=expanded):
                frontier = update_node_in_frontier_gbfs(item, frontier)

    clear_expanded_frontier_color(expanded=expanded,
                                  frontier=frontier)

    # If failure
    if found_goal is False:
        draw_start_and_goal(start=start, goal=goal)
        return [], 0
    # If success
    else:
        path, path_cost = get_solution(goal)
        draw_path(path)
        draw_start_and_goal(start=start, goal=goal)
        return path, path_cost


# Dequeue : Check goal after getting node out of frontier
def a_star_graph_search(start, goal, lst_fence):
    found_goal = False
    frontier = []
    expanded = []

    start = Node(x=start.x, y=start.y, goal=goal)
    frontier = add_node_to_frontier(start, frontier)
    draw_g_and_h_of_node(node=start)
    while frontier and found_goal is False:
        node_to_expand, frontier = get_node_from_frontier_a_star(frontier=frontier)

        # Dequeue : Check if node is goal after getting node out of frontier
        if node_to_expand.is_goal(goal):
            goal.parent = node_to_expand.parent
            expanded = add_node_to_expanded(node_to_expand, expanded)
            found_goal = True
            break

        lst_neighbor = get_neighbor(node=node_to_expand,
                                    goal=goal)
        expanded = add_node_to_expanded(node_to_expand, expanded)
        draw_g_and_h_of_node(node=node_to_expand)
        for item in lst_neighbor:
            # Check a node can be added to frontier:
            # 1. Node is not in explored set or frontier
            # 2. Node is not in fence
            if can_add_node_to_frontier(node=item,
                                        frontier=frontier,
                                        expanded=expanded,
                                        lst_fence=lst_fence):
                frontier = add_node_to_frontier(node=item, frontier=frontier)
                draw_g_and_h_of_node(node=item)
            # Check a node can be updated in frontier:
            # 1. Node is not in explored set
            # 2. Node is not in fence
            # 3. Node is in frontier with lower (g + h)
            elif can_add_node_to_frontier(node=item,
                                          lst_fence=lst_fence,
                                          expanded=expanded):
                frontier = update_node_in_frontier_a_star(item, frontier)

    clear_expanded_frontier_color(expanded=expanded,
                                  frontier=frontier)

    # If failure
    if found_goal is False:
        draw_start_and_goal(start=start, goal=goal)
        return [], 0
    # If success
    else:
        path, path_cost = get_solution(goal)
        draw_path(path)
        draw_start_and_goal(start=start, goal=goal)
        return path, path_cost


def main():
    max_x, max_y, start_node, goal_node, lst_input_clusters = read_file()
    screen = turtle.Screen()
    turtle.setup()
    turtle.screensize(2000, 2000, "white")
    turtle.speed(0)

    lst_fence = draw_grid(max_x=max_x,
                          max_y=max_y,
                          start_node=start_node,
                          goal_node=goal_node,
                          lst_input_clusters=lst_input_clusters)

    path, path_cost = a_star_graph_search(start=start_node,
                                          goal=goal_node,
                                          lst_fence=lst_fence)
    screen.mainloop()


main()
