from enum import IntEnum
from random import randint
from re import S
import string
from wsgiref import validate

class Constants:
    # hp levels:
    SIDE_TOWER_HP = [10, 14, 18, 22, 26, 30, 34, 38, 42, 46]
    MIDDLE_TOWER_HP = [13, 22, 31, 40, 49, 58, 67, 76, 85, 94]

    # income levels:
    SIDE_TOWER_INCOME = [2, 3, 4, 5, 7, 9, 11, 14, 17, 20]
    MIDDLE_TOWER_INCOME = [4, 5, 6, 8, 10, 13, 16, 20, 24, 28]

    #upgrade
    UPGRADE_LEVEL_COST = [18, 32, 50, 78, 119, 176, 243, 340, 451]

    # board:
    SUM_OF_ROW = 30

class Type(IntEnum):
    REGISTER = 0
    GET_USERS = 1
    SUBMIT = 2
    FIGHT = 3

class BoardHexagonType(IntEnum):
    NEUTRAL = 0
    GREEN = 1
    RED = 2

class BorgleException(Exception):
    pass


class Tower:
    def __init__(self, middle, side):
        self.middle = middle
        if middle :
            self.hp = Constants.MIDDLE_TOWER_HP[0]
            self.income = Constants.MIDDLE_TOWER_INCOME[0]
        else:
            self.hp = Constants.SIDE_TOWER_HP[0]
            self.income = Constants.SIDE_TOWER_INCOME[0]
            
        self.side = side
class Player:
    def __init__(self, side):
        self.level = 1
        self.side = side
        self.towers = [Tower(middle=False, side=side), Tower(middle=True, side=side), Tower(middle=False , side=side)]
        self.coins = 0
        self.turn_number = 1
    
    def get_income(self):
        for t in self.towers:
            if t.hp > 0:
                if t.middle:
                    self.coins += Constants.MIDDLE_TOWER_INCOME[self.level-1]
                else:
                    self.coins += Constants.SIDE_TOWER_INCOME[self.level-1]

    def upgrade(self):
        for t in self.towers:
            if t.hp > 0:
                if t.middle :
                    self.hp += Constants.MIDDLE_TOWER_HP[self.level-1] - Constants.MIDDLE_TOWER_HP[self.level - 2]
                    self.income = Constants.MIDDLE_TOWER_INCOME[self.level-1]
                else:
                    self.hp += Constants.SIDE_TOWER_HP[self.level-1] - Constants.SIDE_TOWER_HP[self.level-2]
                    self.income = Constants.SIDE_TOWER_INCOME[self.level-1]



class BoardHexagon:
    def __init__(self, board_hexagon_type: BoardHexagonType, num_of_soldiers):
        self.board_hexagon_type = board_hexagon_type
        self.num_of_soldiers = num_of_soldiers
class Board:
    def __init__(self):
        self.board_hexagons = {"A":[BoardHexagon(BoardHexagonType.NEUTRAL, randint(0,10)), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, randint(0,10))],
        "B": [BoardHexagon(BoardHexagonType.GREEN, 10), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.RED, 10)],
        "C": [BoardHexagon(BoardHexagonType.GREEN, 10), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.RED, 10)],
        "D": [BoardHexagon(BoardHexagonType.GREEN, 10), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.RED, 10)],
        "E": [BoardHexagon(BoardHexagonType.GREEN, 10), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.RED, 10)],
        "F": [BoardHexagon(BoardHexagonType.GREEN, 10), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.RED, 10)],
        "G": [BoardHexagon(BoardHexagonType.NEUTRAL, randint(0,10)), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, 0), BoardHexagon(BoardHexagonType.NEUTRAL, randint(0,10))]
        }
        for i in range(1,6):
            rand_row = [0]*7
            for j in range(Constants.SUM_OF_ROW) : 
                rand_row[randint(0, Constants.SUM_OF_ROW) % 7] += 1
            for j in range(7):
                self.board_hexagons[chr(ord('A')+j)][i].num_of_soldiers = rand_row[j]
        

    


