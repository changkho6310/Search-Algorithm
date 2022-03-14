import turtle

SQUARE = 21
FONT_SIZE = 13
FONT = ('Consoles', FONT_SIZE)


class Node:
    def __init__(self, x, y, parent=None, h=0):
        self.x = x
        self.y = y
        self.parent = parent
        self.h = h

    def is_goal(self, goal):
        return self.x == goal.x and self.y == goal.y


# done
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


# done
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


# done
def draw_4_fence_borders(lst_fence, max_x, max_y):
    for i in range(0, max_y + 1):
        lst_fence.append(Node(0, i))
        lst_fence.append(Node(max_x, i))

    for i in range(0, max_x + 1):
        lst_fence.append(Node(i, 0))
        lst_fence.append(Node(i, max_y))
    return lst_fence


# done
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


# done
def get_list_nodes_of_clusters(lst_clusters):
    list_nodes_of_clusters = []
    for cluster in lst_clusters:
        for node in cluster:
            list_nodes_of_clusters.append(Node(node.x, node.y))
    return list_nodes_of_clusters


# done
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


# done
def draw_grid(max_x, max_y, start_node, goal_node, lst_input_clusters):
    turtle.shape("square")
    turtle.shapesize(1, 1, 1)
    turtle.fillcolor("white")
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
        turtle.fillcolor("grey")
        turtle.stamp()

    # Draw Input Fence Node (RED)
    for node in list_nodes_of_clusters:
        turtle.setpos(node.x * SQUARE, node.y * SQUARE)
        turtle.fillcolor("orange")
        turtle.stamp()

    #   Draw START
    turtle.setpos(start_node.x * SQUARE, start_node.y * SQUARE)
    turtle.fillcolor("blue")
    turtle.stamp()

    turtle.setpos(start_node.x * SQUARE, start_node.y * SQUARE - 10)
    turtle.pencolor("white")
    turtle.write("S", align="center", font=FONT)

    #   Draw GOAL
    turtle.setpos(goal_node.x * SQUARE, goal_node.y * SQUARE)
    turtle.pencolor("black")
    turtle.fillcolor("blue")
    turtle.stamp()

    turtle.setpos(goal_node.x * SQUARE, goal_node.y * SQUARE - 10)
    turtle.pencolor("white")
    turtle.write("G", align="center", font=FONT)

    # Clear color of shape and move it to another pos to hint it from GRID TABLE
    turtle.fillcolor("white")
    turtle.setpos(-300, -300)


max_x, max_y, start_node, goal_node, lst_input_clusters = read_file()

screen = turtle.Screen()
turtle.setup()
turtle.screensize(2000, 2000, "white")
turtle.speed(0)

draw_grid(max_x=max_x,
          max_y=max_y,
          start_node=start_node,
          goal_node=goal_node,
          lst_input_clusters=lst_input_clusters)

screen.mainloop()
