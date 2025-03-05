import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os

class RPSLSGame:
    def __init__(self, master, img_dir="C:/Users/hitub/OneDrive/Desktop/coding/rpsls"):
        self.master = master
        master.title("Rock Paper Scissors Lizard Spock Game")
        master.configure(background='#0b034e')  # Dark blue background
        self.img_dir = img_dir
        
        # Load images
        self.images = {
            "r_p": self.load_image(os.path.join(self.img_dir, "r_p.png")),
            "p_p": self.load_image(os.path.join(self.img_dir, "p_p.png")),
            "s_p": self.load_image(os.path.join(self.img_dir, "s_p.png")),
            "l_p": self.load_image(os.path.join(self.img_dir, "l_p.png")),
            "sp_p": self.load_image(os.path.join(self.img_dir, "sp_p.png"))
        }
        
        # Initialize game variables
        self.player1_score = 0
        self.player2_score = 0
        self.player1_move = None
        self.player2_move = None

        # Mode selection screen
        self.start_frame = tk.Frame(master, bg='#0b034e')
        self.start_frame.pack()

        self.title_label = tk.Label(self.start_frame, text="~~~~~~~~~~~~~~~~~~\n Rock Paper Scissors Lizard Spock\n ~~~~~~~~~~~~~~~~~~~", font=("Segoe Print", 28, "bold"), bg='#0b034e', fg='#ffffff')
        self.title_label.pack(pady=10)

        self.human_vs_human_button = tk.Button(self.start_frame, text="Human vs Human", font=("Palatino Linotype", 16, "bold"), bg='#ff8080', fg='#ffffff', command=lambda: self.start_game(1))
        self.human_vs_human_button.pack(pady=10)

        self.human_vs_ai_button = tk.Button(self.start_frame, text="Human vs AI", font=("Palatino Linotype", 16, "bold"), bg='#ff8080', fg='#ffffff', command=lambda: self.start_game(2))
        self.human_vs_ai_button.pack(pady=10)

        # Game frame (hidden initially)
        self.game_frame = tk.Frame(master, bg='#0b034e')

        # Labels for Player 1 and Player 2
        self.player1_label = tk.Label(self.game_frame, text="Choose a move to play... Player 1", font=("Palatino Linotype", 18, "bold"), bg='#0b034e', fg='#ff8080', anchor='w')
        self.player2_label = tk.Label(self.game_frame, text="Choose a move to play... Player 2", font=("Palatino Linotype", 18, "bold"), bg='#0b034e', fg='#ff8080', anchor='w')

        # Buttons for Player 1 moves
        self.player1_buttons_frame = tk.Frame(self.game_frame, bg='#0b034e')
        self.player1_rock_button = tk.Button(self.player1_buttons_frame, image=self.images["r_p"], command=lambda: self.set_player_move(1, 'r'), bd=3, relief="solid", bg='#ff0000')
        self.player1_rock_button.grid(row=0, column=0, padx=10, pady=5)

        self.player1_paper_button = tk.Button(self.player1_buttons_frame, image=self.images["p_p"], command=lambda: self.set_player_move(1, 'p'), bd=3, relief="solid", bg='#ff0000')
        self.player1_paper_button.grid(row=0, column=1, padx=10, pady=5)

        self.player1_scissors_button = tk.Button(self.player1_buttons_frame, image=self.images["s_p"], command=lambda: self.set_player_move(1, 's'), bd=3, relief="solid", bg='#ff0000')
        self.player1_scissors_button.grid(row=0, column=2, padx=10, pady=5)

        self.player1_lizard_button = tk.Button(self.player1_buttons_frame, image=self.images["l_p"], command=lambda: self.set_player_move(1, 'l'), bd=3, relief="solid", bg='#ff0000')
        self.player1_lizard_button.grid(row=0, column=3, padx=10, pady=5)

        self.player1_spock_button = tk.Button(self.player1_buttons_frame, image=self.images["sp_p"], command=lambda: self.set_player_move(1, 'sp'), bd=3, relief="solid", bg='#ff0000')
        self.player1_spock_button.grid(row=0, column=4, padx=10, pady=5)

        # Buttons for Player 2 moves (only in Human vs Human mode)
        self.player2_buttons_frame = tk.Frame(self.game_frame, bg='#0b034e')
        self.player2_rock_button = tk.Button(self.player2_buttons_frame, image=self.images["r_p"], command=lambda: self.set_player_move(2, 'r'), bd=3, relief="solid", bg='#ff0000')
        self.player2_rock_button.grid(row=0, column=0, padx=10, pady=5)

        self.player2_paper_button = tk.Button(self.player2_buttons_frame, image=self.images["p_p"], command=lambda: self.set_player_move(2, 'p'), bd=3, relief="solid", bg='#ff0000')
        self.player2_paper_button.grid(row=0, column=1, padx=10, pady=5)

        self.player2_scissors_button = tk.Button(self.player2_buttons_frame, image=self.images["s_p"], command=lambda: self.set_player_move(2, 's'), bd=3, relief="solid", bg='#ff0000')
        self.player2_scissors_button.grid(row=0, column=2, padx=10, pady=5)

        self.player2_lizard_button = tk.Button(self.player2_buttons_frame, image=self.images["l_p"], command=lambda: self.set_player_move(2, 'l'), bd=3, relief="solid", bg='#ff0000')
        self.player2_lizard_button.grid(row=0, column=3, padx=10, pady=5)

        self.player2_spock_button = tk.Button(self.player2_buttons_frame, image=self.images["sp_p"], command=lambda: self.set_player_move(2, 'sp'), bd=3, relief="solid", bg='#ff0000')
        self.player2_spock_button.grid(row=0, column=4, padx=10, pady=5)

        # AI Move Display (only in Human vs AI mode)
        self.ai_move_label = tk.Label(self.game_frame, text="AI's Move:", font=("Palatino Linotype", 18, "bold"), bg='#0b034e', fg='#ff8080', anchor='w')
        self.ai_move_image_label = tk.Label(self.game_frame, bg='#0b034e', bd=3, relief="solid")

        # Result label inside white-bordered box
        self.result_label = tk.Label(self.game_frame, text="", font=("Palatino Linotype", 22, "bold"), bg='#ffffff', fg='#ff8080', bd=3, relief="solid", padx=10, pady=10)

        # Score tracking
        self.score_label = tk.Label(self.game_frame, font=("Palatino Linotype", 20, "bold"), bg="#0b034e", fg="#ffffff", bd=3, relief="solid", padx=10, pady=10)

        # Reset button
        self.reset_button = tk.Button(self.game_frame, text="Reset Game", font=("Palatino Linotype", 16, "bold"), bg='#ff8080', fg='#ffffff', command=self.reset_game)

    def load_image(self, filepath):
        try:
            return ImageTk.PhotoImage(Image.open(filepath))
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return ImageTk.PhotoImage(Image.new('RGB', (100, 100), color=(200, 200, 200)))

    def start_game(self, mode):
        self.mode = mode
        self.start_frame.pack_forget()
        self.game_frame.pack()
        self.player1_label.pack(pady=5, anchor='w')
        self.player1_buttons_frame.pack(pady=10)
        
        if self.mode == 1:  # Human vs Human
            self.player2_label.pack(pady=5, anchor='w')
            self.player2_buttons_frame.pack(pady=10)
            self.ai_move_label.pack_forget()
            self.ai_move_image_label.pack_forget()
        else:  # Human vs AI
            self.player2_label.pack_forget()
            self.player2_buttons_frame.pack_forget()
            self.ai_move_label.pack(pady=5, anchor='w')
            self.ai_move_image_label.pack(pady=5)
        
        self.result_label.pack(pady=10)
        self.score_label.pack(pady=10)
        self.reset_button.pack(pady=10)
        self.update_score()

    def set_player_move(self, player, move):
        if player == 1:
            self.player1_move = move
        elif player == 2:
            self.player2_move = move
        
        if self.mode == 1 and self.player1_move is not None and self.player2_move is not None:
            self.determine_winner_human_vs_human()
        elif self.mode == 2 and self.player1_move is not None:
            self.determine_winner_human_vs_ai()

    def determine_winner_human_vs_human(self):
        result = self.determine_winner(self.player1_move, self.player2_move)
        self.result_label.config(text=result)
        self.update_score()
        self.reset_moves()

    def determine_winner_human_vs_ai(self):
        self.player2_move = random.choice(['r', 'p', 's', 'l', 'sp'])
        self.ai_move_image_label.config(image=self.images[f"{self.player2_move}_p"])
        result = self.determine_winner(self.player1_move, self.player2_move)
        self.result_label.config(text=result)
        self.update_score()
        self.reset_moves()

    def determine_winner(self, player1, player2):
        if player1 == player2:
            return "It's a tie!"
        elif (player1 == 'r' and (player2 == 's' or player2 == 'l')) or \
             (player1 == 'p' and (player2 == 'r' or player2 == 'sp')) or \
             (player1 == 's' and (player2 == 'p' or player2 == 'l')) or \
             (player1 == 'l' and (player2 == 'sp' or player2 == 'p')) or \
             (player1 == 'sp' and (player2 == 's' or player2 == 'r')):
            return "Player 1 wins!"
        else:
            return "Player 2 wins!" if self.mode == 1 else "AI wins!"

    def update_score(self):
        if self.mode == 1:
            self.score_label.config(text=f"Player 1: {self.player1_score}  |  Player 2: {self.player2_score}")
        else:
            self.score_label.config(text=f"Player 1: {self.player1_score}  |  AI: {self.player2_score}")

    def reset_game(self):
        self.player1_score = 0
        self.player2_score = 0
        self.reset_moves()
        self.result_label.config(text="")
        self.ai_move_image_label.config(image="")
        self.update_score()

    def reset_moves(self):
        self.player1_move = None
        self.player2_move = None

if __name__ == "__main__":
    root = tk.Tk()
    game = RPSLSGame(root, img_dir="C:/Users/hitub/OneDrive/Desktop/coding/rpsls")
    root.mainloop()