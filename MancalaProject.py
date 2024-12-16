import pygame
import tkinter as tk
from tkinter import messagebox


class Mancala:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load background music
        pygame.mixer.music.load("backgroundjazz.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set the volume
        pygame.mixer.music.play(-1, 0.0)  # Play music in a loop

        # Load sound effects
        self.move_sound = pygame.mixer.Sound("movesound.mp3")
        self.capture_sound = pygame.mixer.Sound("capturesound.mp3")
        self.game_over_sound = pygame.mixer.Sound("gameoversound.mp3")

        # Initialize game variables
        self.stones = [4] * 6 + [0] + [4] * 6 + [0]
        self.current_player = 1
        self.p1score = 0
        self.p2score = 0

        # Initialize UI components
        self.create_widgets()
        self.create_grid()
        self.create_scoreboard()

    def create_widgets(self):
        # Welcome and player indicator labels
        self.welcome_label = tk.Label(self.root, text="Welcome to Mancala", font=('Arial', 24))
        self.welcome_label.pack(pady=10, anchor="center")

        self.goal1_label = tk.Label(self.root, text="Goal 1", font=('Arial', 18))
        self.goal1_label.pack(side="left", padx=25, pady=10, anchor="center")

        self.goal2_label = tk.Label(self.root, text="Goal 2", font=('Arial', 18))
        self.goal2_label.pack(side="right", padx=25, pady=10, anchor="center")

        self.player_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn", font=('Arial', 18))
        self.player_label.pack(pady=5, anchor="center")

        self.Rules = tk.Button(self.root, text="Rules", font=('Arial', 12), width=5, height=1,
                               command=self.rules_button_click)
        self.Rules.pack(pady=5, anchor="center")

        self.Reset = tk.Button(self.root, text="Reset", font=('Comic Sans', 12), width=5, height=1,
                               command=self.reset_button_click)
        self.Reset.pack(pady=5, anchor="center")

    def create_grid(self):
        self.frame = tk.Frame(self.root, bg="#A1662F")
        self.frame.pack(pady=20, anchor="center")

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
        for col in range(6):
            self.buttons[0][5 - col].config(state="normal")
            self.buttons[1][col].config(state="disabled")

    def create_scoreboard(self):
        self.scoreboard = tk.Label(self.root, text=f"Player 1: {self.p1score}\nPlayer 2: {self.p2score}",
                                   font=('Arial', 18))
        self.scoreboard.pack(pady=10, anchor="center")

    def on_button_click(self, row, col):
        if (self.current_player == 1 and row == 0 and self.stones[col] > 0) or \
                (self.current_player == 2 and row == 1 and self.stones[col] > 0):

            # Play move sound when player clicks a pocket
            self.move_sound.play()

            stones_to_distribute = self.stones[col]
            self.stones[col] = 0
            current_index = col

            # Distribute stones
            while stones_to_distribute > 0:
                current_index = (current_index + 1) % 14

                if self.current_player == 1 and current_index == 13:
                    continue
                elif self.current_player == 2 and current_index == 6:
                    continue

                self.stones[current_index] += 1
                stones_to_distribute -= 1

            # Check for capture
            if self.stones[current_index] == 1 and self.stones[12 - current_index] > 0:
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
                # Play capture sound
                self.capture_sound.play()

            self.update_board()

            # Check for game end
            self.check_game_end()

            # Switch player
            if stones_to_distribute == 0 and (current_index != 13 and current_index != 6):
                self.current_player = 2 if self.current_player == 1 else 1
                self.player_label.config(text=f"Player {self.current_player}'s Turn")

            self.update_board()

    def rules_button_click(self):
        tk.messagebox.showinfo("Rules:", """
        These are the rules of Mancala:

        1. Each player takes turns picking up all the stones from one of their side's pockets by clicking on it.
        2. The player distributes the stones one by one in each pocket counterclockwise, skipping the opponent's goal.
        3. If the last stone lands in an empty pocket on the player's side, and the opposite pocket has stones, the player captures the stones from the opposite pocket.
        4. If the last stone lands in the player's goal, the player gets to play another turn
        5. The game ends when one player has no stones left in any of their pockets. The other player captures the remaining stones.
        """)

    def reset_button_click(self):
        self.current_player = 1
        self.player_label.config(text=f"Player {self.current_player}'s Turn")
        self.stones = [4] * 6 + [0] + [4] * 6 + [0]
        self.update_board()

    def check_game_end(self):
        if sum(self.stones[:6]) == 0 or sum(self.stones[7:13]) == 0:
            # Collect remaining stones
            self.stones[6] += sum(self.stones[:6])
            self.stones[13] += sum(self.stones[7:13])
            for i in range(6):
                self.stones[i] = 0
            for i in range(7, 13):
                self.stones[i] = 0
            self.update_board()

            # Play game over sound
            self.game_over_sound.play()

            # Determine the winner
            if self.stones[6] > self.stones[13]:
                winner = "Player 1"
                self.p1score += 1
            elif self.stones[6] < self.stones[13]:
                winner = "Player 2"
                self.p2score += 1
            else:
                winner = "It's a tie! Nobody"

            messagebox.showinfo("Game Over", f"Game over! {winner} wins!")

            self.scoreboard.config(text=f"Player 1: {self.p1score}\nPlayer 2: {self.p2score}")

            # Stop the background music when the game ends
            pygame.mixer.music.stop()

    def update_board(self):
        # Update button text to reflect the stones array
        for col in range(6):
            # Update the text for Player 1 (top row)
            self.buttons[0][5 - col].config(text=str(self.stones[5 - col]))
            # Update the text for Player 2 (bottom row)
            self.buttons[1][col].config(text=str(self.stones[col + 7]))

        # Enable or disable buttons based on the current player
        for col in range(6):
            if self.current_player == 1:
                # Player 1's turn: Enable Player 1's pockets (top row), disable Player 2's (bottom row)
                self.buttons[0][5 - col].config(state="normal")
                self.buttons[1][col].config(state="disabled")
            elif self.current_player == 2:
                # Player 2's turn: Enable Player 2's pockets (bottom row), disable Player 1's (top row)
                self.buttons[0][5 - col].config(state="disabled")
                self.buttons[1][col].config(state="normal")

        # Update the goals for both players
        self.goal_left.config(text=str(self.stones[6]))
        self.goal_right.config(text=str(self.stones[13]))


def main():
    root = tk.Tk()

    # Get the width and height of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Get the width and height of the window
    window_width = 1200  # You can adjust this as needed
    window_height = 600  # You can adjust this as needed

    # Calculate the x and y coordinates for centering the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the dimensions of the window and its position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create Mancala game object
    game = Mancala(root)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