def inverse_location(location: str) -> list:
    l = ['A',0]
    if location[0] ==  'A':
        l[0] ='G'
    if location[0] == 'B':
        l[0] ='F'
    if location[0] == 'C':
        l[0] ='E'
    if location[0] == 'D':
        l[0] ='D'
    if location[0] == 'E':
        l[0] ='C'
    if location[0] == 'F':
        l[0] ='B'
    if location[0] == 'G':
        l[0] ='A' 
    l[1] = 6 - int(location[1])
    return l

def inverse_tower_location(tower_location: str) -> str:
    if tower_location == "left":
        return "right"
    elif tower_location == "right":
        return "left"
    return "middle"

class Validate:
    def __init__(self):
        self.check_one_move = False

    def validate_location(location) -> list:
        if type(location) is not str: # must get str as location
            raise BorgleException("location must be str, you gave: " + str(type(location)))
        if len(location) != 2: # must get only 2 characters
            raise BorgleException("length of location must be 2(for example: A4), you gave: " + location)
        try:
            index2 = int(location[1])
            index1 = location[0]
        except: # second integer must be char between 0-6
            raise BorgleException("second char of location must be char between 0 - 6(for example: A0,D6)")
        l = [index1, index2]
        if index1 <'A' or index1 >'G': # index 1 must be on the board
            raise BorgleException("first char of location must be between A-G(for example A3,G0)")
        if index2 < 0 or index2 > 6: # index 2 must be on the board
            raise BorgleException("second char of location must be char between 0-6(for example: A0,D6)")
        return l
    def validate_tower_location(tower_location):
        if type(tower_location) is not str: # must get str as location
            raise BorgleException("location must be str, you gave: "+str(type(tower_location)))
        if tower_location!= "left" and tower_location!="middle" and tower_location!= "right":
            raise BorgleException("Tower location must be: left, middle, or right")

    def validate_num_of_soldiers(num_of_soldiers):
        if type(num_of_soldiers) is not int: # must get number of soldiers as integer
            raise BorgleException("num_of_soldiers must be int")
        if num_of_soldiers <=0: # must get positive number of soldiers
            raise BorgleException("num of soldiers must be a positive integer")
    
    def validate_move(board: Board, from_list, to_list, num_of_soldiers, side):
        v = 1
        if side == "GREEN":
            v = BoardHexagonType.GREEN.value
        elif side == "RED":
            v = BoardHexagonType.RED.value
        if board.board_hexagons[from_list[0]][from_list[1]].board_hexagon_type.value != v: # move only something on your side
            raise BorgleException("can not move soldiers from hexagon you do not have soldiers on") 
        if board.board_hexagons[from_list[0]][from_list[1]].num_of_soldiers < num_of_soldiers: # cant move more soldiers than you have on one hexagon
            raise BorgleException("num of soldiers specified is bigger that the actual number of soldiers")
        if to_list[0] == from_list[0] and to_list[1] == from_list[1]: #cant move from same hexagon to same hexagon
            raise BorgleException("can not move soldiers to same hexagon")
        if (ord(to_list[0]) != (ord(from_list[0]) + 1) and ord(to_list[0]) != (ord(from_list[0]) - 1) and ord(to_list[0]) != ord(from_list[0]) or int(to_list[1]) != (int(from_list[1]) + 1) and int(to_list[1]) != (int(from_list[1]) - 1) and int(to_list[1]) != int(from_list[1])): # can only move up, down, right, left, up-right, up-left, down-right, down-left
            raise BorgleException("illegal hexagon to move(can only move up, down, left, right, up-right, up-left, down-right and down-left")

    def validate_attack(board: Board, from_list, tower_location, num_of_soldiers, side):
        v = 1
        attack_location = 0
        if side == "GREEN":
            v = BoardHexagonType.GREEN.value
            attack_location = 6
        elif side == "RED":
            v = BoardHexagonType.RED.value
        print(v,", ", from_list)
        if board.board_hexagons[from_list[0]][from_list[1]].board_hexagon_type.value != v: # move only something on your side
            raise BorgleException("can not attack with soldiers from hexagon you do not have soldiers on") 
        if board.board_hexagons[from_list[0]][from_list[1]].num_of_soldiers < num_of_soldiers: # cant move more soldiers than you have on one hexagon
            raise BorgleException("num of soldiers specified is bigger that the actual number of soldiers")
        if tower_location == "left":
            if from_list[1]!=attack_location or (from_list[0]!='B' and from_list[0]!='C' and from_list[0]!='D'):
                raise BorgleException(f"can not attack {tower_location} tower from this location : {from_list[0]}, {str(from_list[1])}")
        elif tower_location == "right":
            if from_list[1]!=attack_location or (from_list[0]!='D' and from_list[0]!='E' and from_list[0]!='F'):
                raise BorgleException(f"can not attack {tower_location} tower from this location : {from_list[0]}, {str(from_list[1])}")
        elif tower_location == "middle":
            if from_list[1]!=attack_location  or (from_list[0]!='C' and from_list[0]!='D' and from_list[0]!='E'):
                raise BorgleException(f"can not attack {tower_location} tower from this location : {from_list[0]}, {str(from_list[1])}")

