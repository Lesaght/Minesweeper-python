import tkinter as tk
from .constants import Colors, GameConfig

class ModernFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        bg = kwargs.pop('bg', Colors.SURFACE)
        super().__init__(master, bg=bg, **kwargs)
        
        # Add subtle shadow effect
        self.shadow = tk.Frame(self, bg=Colors.BORDER)
        self.shadow.place(x=2, y=2, relwidth=1, relheight=1)
        self.lift()

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        bg = kwargs.pop('bg', Colors.PRIMARY)
        fg = kwargs.pop('fg', Colors.SURFACE)
        font = kwargs.pop('font', GameConfig.BUTTON_FONT)
        relief = kwargs.pop('relief', GameConfig.BUTTON_RELIEF)
        
        super().__init__(
            master,
            bg=bg,
            fg=fg,
            font=font,
            relief=relief,
            activebackground=self._darken_color(bg),
            activeforeground=fg,
            borderwidth=0,
            padx=20,
            pady=10,
            **kwargs
        )
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _darken_color(self, hex_color):
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        darkened = tuple(max(0, c - 20) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'
    
    def _on_enter(self, event):
        self.configure(bg=self._darken_color(self['bg']))
    
    def _on_leave(self, event):
        self.configure(bg=self['bg'])

class ModernEntry(tk.Entry):
    def __init__(self, master, placeholder="", **kwargs):
        super().__init__(
            master,
            font=GameConfig.BUTTON_FONT,
            relief=GameConfig.BUTTON_RELIEF,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_PRIMARY,
            insertbackground=Colors.TEXT_PRIMARY,
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_color = Colors.TEXT_SECONDARY
        self.default_fg_color = Colors.TEXT_PRIMARY
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self._on_focus_out(None)
    
    def _on_focus_in(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete(0, tk.END)
            self['fg'] = self.default_fg_color
    
    def _on_focus_out(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

class GameCell(tk.Button):
    def __init__(self, master, x, y, **kwargs):
        super().__init__(
            master,
            width=2,
            height=1,
            font=GameConfig.CELL_FONT,
            relief=GameConfig.BUTTON_RELIEF,
            bg=Colors.UNREVEALED_CELL,
            borderwidth=GameConfig.BORDER_WIDTH,
            **kwargs
        )
        
        self.x = x
        self.y = y
        self.revealed = False
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        if not self.revealed and self['state'] != 'disabled':
            self.configure(bg=Colors.HOVER)
    
    def _on_leave(self, event):
        if not self.revealed and self['state'] != 'disabled':
            self.configure(bg=Colors.UNREVEALED_CELL)
    
    def reveal(self, is_mine=False, neighbor_count=0):
        self.revealed = True
        self.configure(
            relief="sunken",
            state="disabled",
            bg=Colors.MINE if is_mine else Colors.REVEALED_CELL
        )
        
        if is_mine:
            self.configure(text=GameConfig.MINE_SYMBOL)
        elif neighbor_count > 0:
            self.configure(
                text=str(neighbor_count),
                fg=Colors.NUMBERS.get(neighbor_count)
            )

class StatsPanel(ModernFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.time_label = tk.Label(
            self,
            text=f"{GameConfig.TIMER_SYMBOL} Time: 0",
            font=GameConfig.STATS_FONT,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_SECONDARY
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.mines_label = tk.Label(
            self,
            text=f"{GameConfig.MINE_COUNT_SYMBOL} Mines: 0",
            font=GameConfig.STATS_FONT,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_SECONDARY
        )
        self.mines_label.pack(side=tk.RIGHT, padx=10)
    
    def update_time(self, seconds):
        self.time_label.configure(
            text=f"{GameConfig.TIMER_SYMBOL} Time: {seconds}"
        )
    
    def update_mines(self, count):
        self.mines_label.configure(
            text=f"{GameConfig.MINE_COUNT_SYMBOL} Mines: {count}"
        )