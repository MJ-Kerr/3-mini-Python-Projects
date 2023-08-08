import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "O", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

# this is to print the maze --- maze is th above maze, stdscr is the standard screen, and path is to draw them a different color in the maze, WE DONT KNOW WHAT IT IS YET SO IT WILL BE EMPTY ARRAY


def print_maze(maze, stdscr, path=[]):
    # grabbing the color pairs to color the maze
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    # looping through the whole maze
    # i = index of the row = which row we are on enumerate = will not only give you the index but also the value of that index.
    for i, row in enumerate(maze):
        # j = index of column we are on value = the value of that column on that row enumerate gives you the index and value of that square.
        for j, value in enumerate(row):
            # this will print the path in a different color
            if (i, j) in path:
                # this will make it "x" in red
                stdscr.addstr(i, j*2, "X", RED)
            else:
                # this is actually adding the maze to the terminal here
                stdscr.addstr(i, j*2, value, BLUE)

# this function will tell us where to start


def find_start(maze, start):
    # this will go through the rows and the columns i= row j = column
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


# this function will find the fastest path.
def find_path(maze, stdscr):
    start = "O"
    end = "X"
    # this line tells it to call the function to start.
    start_pos = find_start(maze, start)
    # this initializes the queue
    q = queue.Queue()

    # I wanna keep track of the node that i want to process next and the path i took to get there. This is what I will return for the shortest path.
    # params are ( where we are, and where i have been)
    q.put((start_pos, [start_pos]))

    # this sets the history or path of where you have been.
    visited = set()
    # while we still have elements in the queue is empty then we get the next one in the path.
    while not q.empty():
        # this is where you grab both of the pieces of information from q.put
        current_pos, path = q.get()
        # row and col are equal to current pos
        row, col = current_pos  # then we are gonna grab the neighbors of the current_pos

        stdscr.clear()  # clears the terminal so we can print what we want there
        # stdscr.addstr(5, 5, "HELLO WORLDS!!!!") # very simple hello world statement
        # runs the print maze functions while passing the maze and standard screen as params and the path so it prints it every time it goes through the path.
        print_maze(maze, stdscr, path)
        stdscr.refresh()  # restarts the terminal so that we can see what we have written

        if maze[row][col] == end:  # here we check if the current_pos is equal to the end if it is then
            # this will be the shortest path. or one of the shortest.
            return path
        # this is where we go through the neighbors.
        neighbors = find_neighbors(maze, row, col)
        # this take one of all of em
        for neighbor in neighbors:
            # this checks if the neighbor has been visited before
            if neighbor in visited:
                # if it has then we can continue we dont have to check it.
                continue
            # this will assign the row(r) and col(c) to neighbor
            r, c = neighbor
            # this will check for a # sign
            if maze[r][c] == "#":
                continue  # here we dont want to process so we just continue.
            # this will add a new path for the updated path.
            new_path = path + [neighbor]
            # this will add the new neighbor to the queue
            q.put((neighbor, new_path))
            # this will add the neighbor to the visited array so we dont check it twice
            visited.add(neighbor)


# this will define all the neighbors
def find_neighbors(maze, row, col):
    neighbors = []
    # now we check left right up and down
    if row > 0:  # UP
        neighbors.append((row-1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))
    return neighbors  # this return the neighbors array.

# STDSCR = STanDard SCReen


def main(stdscr):
    # this changes the main printed in the console blue with a black background
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # this changes the secondary printed in the console red with a black background
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()  # clears the terminal so we can print what we want there
    # stdscr.addstr(5, 5, "HELLO WORLDS!!!!") # very simple hello world statement
    # runs the print maze functions while passing the maze and standard screen as params
    print_maze(maze, stdscr)
    stdscr.refresh()  # restarts the terminal so that we can see what we have written
    # call the function to show all of this cool stuff
    find_path(maze, stdscr)
    stdscr.getch()


# how the algo works
# find shortest path from starting node to ending node in our example we are using O and X
# gonna reference nodes by their position in the graph so the first starting point(O) in this simple graph would be 0,3
# so we start at a certain point then expand outward till we find the end point.
# we check from neighbor to neighbor  so from the  start we go up and to the right since the left and down are blocked. we continue checking for the end till we find it then showing us the shortest line to the  end.
#      0    1    2    3    4
#
#   0                 X
#
#   1       #    #    #
#
#   2       #
#
#   3  O              #
#
# we will be setting it up as a queue so first in first out. Like an actual line.
# start with the Start so (3,0)
# then process to see the neighbors then process those neighbors.
# moving it into a set so we know that we have looked their already.
# then  repeat all of the steps and check the set to see if the neighbor has been processed yet.
wrapper(main)
