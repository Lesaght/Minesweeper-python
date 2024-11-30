from tkinter import font

class Colors:
    # Modern color palette
    PRIMARY = "#2196F3"
    SECONDARY = "#FF4081"
    SUCCESS = "#4CAF50"
    WARNING = "#FFC107"
    DANGER = "#F44336"
    INFO = "#00BCD4"
    
    # UI Elements
    BACKGROUND = "#FAFAFA"
    SURFACE = "#FFFFFF"
    BORDER = "#E0E0E0"
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    
    # Game specific colors
    REVEALED_CELL = "#F5F5F5"
    UNREVEALED_CELL = "#FFFFFF"
    MINE = DANGER
    HOVER = "#E3F2FD"
    FLAG = WARNING
    NUMBERS = {
        1: "#1976D2",  # Blue
        2: "#388E3C",  # Green
        3: "#D32F2F",  # Red
        4: "#7B1FA2",  # Purple
        5: "#C2185B",  # Pink
        6: "#00796B",  # Teal
        7: "#424242",  # Dark Gray
        8: "#FF5722"   # Deep Orange
    }

class GameConfig:
    # Window configuration
    TITLE = "Modern Minesweeper"
    MIN_WIDTH = 600
    MIN_HEIGHT = 700
    
    # Game settings
    DEFAULT_WIDTH = 10
    DEFAULT_HEIGHT = 10
    DEFAULT_MINES = 10
    
    # UI Elements
    CELL_SIZE = 45
    CELL_PADDING = 2
    ANIMATION_SPEED = 150  # milliseconds
    
    # Fonts
    TITLE_FONT = ("Helvetica", 24, "bold")
    HEADER_FONT = ("Helvetica", 18, "bold")
    CELL_FONT = ("Helvetica", 16, "bold")
    BUTTON_FONT = ("Helvetica", 14)
    STATS_FONT = ("Helvetica", 12)
    
    # Symbols
    MINE_SYMBOL = "💣"
    FLAG_SYMBOL = "🚩"
    TIMER_SYMBOL = "⏱"
    MINE_COUNT_SYMBOL = "💣"
    
    # Styles
    BUTTON_RELIEF = "flat"
    FRAME_RELIEF = "flat"
    BORDER_WIDTH = 1
    CORNER_RADIUS = 8  # pixels