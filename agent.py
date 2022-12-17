"""
Legend:
. = visited tile
A = agent
G = gold
W = wumpus
S = stench
w = potential wumpus
nw = no wumpus
P = pit
B = breeze
p = potential pit
np = no pit
"""

# from pandas import * # pip install pandas
import time

class Agent:
    def __init__(self, world, label_grid):
        self.world = world
        self.world_knowledge = [[[] for i in range(self.world.num_cols)] for j in range(self.world.num_rows)]
        self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A')
        self.num_stenches = 0
        self.path_out_of_cave = [[self.world.agent_row, self.world.agent_col]]
        self.mark_tile_visited()
        self.world.cave_entrance_row = self.world.agent_row
        self.world.cave_entrance_col = self.world.agent_col
        self.found_gold = False # self.exit_cave(found_gold)
        self.took_gold = False
        self.exited = False
        self.label_grid = label_grid

        self.repaint_world()
        # print(DataFrame(self.world_knowledge))
        # print("Agent: [" + str(self.world.agent_row) + ", " + str(self.world.agent_col) + "]")


    def repaint_world(self):
        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                updated_text = []
                if 'A' in self.world_knowledge[i][j]:
                    updated_text.append('A')
                if 'w' in self.world_knowledge[i][j]:
                    updated_text.append('W')
                if 'p' in self.world_knowledge[i][j]:
                    updated_text.append('P')
                if 'B' in self.world_knowledge[i][j]:
                    updated_text.append('B')
                if 'S' in self.world_knowledge[i][j]:
                    updated_text.append('S')
                if 'G' in self.world_knowledge[i][j]:
                    updated_text.append('G')

                updated_str=""

                self.label_grid[i][j].change_text(updated_str.join(updated_text))
                if '.' in self.world_knowledge[i][j]:
                    self.label_grid[i][j].label.config(bg="gray40")
                self.label_grid[i][j].label.update()
        # print("repainted")

    def go_back_one_tile(self):
        # print(self.path_out_of_cave)
        # print(self.path_out_of_cave[-1][0])

        if self.world.agent_row-1 == self.path_out_of_cave[-1][0]:
            self.move('u')
        if self.world.agent_row+1 == self.path_out_of_cave[-1][0]:
            self.move('d')
        if self.world.agent_col+1 ==  self.path_out_of_cave[-1][1]:
            self.move('r')
        if self.world.agent_col-1 ==  self.path_out_of_cave[-1][1]:
            self.move('l')


        del self.path_out_of_cave[-1]



    def leave_cave(self):
        for tile in reversed(self.path_out_of_cave):
            # print("Leaving from: " + str(self.path_out_of_cave))
            if self.world.agent_row-1 == tile[0]:
                self.move('u')
            if self.world.agent_row+1 == tile[0]:
                self.move('d')
            if self.world.agent_col+1 == tile[1]:
                self.move('r')
            if self.world.agent_col-1 == tile[1]:
                self.move('l')

            if self.world.cave_entrance_row == self.world.agent_row:
                if self.world.cave_entrance_col == self.world.agent_col:
                    if self.found_gold == True:
                        self.exited = True
                        break


    def explore(self):
        last_move = ''
        already_moved = False
        while self.found_gold == False:

            if self.found_gold == True:
                break

            try:
                if  '.' not in self.world_knowledge[self.world.agent_row-1][self.world.agent_col] and self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('u'):
                            already_moved = True

                    # print(self.path_out_of_cave)
            except IndexError:
                pass

            try:
                if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col+1] and self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                    if already_moved == False:
                        if self.move('r'):
                            already_moved = True
                    # print(self.path_out_of_cave)
            except IndexError:
                pass

            try:
                if '.' not in self.world_knowledge[self.world.agent_row+1][self.world.agent_col] and self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('d'):
                            already_moved = True
                    # print(self.path_out_of_cave)
            except IndexError:
                pass

            try:
                if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col-1] and self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                    if already_moved == False:
                        if self.move('l'):
                            already_moved = True
                    # print(self.path_out_of_cave)
            except IndexError:
                pass

            # print(already_moved)

            if already_moved == False:
                self.go_back_one_tile()


            already_moved = False


            """
            if last_move != 'u' and self.move('u'):
                if self.found_gold == True:
                    break
                if self.move('u'):
                    pass
                elif self.move('r'):
                    pass
                elif self.move('l'):
                    pass
                elif self.move('d'):
                    pass
                last_move = 'u'
            """


    def move(self, direction):

        self.repaint_world()

        if self.found_gold == True and self.took_gold == False:
            self.took_gold == True
            if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('G')

        successful_move = False
        if direction == 'u':
            if self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                successful_move = self.move_up()
        if direction == 'r':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                successful_move = self.move_right()
        if direction == 'd':
            if self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                successful_move = self.move_down()
        if direction == 'l':
            if self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                successful_move = self.move_left()

        if successful_move:
            self.add_indicators_to_knowledge()
            self.mark_tile_visited()
            self.predict_wumpus()
            self.predict_pits()
            self.clean_predictions()
            self.confirm_wumpus_knowledge()

            # print(DataFrame(self.world_knowledge))
            # print("Agent: [" + str(self.world.agent_row) + ", " + str(self.world.agent_col) + "]")
            # print("Path out:" + str(self.path_out_of_cave))
            if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                # print("You found the gold! Time to leave!")
                self.found_gold = True

            if self.found_gold == False:
                self.path_out_of_cave.append([self.world.agent_row, self.world.agent_col])

        # print("Successful move: " + str(successful_move))

            time.sleep(1.5)

        return successful_move


    def add_indicators_to_knowledge(self):
        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'B' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('B')
        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'S' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('S')
        if 'G' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'G' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('G')
        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'P' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('P')
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'W' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('W')


    def predict_pits(self):
        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'p' not in self.world_knowledge[self.world.agent_row-1][self.world.agent_col]:
                            self.world_knowledge[self.world.agent_row-1][self.world.agent_col].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.num_cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'p' not in self.world_knowledge[self.world.agent_row][self.world.agent_col+1]:
                            self.world_knowledge[self.world.agent_row][self.world.agent_col+1].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.num_rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'p' not in self.world_knowledge[self.world.agent_row+1][self.world.agent_col]:
                            self.world_knowledge[self.world.agent_row+1][self.world.agent_col].append('p')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'p' not in self.world_knowledge[self.world.agent_row][self.world.agent_col-1]:
                            self.world_knowledge[self.world.agent_row][self.world.agent_col-1].append('p')
        except IndexError:
            pass


    def predict_wumpus(self):
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'w' not in self.world_knowledge[self.world.agent_row-1][self.world.agent_col]:
                            self.world_knowledge[self.world.agent_row-1][self.world.agent_col].append('w')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.num_cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'w' not in self.world_knowledge[self.world.agent_row][self.world.agent_col+1]:
                            self.world_knowledge[self.world.agent_row][self.world.agent_col+1].append('w')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.num_rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'w' not in self.world_knowledge[self.world.agent_row+1][self.world.agent_col]:
                            self.world_knowledge[self.world.agent_row+1][self.world.agent_col].append('w')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'w' not in self.world_knowledge[self.world.agent_row][self.world.agent_col-1]:
                            self.world_knowledge[self.world.agent_row][self.world.agent_col-1].append('w')
        except IndexError:
            pass


    def clean_predictions(self):
        self.num_stenches = 0

        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                if 'S' in self.world_knowledge[i][j]:
                    self.num_stenches += 1
                if 'w' in self.world_knowledge[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.world_knowledge[i-1][j]:
                                if 'S' not in self.world_knowledge[i-1][j]:
                                    self.world_knowledge[i][j].remove('w')
                                    self.world_knowledge[i][j].append('nw')
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.num_cols:
                            if '.' in self.world_knowledge[i][j+1]:
                                if 'S' not in self.world_knowledge[i][j+1]:
                                    self.world_knowledge[i][j].remove('w')
                                    self.world_knowledge[i][j].append('nw')
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.num_rows:
                            if '.' in self.world_knowledge[i+1][j]:
                                if 'S' not in self.world_knowledge[i+1][j]:
                                    self.world_knowledge[i][j].remove('w')
                                    self.world_knowledge[i][j].append('nw')
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.world_knowledge[i][j-1]:
                                if 'S' not in self.world_knowledge[i][j-1]:
                                    self.world_knowledge[i][j].remove('w')
                                    self.world_knowledge[i][j].append('nw')
                    except IndexError:
                        pass

                if 'p' in self.world_knowledge[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.world_knowledge[i-1][j]:
                                if 'B' not in self.world_knowledge[i-1][j]:
                                    self.world_knowledge[i][j].remove('p')
                                    self.world_knowledge[i][j].append('np')
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.num_cols:
                            if '.' in self.world_knowledge[i][j+1]:
                                if 'B' not in self.world_knowledge[i][j+1]:
                                    self.world_knowledge[i][j].remove('p')
                                    self.world_knowledge[i][j].append('np')
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.num_rows:
                            if '.' in self.world_knowledge[i+1][j]:
                                if 'B' not in self.world_knowledge[i+1][j]:
                                    self.world_knowledge[i][j].remove('p')
                                    self.world_knowledge[i][j].append('np')
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.world_knowledge[i][j-1]:
                                if 'B' not in self.world_knowledge[i][j-1]:
                                    self.world_knowledge[i][j].remove('p')
                                    self.world_knowledge[i][j].append('np')
                    except IndexError:
                        pass


    def confirm_wumpus_knowledge(self):
        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                if 'w' in self.world_knowledge[i][j]:
                    stenches_around = 0
                    try:
                        if i-1 >= 0:
                            if 'S' in self.world_knowledge[i-1][j]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.num_cols:
                            if 'S' in self.world_knowledge[i][j+1]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.num_rows:
                            if 'S' in self.world_knowledge[i+1][j]:
                                stenches_around += 1
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if 'S' in self.world_knowledge[i][j-1]:
                                stenches_around += 1
                    except IndexError:
                        pass

                    if stenches_around < self.num_stenches:
                        self.world_knowledge[i][j].remove('w')
                        self.world_knowledge[i][j].append('nw')


    def move_up(self):
        try:
            if self.world.agent_row-1 >= 0:
                self.remove_agent()
                self.world.agent_row -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_right(self):
        try:
            if self.world.agent_col+1 < self.world.num_cols:
                self.remove_agent()
                self.world.agent_col += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_down(self):
        try:
            if self.world.agent_row+1 < self.world.num_rows:
                self.remove_agent()
                self.world.agent_row += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_left(self):
        try:
            if self.world.agent_col-1 >= 0:
                self.remove_agent()
                self.world.agent_col -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def remove_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].remove('A')
        self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('A')


    def add_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].append('A')
        self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A')


    def mark_tile_visited(self):
        if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world.world[self.world.agent_row][self.world.agent_col].append('.')
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('.')


    def is_dead(self):
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have been slain by the Wumpus!")
            return True
        elif 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have fallen in a pit!")
            return True
        else:
            return False


    def is_safe_move(self, row, col):
        try:
            if 'w' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'p' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'W' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'P' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass

        return True