from file_parser import File_Parser
# from pandas import *

class World:
    def __init__(self):
        self.world = [[]]
        self.num_rows = 0
        self.num_cols = 0

        self.agent_row = 0
        self.agent_col = 0
        self.cave_entrance_row = 0
        self.cave_entrance_col = 0


    def generate_world(self, file_name):

        file_parser = File_Parser(file_name)
        """
        print(file_parser.row_col)
        print(file_parser.agent)
        print(file_parser.wumpus)
        print(file_parser.gold)
        print(file_parser.pits)
        """
        self.num_rows = int(file_parser.row_col[0])
        self.num_cols = int(file_parser.row_col[1])

        self.world = [[[] for i in range(self.num_cols)] for j in range(self.num_rows)]

        self.agent_row = int(file_parser.agent[1])
        self.agent_col = int(file_parser.agent[2])
        self.world[self.agent_row][self.agent_col].append('A')


        self.world[int(file_parser.wumpus[1])][int(file_parser.wumpus[2])].append(file_parser.wumpus[0])
        self.world[int(file_parser.gold[1])][int(file_parser.gold[2])].append(file_parser.gold[0])
        for pit in file_parser.pits:
            self.world[int(pit[1])][int(pit[2])].append(pit[0])

        # print(DataFrame(self.world))


        self.populate_indicators()

    def populate_indicators(self):

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                for k in range(len(self.world[i][j])):
                    """
                    if self.world[i][j][k] == 'A':
                        print("Agent at [" + str(i) + ", " + str(j) + "]")
                    """

                    if self.world[i][j][k] == 'W':
                        # print("Wumpus at [" + str(i) + ", " + str(j) + "]")

                        try:
                            if i-1 >= 0:
                                if 'S' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('S')
                        except IndexError:
                            pass

                        try:
                            if j+1 < self.num_cols:
                                if 'S' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('S')
                        except IndexError:
                            pass

                        try:
                            if i+1 < self.num_rows:
                                if 'S' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('S')
                        except IndexError:
                            pass

                        try:
                            if j-1 >= 0:
                                if 'S' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('S')
                        except IndexError:
                            pass

                    """
                    if self.world[i][j][k] == 'G':
                        print("Gold at [" + str(i) + ", " + str(j) + "]")
                    """

                    if self.world[i][j][k] == 'P':
                        # print("Pit at [" + str(i) + ", " + str(j) + "]")

                        try:
                            if i-1 >= 0:
                                if 'B' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('B')
                        except IndexError:
                            pass

                        try:
                            if j+1 < self.num_cols:
                                if 'B' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('B')
                        except IndexError:
                            pass

                        try:
                            if i+1 < self.num_rows:
                                if 'B' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('B')
                        except IndexError:
                            pass

                        try:
                            if j-1 >= 0:
                                if 'B' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('B')
                        except IndexError:
                            pass