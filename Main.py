from tkinter import *
from agent import Agent
from world import World
from grid_label import Grid_Label
import time

def solve_wumpus_world(master, world_file):
    world = World()
    world.generate_world(world_file)
    # print(DataFrame(world.world))
    label_grid = [[Grid_Label(master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)]
    agent = Agent(world, label_grid)

    # Agent Solving
    while agent.exited == False:
        agent.explore()
        if agent.found_gold == True:
            agent.leave_cave()
        break
    # print("You have exited with the gold!")
    agent.repaint_world()
    agent.world_knowledge[agent.world.agent_row][agent.world.agent_col].remove('A')
    time.sleep(1.5)
    agent.repaint_world()


master = Tk()
master.title("Wumpus World")

world = World()
world.generate_world("world_1.txt")
label_grid = [[Grid_Label(master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)]
# agent = Agent(world, label_grid)

# start = Button(master, text="Start", command= lambda: solve_wumpus_world(master, "world_1.txt"))
world_1 = Button(master, text="World 1",  command= lambda: solve_wumpus_world(master, "world_1.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world_2 = Button(master, text="World 2",  command= lambda: solve_wumpus_world(master, "world_2.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world_3 = Button(master, text="World 3",  command= lambda: solve_wumpus_world(master, "world_3.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")
world_4 = Button(master, text="World 4",  command= lambda: solve_wumpus_world(master, "world_4.txt"), width=8, font = "Helvetica 14 bold", bg = "gray80", fg = "gray40", borderwidth=0, activeforeground="white", activebackground="gray40")

# start.grid(row = 0, column = len(label_grid[0]), sticky = W, pady = 1)
world_1.grid(row = 0, column = len(label_grid[0]))
world_2.grid(row = 1, column = len(label_grid[0]))
world_3.grid(row = 2, column = len(label_grid[0]))
world_4.grid(row = 3, column = len(label_grid[0]))


mainloop()