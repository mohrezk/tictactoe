from zero import ZeroServer
import json 


app = ZeroServer(port=5559)

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
current_player = 1

@app.register_rpc
def check_for_winner(msg: str) -> str:
    data = json.loads(msg)
    print(data)
    row = data['row']
    col = data['col']
    board = data['board']
    winner = None

    # Check rows
    for row in board:
        if row.count(row[0]) == len(row) and row[0] != 0:
            winner = row[0]
            break

    # Check columns
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
            winner = board[0][col]
            break

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        winner = board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        winner = board[0][2]

    if all([all(row) for row in board]) and winner is None:
        winner = "tie"


    return winner




if __name__ == "__main__":
    app.run()