class State:
    def __init__(self, board: Board, player: Player, enemy_player: Player, validate: Validate):
        self.__player = player
        self.__enemy_player = enemy_player
        self.__board = board
        self.__validate = validate

    def get_side(self):
        return self.__player.side

    def get_turn_number(self):
        return self.__player.turn_number
    
    def get_board_hexagon_type(self, location: str) -> str:
        l = Validate.validate_location(location)
        if self.__player.side == "RED":
            l = inverse_location(location)
        if self.__board.board_hexagons[l[0]][l[1]].board_hexagon_type == BoardHexagonType.GREEN:
            return "GREEN"
        elif self.__board.board_hexagons[l[0]][l[1]].board_hexagon_type == BoardHexagonType.RED:
            return "RED"
        else:
            return "NEUTRAL"
    def get_board_hexagon_num_of_soldiers(self, location: str):
        l = Validate.validate_location(location)
        if self.__player.side == "GREEN":
            return self.__board.board_hexagons[l[0]][l[1]].num_of_soldiers
        else:
            l = inverse_location(location)
            return self.__board.board_hexagons[l[0]][l[1]].num_of_soldiers
    def get_left_tower_hp(self):
        return self.__player.towers[0].hp
    def get_middle_tower_hp(self):
        return self.__player.towers[1].hp
    def get_right_tower_hp(self):
        return self.__player.towers[2].hp
    def get_enemy_left_tower_hp(self):
        return self.__enemy_player.towers[2].hp
    def get_enemy_middle_tower_hp(self):
        return self.__enemy_player.towers[1].hp
    def get_enemy_right_tower_hp(self):
        return self.__enemy_player.towers[0].hp
    
    def attack_tower(self, from_location: str, tower_location: str, num_of_soldiers: int):
        if(self.__validate.check_one_move):
            raise BorgleException("you have already made your move - can not make another move")

        from_list = Validate.validate_location(from_location)
        Validate.validate_tower_location(tower_location)
        Validate.validate_num_of_soldiers(num_of_soldiers)
        if self.__player.side == "RED":
            from_list = inverse_location(from_location)
        else:
            tower_location = inverse_tower_location(tower_location)
        Validate.validate_attack(self.__board, from_list, tower_location, num_of_soldiers, self.__player.side)
        tower_index = 0
        if tower_location == "left":
            tower_index = 0
        elif tower_location == "middle":
            tower_index = 1
        elif tower_location == "right":
            tower_index = 2
        
        if self.__enemy_player.towers[tower_index].hp == 0:
            raise BorgleException("can not attack tower which is already destroyed")
        else:
            if num_of_soldiers >= self.__enemy_player.towers[tower_index].hp:
                self.__board.board_hexagons[from_list[0]][from_list[1]].num_of_soldiers -= self.__enemy_player.towers[tower_index].hp
                self.__enemy_player.towers[tower_index].hp = 0
            else:
                self.__enemy_player.towers[tower_index].hp -= num_of_soldiers
                self.__board.board_hexagons[from_list[0]][from_list[1]].num_of_soldiers -= num_of_soldiers
            

        self.__validate.check_one_move = True
    
    def move_soldiers(self, from_location: str, to_location: str, num_of_soldiers: int):
        if(self.__validate.check_one_move):
            raise BorgleException("you have already made your move - can not make another move")

        from_list = Validate.validate_location(from_location)
        to_list = Validate.validate_location(to_location)
        Validate.validate_num_of_soldiers(num_of_soldiers)
        if self.__player.side == "RED":
            from_list = inverse_location(from_location)
            to_list = inverse_location(to_location)
        Validate.validate_move(self.__board, from_list, to_list, num_of_soldiers, self.__player.side)

        board_hexa_from = self.__board.board_hexagons[from_list[0]][from_list[1]]
        board_hexa_to = self.__board.board_hexagons[to_list[0]][to_list[1]]

        board_hexa_from.num_of_soldiers -= num_of_soldiers
        if board_hexa_from.num_of_soldiers == 0:
            board_hexa_from.board_hexagon_type = BoardHexagonType.NEUTRAL
        if self.__player.side == "GREEN":
            if board_hexa_to.board_hexagon_type == BoardHexagonType.GREEN:
                    board_hexa_to.num_of_soldiers += num_of_soldiers
            elif board_hexa_to.board_hexagon_type == BoardHexagonType.RED:
                if board_hexa_to.num_of_soldiers >= num_of_soldiers:
                    board_hexa_to.num_of_soldiers -= num_of_soldiers 
                    if board_hexa_to.num_of_soldiers == 0:
                        board_hexa_to.board_hexagon_type = BoardHexagonType.NEUTRAL
                else:
                    board_hexa_to.num_of_soldiers = num_of_soldiers - board_hexa_to.num_of_soldiers
                    board_hexa_to.board_hexagon_type = BoardHexagonType.GREEN
            elif board_hexa_to.board_hexagon_type == BoardHexagonType.NEUTRAL:
                board_hexa_to.num_of_soldiers += num_of_soldiers
                board_hexa_to.board_hexagon_type = BoardHexagonType.GREEN
        else:
            if board_hexa_to.board_hexagon_type == BoardHexagonType.GREEN:
                if board_hexa_to.num_of_soldiers >= num_of_soldiers:
                    board_hexa_to.num_of_soldiers -= num_of_soldiers 
                    if board_hexa_to.num_of_soldiers == 0:
                        board_hexa_to.board_hexagon_type = BoardHexagonType.NEUTRAL
                else:
                    board_hexa_to.num_of_soldiers = num_of_soldiers - board_hexa_to.num_of_soldiers
                    board_hexa_to.board_hexagon_type = BoardHexagonType.RED
            elif board_hexa_to.board_hexagon_type == BoardHexagonType.RED:
                board_hexa_to.num_of_soldiers += num_of_soldiers
            elif board_hexa_to.board_hexagon_type == BoardHexagonType.NEUTRAL:
                board_hexa_to.num_of_soldiers += num_of_soldiers
                board_hexa_to.board_hexagon_type = BoardHexagonType.RED
        
        self.__validate.check_one_move = True
        print(from_location + ":" + to_location)

    def get_level(self):
        return self.__player.level

    def get_upgrade_level_cost(self):
        if self.__player.level >= 10:
            raise BorgleException("can not upgrade - max level reached")
        return Constants.UPGRADE_LEVEL_COST[self.__player.level-1]

    def upgrade_level(self):
        if self.__player.level >= 10:
            raise BorgleException("can not upgrade - max level reached")
        if(self.__player.coins < Constants.UPGRADE_LEVEL_COST[self.__player.level-1]):
            raise BorgleException("you dont have enough money to upgrade your level")
        self.__player.level += 1
        self.__player.upgrade()



class Game:
    def __init__(self):
        pass

    def calcTurn(state: State):
        print("this is an automatic response of turn calculating")








