import tkinter as tk
from tkinter import ttk
from .components import ModernFrame
from .constants import Colors, GameConfig

class LeaderboardFrame(ModernFrame):
    def __init__(self, master, database, **kwargs):
        super().__init__(master, **kwargs)
        self.database = database
        self._setup_ui()
        self.update_scores()
    
    def _setup_ui(self):
        # Title
        tk.Label(
            self,
            text="Top Scores",
            font=GameConfig.HEADER_FONT,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_PRIMARY
        ).pack(pady=(10, 20))
        
        # Treeview for scores
        self.tree = ttk.Treeview(
            self,
            columns=("rank", "player", "time", "mines", "board", "date"),
            show="headings",
            height=10
        )
        
        # Configure columns
        self.tree.heading("rank", text="#")
        self.tree.heading("player", text="Player")
        self.tree.heading("time", text="Time")
        self.tree.heading("mines", text="Mines")
        self.tree.heading("board", text="Board")
        self.tree.heading("date", text="Date")
        
        # Column widths
        self.tree.column("rank", width=50)
        self.tree.column("player", width=100)
        self.tree.column("time", width=80)
        self.tree.column("mines", width=80)
        self.tree.column("board", width=100)
        self.tree.column("date", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
    
    def update_scores(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get and display scores
        scores = self.database.get_top_scores()
        for i, score in enumerate(scores, 1):
            username, time, mines, board_size, date = score
            self.tree.insert(
                "",
                tk.END,
                values=(
                    f"#{i}",
                    username,
                    f"{time}s",
                    mines,
                    board_size,
                    date.split(".")[0]  # Remove microseconds
                )
            )