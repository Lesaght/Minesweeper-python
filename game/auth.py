import tkinter as tk
from tkinter import messagebox
from .components import ModernFrame, ModernButton, ModernEntry
from .constants import Colors, GameConfig

class AuthFrame(ModernFrame):
    def __init__(self, master, database, on_auth_success, **kwargs):
        super().__init__(master, **kwargs)
        self.database = database
        self.on_auth_success = on_auth_success
        self._setup_ui()
    
    def _setup_ui(self):
        # Login Frame
        self.login_frame = ModernFrame(self)
        self.login_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            self.login_frame,
            text="Login",
            font=GameConfig.HEADER_FONT,
            bg=Colors.SURFACE,
            fg=Colors.TEXT_PRIMARY
        ).pack(pady=(0, 20))
        
        # Username
        self.username_entry = ModernEntry(
            self.login_frame,
            placeholder="Username"
        )
        self.username_entry.pack(pady=5, fill=tk.X)
        
        # Password
        self.password_entry = ModernEntry(
            self.login_frame,
            placeholder="Password",
            show="•"
        )
        self.password_entry.pack(pady=5, fill=tk.X)
        
        # Login Button
        ModernButton(
            self.login_frame,
            text="Login",
            command=self._handle_login,
            bg=Colors.PRIMARY
        ).pack(pady=10)
        
        # Register Button
        ModernButton(
            self.login_frame,
            text="Register",
            command=self._handle_register,
            bg=Colors.SECONDARY
        ).pack(pady=5)
    
    def _handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        user_id = self.database.verify_user(username, password)
        if user_id:
            self.on_auth_success(user_id, username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def _handle_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        if self.database.add_user(username, password):
            messagebox.showinfo("Success", "Registration successful! You can now login.")
        else:
            messagebox.showerror("Error", "Username already exists")