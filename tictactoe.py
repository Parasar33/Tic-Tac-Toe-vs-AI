from tkinter import *
from tkinter import messagebox
import random

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

root = Tk()
root.title("Tic Tac Toe")
center_window(root, 310, 350)

clicked = True
count = 0
difficulty = "Easy"

buttons = []
for i in range(3):
    row = []
    for j in range(3):
        button = Button(root, text="", font=("Helvetica", 20), height=3, width=6, command=lambda row=i, col=j: click(row, col))
        button.grid(row=i, column=j, sticky="nsew")
        row.append(button)
    buttons.append(row)

def click(row, col):
    global clicked, count

    if buttons[row][col]["text"] == "" and clicked:
        buttons[row][col]["text"] = "X"
        count += 1

        if check_win("X"):
            messagebox.showinfo("Tic Tac Toe", "You won!")
            messagebox.showinfo("Tic Tac Toe", "Click reset to play again")
            disable_all_buttons()
        elif count == 9:
            messagebox.showinfo("Tic Tac Toe", "Tie")
            disable_all_buttons()
        else:
            computer_move()
            count += 1

def check_win(player):
    for i in range(3):
        if buttons[i][0]["text"] == player and buttons[i][1]["text"] == player and buttons[i][2]["text"] == player:
            buttons[i][0].config(bg="lightgreen")
            buttons[i][1].config(bg="lightgreen")
            buttons[i][2].config(bg="lightgreen")
            return True

        if buttons[0][i]['text'] == player and buttons[1][i]['text'] == player and buttons[2][i]['text'] == player:
            buttons[0][i].config(bg="lightgreen")
            buttons[1][i].config(bg="lightgreen")
            buttons[2][i].config(bg="lightgreen")
            return True

    if buttons[0][0]['text'] == player and buttons[1][1]['text'] == player and buttons[2][2]['text'] == player:
        buttons[0][0].config(bg="lightgreen")
        buttons[1][1].config(bg="lightgreen")
        buttons[2][2].config(bg="lightgreen")
        return True

    if buttons[0][2]['text'] == player and buttons[1][1]['text'] == player and buttons[2][0]['text'] == player:
        buttons[0][2].config(bg="lightgreen")
        buttons[1][1].config(bg="lightgreen")
        buttons[2][0].config(bg="lightgreen")
        return True

    return False

def computer_move():
    global count
    if count == 0:
        # Randomize the computer's first move
        row, col = random.choice([(0, 0), (0, 2), (2, 0), (2, 2)])
        buttons[row][col]["text"] = "O"
    else:
        if difficulty == "Easy":
            easy_computer_move()
        elif difficulty == "Hard":
            hard_computer_move()

def easy_computer_move():
    row, col = random.choice([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = "O"
    else:
        easy_computer_move()  # Try again if the selected cell is not empty

def hard_computer_move():
    best_score = -float("inf")
    best_move = None
    depth = 2  # Increase the depth of the minimax search

    for i in range(3):
        for j in range(3):
            if buttons[i][j]["text"] == "":
                buttons[i][j]["text"] = "O"
                score = minimax(buttons, depth, False)
                buttons[i][j]["text"] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        row, col = best_move
        buttons[row][col]["text"] = "O"

        if check_win("O"):
            messagebox.showinfo("Tic Tac Toe", "Computer won!")
            messagebox.showinfo("Tic Tac Toe", "Click reset to play again")
            disable_all_buttons()

def minimax(board, depth, is_maximizing):
    scores = {"X": -1, "O": 1, "tie": 0}

    result = check_winner(board)
    if result:
        return scores[result]

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j]["text"] == "":
                    board[i][j]["text"] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j]["text"] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j]["text"] == "":
                    board[i][j]["text"] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j]["text"] = ""
                    best_score = min(score, best_score)
        return best_score

def check_winner(board):
    for i in range(3):
        if board[i][0]["text"] == board[i][1]["text"] == board[i][2]["text"]:
            return board[i][0]["text"]

        if board[0][i]["text"] == board[1][i]["text"] == board[2][i]["text"]:
            return board[0][i]["text"]

    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"]:
        return board[0][0]["text"]

    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"]:
        return board[0][2]["text"]

    if all(board[i][j]["text"] != "" for i in range(3) for j in range(3)):
        return "tie"

    return None

def disable_all_buttons():
    for row in buttons:
        for button in row:
            button.config(state=DISABLED)

def reset():
    global clicked, count
    clicked = True
    count = 0
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state=NORMAL, bg="SystemButtonFace")

def set_difficulty(diff):
    global difficulty
    difficulty = diff
    reset()

my_menu = Menu(root)
root.config(menu=my_menu)

options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Reset Game", command=reset)
options_menu.add_command(label="Set Easy Difficulty", command=lambda: set_difficulty("Easy"))
options_menu.add_command(label="Set Hard Difficulty", command=lambda: set_difficulty("Hard"))

reset()

root.mainloop()
