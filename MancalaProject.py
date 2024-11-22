import tkinter as tk
from tkinter import messagebox

class Mancala:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala")
        self.stones = [4] * 6 + [0] + [4] * 6 + [0]  # Initial stone counts, index 6 and 13 are goals
        self.current_player = 1  # 1 for Player 1 (top row), 2 for Player 2 (bottom row)
        self.create_widgets()
        self.create_grid()

    def create_widgets(self):
        # Welcome and player indicator labels
        self.welcome_label = tk.Label(self.root, text="Welcome to Mancala", font=('Arial', 24))
        self.welcome_label.pack(pady=10)

        self.player_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn", font=('Arial', 18))
        self.player_label.pack(pady=5)

    def create_grid(self):
        self.frame = tk.Frame(self.root, bg="#A1662F")
        self.frame.pack(pady=20)

        self.buttons = [[None for _ in range(8)] for _ in range(2)]

        # Goal 1 (left side) for Player 1
        self.goal_left = tk.Button(self.frame, text=str(self.stones[6]), font=('Arial', 24), width=5, height=5)
        self.goal_left.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

        # Pockets for Player 1 (top row, right to left)
        for col in range(6):
            button = tk.Button(self.frame, text=str(self.stones[5 - col]), font=('Arial', 24), width=5, height=2)
            button.grid(row=0, column=col + 1, padx=5, pady=5)
            button.config(command=lambda r=0, c=5 - col: self.on_button_click(r, c))
            self.buttons[0][5 - col] = button

        # Goal 2 (right side) for Player 2
        self.goal_right = tk.Button(self.frame, text=str(self.stones[13]), font=('Arial', 24), width=5, height=5)
        self.goal_right.grid(row=0, column=7, rowspan=2, padx=5, pady=5)

        # Pockets for Player 2 (bottom row, left to right)
        for col in range(6):
            button = tk.Button(self.frame, text=str(self.stones[col + 7]), font=('Arial', 24), width=5, height=2)
            button.grid(row=1, column=col + 1, padx=5, pady=5)
            button.config(command=lambda r=1, c=col + 7: self.on_button_click(r, c))
            self.buttons[1][col] = button

    def on_button_click(self, row, col):
        if (self.current_player == 1 and row == 0 and self.stones[col] > 0) or \
           (self.current_player == 2 and row == 1 and self.stones[col] > 0):
            stones_to_distribute = self.stones[col]
            self.stones[col] = 0
            current_index = col

            # Distribute stones
            while stones_to_distribute > 0:
                current_index = (current_index + 1) % 14

                # Skip the opponent's goal
                if self.current_player == 1 and current_index == 13:
                    continue
                elif self.current_player == 2 and current_index == 6:
                    continue

                self.stones[current_index] += 1
                stones_to_distribute -= 1

            # Check if the last stone landed in an empty pocket owned by the current player
            if self.stones[current_index] == 1:  # Last stone landed in an empty pocket
                if self.current_player == 1 and 0 <= current_index <= 5:
                    opposite_index = 12 - current_index
                    self.stones[6] += self.stones[opposite_index] + 1
                    self.stones[current_index] = 0
                    self.stones[opposite_index] = 0
                elif self.current_player == 2 and 7 <= current_index <= 12:
                    opposite_index = 12 - current_index
                    self.stones[13] += self.stones[opposite_index] + 1
                    self.stones[current_index] = 0
                    self.stones[opposite_index] = 0

            # Update the board
            self.update_board()

            # Check for game end
            self.check_game_end()

            # Switch player after turn if the game is not over
            if self.stones[6] != sum(self.stones[:6]) and self.stones[13] != sum(self.stones[7:13]):
                self.current_player = 2 if self.current_player == 1 else 1
                self.player_label.config(text=f"Player {self.current_player}'s Turn")

    def check_game_end(self):
        if sum(self.stones[:6]) == 0 or sum(self.stones[7:13]) == 0:
            # Collect remaining stones
            self.stones[6] += sum(self.stones[:6])
            self.stones[13] += sum(self.stones[7:13])
            for i in range(6):
                self.stones[i] = 0
            for i in range(7, 13):
                self.stones[i] = 0

            # Determine the winner
            if self.stones[6] > self.stones[13]:
                winner = "Player 1"
            elif self.stones[6] < self.stones[13]:
                winner = "Player 2"
            else:
                winner = "It's a tie!"

            # Show winner popup
            messagebox.showinfo("Game Over", f"Game over! {winner} wins!")

    def update_board(self):
        # Update button text to reflect the stones array
        for col in range(6):
            self.buttons[0][5 - col].config(text=str(self.stones[5 - col]))
            self.buttons[1][col].config(text=str(self.stones[col + 7]))
        self.goal_left.config(text=str(self.stones[6]))
        self.goal_right.config(text=str(self.stones[13]))


def main():
    root = tk.Tk()
    Mancala(root)
    root.mainloop()


if __name__ == "__main__":
    main()