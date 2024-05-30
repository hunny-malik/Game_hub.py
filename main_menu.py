import tkinter as tk
import subprocess

def run_game(game_file):
    subprocess.Popen(['python', game_file])

root = tk.Tk()
root.title("GameHUB")
root.geometry("400x300")  # Set the window size to 400x300

games = {
    "Dino Game": "dino.py",
    "Bird Game": "bird.py",
    "Parking Game": "parking.py",
    "Snake Game": "snake.py",
    "Tic Tac Toe Game": "tictactoe.py"
}

for game_name, game_file in games.items():
    button = tk.Button(root, text=game_name, command=lambda file=game_file: run_game(file))
    button.pack(pady=10)

t = tk.Label(root, text = '--By Hunny Malik')
t.pack()

root.mainloop()
