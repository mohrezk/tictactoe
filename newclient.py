import tkinter as tk
from tkinter import messagebox
from zero import ZeroClient
import json 


zero_client = ZeroClient("localhost", 5559)

window = tk.Tk()
window.title("Tic Tac Toe")

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
current_player = 1


class RpcClient:
    def __init__(self, zero_client: ZeroClient):
        self._zero_client = zero_client
        self.player_id = None
        self.board_created = False
    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(window, text="", font=("Arial", 50), height=2, width=6, bg="lightblue", command=lambda row=i, col=j: self.handle_click(row, col))
                button.grid(row=i, column=j, sticky="nsew")

        self.board_created = True 

    def start(self): 
        window.mainloop()
        
    def handle_click(self, row, col):
        global current_player

        if self.player_id == current_player:
            if board[row][col] == 0:
                if current_player == 1:
                    board[row][col] = "X"
                    current_player = 2
                else:
                    board[row][col] = "O"
                    current_player = 1

                button = window.grid_slaves(row=row, column=col)[0]
                button.config(text=board[row][col])

                data = json.dumps({'row': row, 'col': col, 'board': board}) 
                winner = zero_client.call("check_for_winner", data)

                if winner:
                    self.declare_winner(winner)
      
    def declare_winner(self, winner):
        if winner == "tie":
            message = "It's a tie!"
        else:
            message = f"Player {winner} wins!"


        answer = messagebox.askyesno("Game Over", message + " Do you want to restart the game?")

        if answer:
            global board
            board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

            for i in range(3):
                for j in range(3):
                    button = window.grid_slaves(row=i, column=j)[0]
                    button.config(text="")

            global current_player
            current_player = 1
        else:
            window.quit()
