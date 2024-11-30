import tkinter as tk
from tkinter import messagebox
from .board import Board
from .constants import Colors, GameConfig
from .components import ModernFrame, ModernButton, GameCell, StatsPanel
from .auth import AuthFrame
from .leaderboard import LeaderboardFrame
from .database import Database

class MinesweeperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title(GameConfig.TITLE)
        self.master.configure(bg=Colors.BACKGROUND)
        self.master.minsize(GameConfig.MIN_WIDTH, GameConfig.MIN_HEIGHT)
        
        # Initialize database
        self.database = Database()
        
        # User state
        self.current_user_id = None
        self.current_username = None
        
        # Game settings
        self.width = GameConfig.DEFAULT_WIDTH
        self.height = GameConfig.DEFAULT_HEIGHT
        self.num_mines = GameConfig.DEFAULT_MINES
        self.time_count = 0
        self.timer_running = False
        
        self._setup_auth()
    
    def _setup_auth(self):
        self.auth_frame = AuthFrame(
            self.master,
            self.database,
            self._on_auth_success
        )
        self.auth_frame.pack(expand=True, fill=tk.BOTH)
    
    def _on_auth_success(self, user_id, username):
        self.current_user_id = user_id
        self.current_username = username
        self.auth_frame.destroy()
        self._setup_ui()
        self._start_new_game()
    
    def _setup_ui(self):
        # Main container
        self.main_container = ModernFrame(
            self.master,
            padx=20,
            pady=20
        )
        self.main_container.pack(expand=True, fill=tk.BOTH)
        
        # Header frame
        header_frame = ModernFrame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title and welcome message
        tk.Label(
            header_frame,
            text=f"Welcome, {self.current_username}!",
            font=GameConfig.HEADER_FONT,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_PRIMARY
        ).pack(side=tk.LEFT, padx=10)
        
        # Logout button
        ModernButton(
            header_frame,
            text="Logout",
            command=self._handle_logout,
            bg=Colors.SECONDARY
        ).pack(side=tk.RIGHT, padx=10)
        
        # Stats panel
        self.stats_panel = StatsPanel(self.main_container)
        self.stats_panel.pack(fill=tk.X, padx=10, pady=10)
        
        # Game board frame
        self.game_frame = ModernFrame(
            self.main_container,
            relief=GameConfig.FRAME_RELIEF,
            borderwidth=GameConfig.BORDER_WIDTH
        )
        self.game_frame.pack(padx=10, pady=10)
        
        # Control panel
        self.control_panel = ModernFrame(
            self.main_container,
            pady=10
        )
        self.control_panel.pack(fill=tk.X)
        
        # New Game button
        ModernButton(
            self.control_panel,
            text="New Game",
            command=self._start_new_game,
            bg=Colors.SUCCESS
        ).pack(side=tk.LEFT, padx=10)
        
        # Leaderboard
        self.leaderboard = LeaderboardFrame(
            self.main_container,
            self.database
        )
        self.leaderboard.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.buttons = []
    
    def _handle_logout(self):
        self.main_container.destroy()
        self._setup_auth()
    
    def _start_new_game(self):
        self.board = Board(self.width, self.height, self.num_mines)
        self._reset_timer()
        self._create_board()
        self.stats_panel.update_mines(self.num_mines)
    
    def _create_board(self):
        # Clear existing buttons
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons.clear()
        
        # Create new buttons
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = GameCell(
                    self.game_frame,
                    x, y,
                    command=lambda x=x, y=y: self._handle_click(x, y)
                )
                cell.grid(
                    row=y,
                    column=x,
                    padx=GameConfig.CELL_PADDING,
                    pady=GameConfig.CELL_PADDING
                )
                cell.bind(
                    '<Button-3>',
                    lambda e, x=x, y=y: self._handle_right_click(x, y)
                )
                row.append(cell)
            self.buttons.append(row)
    
    def _handle_click(self, x, y):
        if not self.timer_running:
            self._start_timer()
        
        self.board.reveal(x, y)
        self._update_display()
        self._check_game_state()
    
    def _handle_right_click(self, x, y):
        if self.board.toggle_flag(x, y):
            self._update_display()
    
    def _update_display(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board.grid[y][x]
                button = self.buttons[y][x]
                
                if cell.is_revealed:
                    button.reveal(
                        is_mine=cell.is_mine,
                        neighbor_count=cell.neighbor_mines
                    )
                elif cell.is_flagged:
                    button.configure(
                        text=GameConfig.FLAG_SYMBOL,
                        fg=Colors.FLAG
                    )
                else:
                    button.configure(
                        text="",
                        bg=Colors.UNREVEALED_CELL
                    )
    
    def _check_game_state(self):
        if self.board.game_over:
            self._stop_timer()
            if self.board.won:
                # Save score
                self.database.add_score(
                    self.current_user_id,
                    self.time_count,
                    self.num_mines,
                    f"{self.width}x{self.height}"
                )
                # Update leaderboard
                self.leaderboard.update_scores()
                messagebox.showinfo(
                    "Victory! 🎉",
                    f"Congratulations! You've won in {self.time_count} seconds!"
                )
            else:
                messagebox.showinfo(
                    "Game Over 💥",
                    "Oh no! You hit a mine!"
                )
            self._reveal_all()
    
    def _reveal_all(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board.grid[y][x]
                if cell.is_mine:
                    self.buttons[y][x].reveal(is_mine=True)
    
    def _start_timer(self):
        self.timer_running = True
        self._update_timer()
    
    def _stop_timer(self):
        self.timer_running = False
    
    def _reset_timer(self):
        self._stop_timer()
        self.time_count = 0
        self.stats_panel.update_time(0)
    
    def _update_timer(self):
        if self.timer_running:
            self.time_count += 1
            self.stats_panel.update_time(self.time_count)
            self.master.after(1000, self._update_timer)