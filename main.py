import tkinter as tk
from game.gui import MinesweeperGUI
from game.constants import Colors

def main():
    root = tk.Tk()
    root.configure(bg=Colors.BACKGROUND)
    
    # Center window on screen
    window_width = 800  # Increased width for leaderboard
    window_height = 800  # Increased height for auth and leaderboard
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    game = MinesweeperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()