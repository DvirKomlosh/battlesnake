from api import *
import time
import random
import math


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    times = []
    me = None
    my_head = None
    step_start_time = None

    def get_available_options(self):
        # returns all non killing coordinates for next move
        options = self.get_all_options()
        to_del = []
        # goes over all options, removes only problematic ones (or does it?)
        for direction, coord in options.items():
            if coord in self.context.get_occupied_tiles() or not self.context.in_bounds(
                coord
            ):
                to_del.append(direction)
        for direction in to_del:
            del options[direction]

        return options

    def get_all_options(self):
        # returns all coordinates for next move
        x, y = self.my_head
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def initialize_variables(self):
        # helper function to set variables that will not change during the step
        self.step_start_time = time.time()
        self.me = self.context.get_myself()
        self.my_head = self.context.get_position(self.me)[-1]

    def get_all_other_snakes(self):
        others = []
        myself = self.context.get_myself()
        for snake in self.context.get_active_players():
            if snake.head == myself.head:
                continue
            others.append(snake)
        return others

    def find_way_to_apple(self, options):
        min_dist = 1000
        best_option = None
        for option in options:
            opt_min = min([manhattan_distance(options[option],apple) for apple in self.context.get_apples()])

            if opt_min < min_dist:
                min_dist = opt_min
                best_option = option
        return best_option
    
    def find_way_to_conquer(self, options):
        best_eval = -10
        other_poses = [snake.position for snake in self.get_all_other_snakes()]
        best_option = None
        for option in options:
            new_pos = self.me.position.copy()
            new_pos.append(options[option])
            #self.context.log_error(new_pos)
            opt_max = self.evaluate(new_pos,100,other_poses)
            #self.context.log_error(f"for move {option}, eval is {opt_max}")


            if opt_max > best_eval:
                best_eval = opt_max
                best_option = option
        
        #self.context.log_warning(f"best move {best_option}, eval is {best_eval}")
        return best_option



    def run(self) -> None:
        self.initialize_variables()


        move = "U"
        options = self.get_available_options()
        if self.context.get_health(self.me) < 15:
            if len(options) == 0:
                self.context.log_warning("dying while hungrey!")
                self.context.log_warning("dying while hungrey!")
                self.context.log_warning("dying while hungrey!")
                self.context.log_warning("dying while hungrey!")
                self.context.log_warning("dying while hungrey!")
                self.context.log_warning("dying while hungrey!")

            move = self.find_way_to_apple(options)
            self.context.set_direction(move)
            return
        else:
            move = self.find_way_to_conquer(options)
            self.context.set_direction(move)
            return
        
        options = self.get_available_options()
        if len(options) > 0:
            # takes the a random available option which should not kill him
            move = list(options.keys())[random.randint(0, len(options) - 1)]
        self.context.set_direction(move)
        

        evaluation_value = self.evaluate(self.me.position,100,[snake.position for snake in self.get_all_other_snakes()])
        #self.context.log_info(f"eval of current pos: {evaluation_value}")

        # value_for_option = {"U":-1, "D":-1,"L":-1,"R":-1}
        # for option,new_head in options:
        #     new_pos = self.me.position.copy()
        #     new_pos.insert(0,new_head)
        #     value_for_option[option] = self.evaluate(new_pos, 100, [snake.position for snake in self.get_all_other_snakes()])

        #max(value_for_option.iteritems(), key=value_for_option.itemgetter(1))[0]

        



        self.context.set_direction(move)

        self.times.append(time.time() - self.step_start_time)
        # prints the average time every 100 steps:
        if len(self.times) % 100 == 0:
            average = sum(self.times) / len(self.times)
            self.context.log_info(f"average time per turn : {average}")

    def setup(self) -> None:
        pass

    def adjecent(self, pos):
        x,y = pos
        options = [(x+1,y), (x-1,y),(x,y+1),(x,y-1)]
        return [pos for pos in options if self.context.in_bounds(pos)]


    def evaluate(self, my_snake, hunger, other_snakes):
        length, height = self.context.get_game_size()
        val = 0
        board = [[0 for _ in range(length)] for j in range(height)]
        
        ## set up the board
        for i in range(length):
            for j in range(height):
                if (i,j) in my_snake:
                    board[i][j] = -1
                    val += 1
                else:
                    for snake in other_snakes:
                        if (i,j) in snake:
                            board[i][j] = len(snake)
        heads = []
        ocupied = self.context.get_occupied_tiles()
        for snake in other_snakes:
            for adj in self.adjecent(snake[-1]):
                if self.context.in_bounds(adj) and adj not in ocupied:
                    heads.append(adj)
                    board[adj[0]][adj[1]] = len(snake)
        heads.append(my_snake[-1])


        return self.fill_board(board, heads, my_snake) + val
        
    def fill_board(self, board, heads, my_snake):
        if len(heads) == 0:
            # self.context.log_info(" ")
            # self.context.log_info("new board:")
            # for row in board:
            #     self.context.log_info(row)
            return 0 
        val = 0

        new_heads = []
        my_length = len(my_snake)
        for head in heads:
            if board[head[0]][head[1]] == -1:
                for pos in self.adjecent(head):
                    if board[pos[0]][pos[1]] == -1:
                        continue
                    elif board[pos[0]][pos[1]] == 0:
                        val += 1
                        board[pos[0]][pos[1]] = -1
                        new_heads.append(pos)
                    elif board[pos[0]][pos[1]] < my_length and pos in new_heads:
                        val += 1
                        board[pos[0]][pos[1]] = -1
                        new_heads.remove(pos)
            else:
                for pos in self.adjecent(head):
                    if board[pos[0]][pos[1]] == 0:
                        board[pos[0]][pos[1]] = board[head[0]][head[1]]
                        new_heads.append(pos)
        return self.fill_board(board, new_heads, my_snake) + val


                         



        


