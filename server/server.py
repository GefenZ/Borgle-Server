#!/usr/bin/env python3

from multiprocessing.connection import Client
import socket
import os
import sys
import time
from _thread import *
from borgle import *


def print_board(board: Board, player1: Player, player2: Player):
    print("         "+str(player2.towers[2].hp)+"  "+str(player2.towers[1].hp)+"  "+str(player2.towers[0].hp))
    for i in range(6,-1,-1):
        print(str(i) + ": ", end="")
        for  j in range(7):
            if (i==6 and (j!=0 and j!=5)) or (i==0 and (j!=0 and j!=5)):
                end = ","
            else: 
                end = ", "
            print(board.board_hexagons[chr(ord('A')+j)][i].num_of_soldiers, end=end)
        print('\n')
    print("         "+str(player1.towers[0].hp)+"  "+str(player1.towers[1].hp)+"  "+str(player1.towers[2].hp))
    print("   A  B  C  D  E  F  G")
    print("----------------------")

def compare_strs(s1,s2):
    if(len(s1)!=len(s2)):
        return False
    for i in range(len(s1)):
        if(s1[i] != s2[i]):
            return False
    return True

def menu(connection):
    
    while True:
        connection.send(str.encode('''Welcome to Borgle!\n
        1 - login
        2 - register
        3 - exit                                                    
        '''))
        answer = connection.recv(1024).decode()
        if answer == "1":
            connection.send(str.encode("Please enter Username and Password.\n"))
            result = handle_login(connection)
            if result != "-1":
               return  result   
        elif answer == "2":
            connection.send(str.encode("Please enter Username and Password.\n"))
            handle_registration(connection)
        elif answer =="3":
            connection.send(str.encode("Goodbye!"))
            connection.close()
            return "3"
        else:
            connection.send(str.encode("invalid choice"))

def handle_login(connection):
    username = connection.recv(1024).decode()
    print("Username: " + str(username))
    password = connection.recv(1024).decode()
    print("Password: " + str(password))

    with open("/home/ec2-user/Borgle-Server/server/DataBase.txt", "r+") as db:
        lines = db.readlines()
        found = False
        for row in range(len(lines)):
            if compare_strs(lines[row].replace("\n",""), username):
                p = lines[row+1].replace("\n","")
                if compare_strs(p,password):
                    connection.send(("Welcome " + str(username) + "!").encode())
                    found = True
                    return username
                else:
                    connection.send("Incorrect password".encode())
                    found = True
                    return "-1"
        if not found:
            connection.send("this user does not exist".encode())
            return "-1"


def handle_registration(connection):
    username = connection.recv(1024).decode()
    print("Username: " + str(username))
    password = connection.recv(1024).decode()
    print("Password: " + str(password))

    with open("/home/ec2-user/Borgle-Server/server/DataBase.txt", "r+") as db:
        lines = db.readlines()
        for row in range(len(lines)):
            if compare_strs(lines[row].replace("\n",""), username):
                connection.send("This username already exists.".encode())
                return 
        db.seek(0,2)
        db.write('\n'+username)
        db.write('\n'+password)
        connection.send("Registration successful!".encode())
        return

def save_submission(connection, username):
    size = int(connection.recv(1024).decode())
    print("file size: " + str(size))
    contents = connection.recv(size).decode()
    file_name = "/home/ec2-user/Borgle-Server/server/Submissions/"+username +".py"
    with open(file_name,"w") as file:
        file.write(contents)
        file.close()
    with open(file_name,"r") as file:
        c = file.read()
        if compare_strs(c, contents):
            connection.send("Submission success!".encode())
        else:
            connection.send("Something went wrong with the submissions...".encode())

def fight(connection, username, rival):
    user_fp = __import__("Submissions."+username, fromlist=[None]).MyGame.calcTurn
    rival_fp = __import__("Submissions."+rival, fromlist=[None]).MyGame.calcTurn
    player1_green = Player("GREEN")
    player2_red = Player("RED")
    board = Board()
    validate1 = Validate()
    validate2 = Validate()
    state1 = State(board, player1_green, player2_red, validate1)
    state2 = State(board, player2_red, player1_green, validate2)
    print_board(board, player1_green, player2_red)
    while True:
        time.sleep(0.5)
        validate1.check_one_move = False
        user_fp(state1)
        player1_green.turn_number += 1
        player1_green.get_income()
        print_board(board, player1_green, player2_red)
        time.sleep(0.5)
        validate2.check_one_move = False
        rival_fp(state2)
        player2_red.turn_number += 1
        player2_red.get_income()
        print_board(board, player1_green, player2_red)

def handle_fight(connection, username, rivals_list):
    try:
        rival_inedx = int(connection.recv(1024).decode()) - 1
    except:
        connection.send("invalid choice".encode())
        return
    if rival_inedx<0 or rival_inedx >= len(rivals_list):
        connection.send("invalid choice".encode())
        return
    else:
        connection.send(("You shall fight "+rivals_list[rival_inedx]+"!").encode())
    fight(connection, username, rivals_list[rival_inedx])

def game_loop(connection, username):
     while True:
        connection.send(str.encode('''Enter your choice\n
        1 - fight
        2 - submit your algorithem    
        3 - exit                                      
        '''))
        answer = connection.recv(1024).decode()
        if answer == "1":
            s = "Who do you want to fight?\n"
            rivals_list = []
            with open("/home/ec2-user/Borgle-Server/server/DataBase.txt", "r") as db:
                lines = db.readlines()
                counter = 1
                for i in range(1,len(lines),2):
                    if not compare_strs(lines[i].replace("\n",""),username):
                        s+= str(counter) + "- " + lines[i]
                        rivals_list.append(lines[i].replace("\n",""))
                        counter += 1
            db.close()
            connection.send(s.encode())
            handle_fight(connection, username, rivals_list)
        elif answer == "2":
            connection.send("saving algorithem..." .encode())
            save_submission(connection, username)
        elif answer =="3":
            connection.send(str.encode("Goodbye!"))
            connection.close()
            return "3"
        else:
            connection.send(str.encode("invalid choice"))

def threaded_client(connection):
    result = menu(connection)
    if result == "3":
        print("Connection closed.")
        return
    else:
        result = game_loop(connection, result)
        if result == "3":
            print("Connection closed.")
            return

    connection.close()

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 6666
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection...')
ServerSocket.listen(5)

while True:
    client, address = ServerSocket.accept()
    print('Connected to: '+ address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (client, ))
    ThreadCount += 1
    print('Thread Number: '+ str(ThreadCount))

ServerSocket.close()
