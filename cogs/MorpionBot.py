import discord
from discord.ext import commands
from secret import *
import random

class MorpionBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="permet de me parler")
    @commands.check(dev_or_not)
    async def start_morpion(self, ctx):
        print(f"{WAITING_REQUEST}" % ("[ACTION]", "[LAUNCH] Morpion"))
        find = 0
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.name == "morpion":
                    find = 1
                    break
            if find == 1:
                break
        if find == 1:
            print(f"y a le channel morpion")
        else:
            print("y a rien")


class Board(MorpionBot):

    def __init__(self):
        self.board = [" " for x in range(10)]

    def InsertLetter(self, letter, pos):
        try:
            self.board[pos] = letter
        except:
            print("Tie Game!")

    def SpaceFree(self, pos):
        lol = [self.InsertLetter]
        return self.board[pos] == " "

    @staticmethod
    def Board(Board):
        print(" " + Board[1] + " | " + Board[2] + " | " + Board[3])
        print("-----------")
        print(" " + Board[4] + " | " + Board[5] + " | " + Board[6])
        print("-----------")
        print(" " + Board[7] + " | " + Board[8] + " | " + Board[9])

    @staticmethod
    def BoardFull(board):

        if board.count(" ") > 1:
            return False
        else:
            return True

    @staticmethod
    def Winner(bo, le):

        return (bo[7] == le and bo[8] == le and bo[9] == le) or (bo[1] == le and bo[4] == le and bo[7] == le) or \
               (bo[4] == le and bo[5] == le and bo[6] == le) or (bo[2] == le and bo[5] == le and bo[8] == le) or \
               (bo[1] == le and bo[2] == le and bo[3] == le) or (bo[3] == le and bo[6] == le and bo[9] == le) or \
               (bo[1] == le and bo[5] == le and bo[9] == le) or (bo[3] == le and bo[5] == le and bo[7] == le)

    def AImove(self):
        global move
        moves_possible = [x for x, letter in enumerate(self.board) if letter == ' ' and x != 0]

        move = 0

        for let in ['O', 'X']:
            for i in moves_possible:
                BoardCopy = self.board[:]
                BoardCopy[i] = let
                if self.Winner(BoardCopy, let):
                    move = i
                    return move

        CornersOpen = []
        for i in moves_possible:
            if i in [1, 3, 7, 9]:
                CornersOpen.append(i)
        if len(CornersOpen) > 0:
            move = self.SelectRandom(CornersOpen)
            return move

        if 5 in moves_possible:
            move = 5
            return move

        EdgesOpen = []
        for i in moves_possible:
            if i in [2, 4, 6, 8]:
                EdgesOpen.append(i)
        if len(EdgesOpen) > 0:
            move = self.SelectRandom(EdgesOpen)
            return move

    def UserMove(self):
        run = True
        while run:

            move = input("please select a position to place an X (1-9): ")
            try:
                move = int(move)
                if 0 < move < 10:
                    if self.SpaceFree(move):
                        run = False
                        self.InsertLetter("X", move)
                    else:
                        print("place occupied")
                else:
                    print("Please Type a number within in range ! ")
            except:
                print("please type a number")

    @staticmethod
    def SelectRandom(li):

        ln = len(li)
        r = random.randrange(0, ln)
        return li[r]


Board = Board()


def main():
    print("welcometo the Tic Tac Toe game")
    print("the boxes are count from left to right")
    Board.Board(Board.board)
    while not Board.BoardFull(Board.board):
        if not Board.Winner(Board.board, "O"):
            Board.UserMove()
            Board.Board(Board.board)
        else:
            print("Sorry, my AI won this time :)")
            break
        if not Board.Winner(Board.board, "X"):
            move = Board.AImove()
            if move == 0:
                print("Tie Game!")
            else:
                Board.InsertLetter("O", move)
                print("Ai placed an \'O\' in position", move)
                Board.Board(Board.board)
        else:
            print("Good job, you win ")
            break
    if Board.BoardFull(Board.board):
        print("Tie Game !")



def setup(bot):
    bot.add_cog(MorpionBot(bot))