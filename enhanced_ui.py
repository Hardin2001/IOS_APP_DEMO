import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageTk
import os
from pathlib import Path

# High-quality rendering settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Enable high-DPI support
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class DynamicIsland(tk.Canvas):
    """Dynamic Island component for iPhone-like experience"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(highlightthickness=0, bg="black")
        
        # Island properties
        self.island_width = 120
        self.island_height = 32
        self.corner_radius = 16
        self.is_expanded = False
        
        self.draw_island()
        self.bind("<Button-1>", self.toggle_island)
        
    def draw_island(self):
        self.delete("all")
        
        # Calculate position (centered)
        canvas_width = self.winfo_width() or 200
        x = (canvas_width - self.island_width) // 2
        y = 8
        
        # Draw rounded rectangle for island
        self.create_rounded_rect(
            x, y, x + self.island_width, y + self.island_height,
            radius=self.corner_radius,
            fill="#1C1C1E",
            outline=""
        )
        
        # Add content based on state
        if self.is_expanded:
            # Expanded state - show more info
            self.create_text(
                canvas_width // 2, y + self.island_height // 2,
                text="HUD Control Active",
                fill="white",
                font=("Segoe UI", 10, "bold")
            )
        else:
            # Compact state - show indicator
            dot_x = canvas_width // 2
            dot_y = y + self.island_height // 2
            self.create_oval(
                dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3,
                fill="#32D74B", outline=""
            )
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Create a rounded rectangle"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def toggle_island(self, event=None):
        """Toggle island expanded state"""
        self.is_expanded = not self.is_expanded
        if self.is_expanded:
            self.island_width = 200
            self.island_height = 40
        else:
            self.island_width = 120
            self.island_height = 32
        
        self.after(10, self.draw_island)

class RoundedFrame(ctk.CTkFrame):
    """Enhanced frame with better anti-aliasing"""
    def __init__(self, parent, corner_radius=12, **kwargs):
        super().__init__(parent, corner_radius=corner_radius, **kwargs)
        
        # Enhanced corner radius for smoother curves
        self.configure(
            corner_radius=corner_radius,
            border_width=0,
            fg_color=("#2b2b2b", "#2b2b2b")
        )

class PhoneFrame(tk.Frame):
    """Phone-like frame with curved edges"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="black")
        
        # Create rounded mask
        self.create_phone_mask()
        
    def create_phone_mask(self):
        """Create phone-like rounded corners"""
        # This will be enhanced with PIL for better curves
        self.configure(relief="flat", bd=0)

class EnhancedSwitch(ctk.CTkSwitch):
    """Enhanced switch with better rendering"""
    def __init__(self, parent, callback=None, **kwargs):
        self._callback = callback
        super().__init__(parent, command=self._handle_toggle, **kwargs)
        
        # Enhanced visual properties
        self.configure(
            width=52,
            height=26,
            switch_width=50,
            switch_height=24,
            corner_radius=13,
            border_width=0,
            fg_color=("#3a3a3c", "#3a3a3c"),
            progress_color=("#32D74B", "#32D74B"),
            button_color=("#FFFFFF", "#FFFFFF"),
            text=""
        )
        
    def _handle_toggle(self):
        if self._callback:
            self._callback(self.get() == 1)

class EnhancedSettingItem(RoundedFrame):
    """Enhanced setting item with better anti-aliasing"""
    def __init__(self, parent, title, has_switch=True, has_arrow=False, 
                 status_text="", callback=None, **kwargs):
        super().__init__(parent, corner_radius=14, **kwargs)
        
        self.title = title
        self.has_switch = has_switch
        self.has_arrow = has_arrow
        self.status_text = status_text
        self.callback = callback
        self.is_active = False
        
        self.configure(height=56, fg_color=("#2b2b2b", "#2b2b2b"))
        self.grid_propagate(False)
        self.create_widgets()
        
    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        
        # Title with enhanced font rendering
        self.title_label = ctk.CTkLabel(
            self, 
            text=self.title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, padx=(20, 10), pady=14, sticky="w")
        
        if self.status_text:
            self.status_label = ctk.CTkLabel(
                self,
                text=self.status_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#8E8E93", "#8E8E93")
            )
            self.status_label.grid(row=0, column=2, padx=(0, 15), pady=14, sticky="e")
        
        if self.has_switch:
            self.switch = EnhancedSwitch(self, callback=self.on_switch_change)
            self.switch.grid(row=0, column=3, padx=(0, 20), pady=14, sticky="e")
        elif self.has_arrow:
            arrow_label = ctk.CTkLabel(
                self, text="›", font=ctk.CTkFont(size=20, weight="bold"),
                text_color=("#8E8E93", "#8E8E93")
            )
            arrow_label.grid(row=0, column=3, padx=(0, 20), pady=14, sticky="e")
        
    def on_switch_change(self, is_on):
        self.is_active = is_on
        if self.callback:
            self.callback(self.title, is_on)

class EnhancedHUDApp:
    def __init__(self, root):
        self.root = root
        self.setup_enhanced_window()
        
        # Feature configuration
        self.features = [
            {"title": "Rear Traffic Alert", "type": "switch"},
            {"title": "Headlight Status", "type": "switch"},
            {"title": "Turn Signals", "type": "switch"},
            {"title": "Navigation", "type": "switch"},
            {"title": "Speed Limits", "type": "switch"},
            {"title": "Takeover Alerts", "type": "switch"},
            {"title": "Lane Departure", "type": "switch"},
            {"title": "Autopilot Status", "type": "switch"},
            {"title": "Gear Position", "type": "switch"},
            {"title": "Battery Range", "type": "switch"},
            {"title": "Speed Display", "type": "switch"}
        ]
        
        self.feature_states = {feature["title"]: False for feature in self.features}
        self.setting_items = {}
        
        self.themes = {
            "Dark": {"name": "Dark", "color": "#007AFF"},
            "Light": {"name": "Light", "color": "#007AFF"},
            "Nature": {"name": "Nature", "color": "#32D74B"},
            "Cyber": {"name": "Cyber", "color": "#FF0080"}
        }
        
        self.current_theme = "Dark"
        
        self.create_enhanced_interface()
        
    def setup_enhanced_window(self):
        """Setup enhanced window with phone-like appearance"""
        self.root.title("HUD Settings")
        self.root.geometry("440x780")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)
        
        # Create phone frame with curved edges
        self.phone_frame = PhoneFrame(self.root)
        self.phone_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
    def create_enhanced_interface(self):
        """Create enhanced interface with Dynamic Island"""
        # Dynamic Island at top
        self.dynamic_island = DynamicIsland(
            self.phone_frame,
            width=440,
            height=50,
            bg="black"
        )
        self.dynamic_island.pack(fill="x", pady=(5, 0))
        
        # Main scrollable content
        self.main_frame = ctk.CTkScrollableFrame(
            self.phone_frame,
            corner_radius=0,
            fg_color=("#000000", "#000000"),
            scrollbar_button_color=("#333333", "#333333"),
            scrollbar_button_hover_color=("#555555", "#555555")
        )
        self.main_frame.pack(fill="both", expand=True, padx=8, pady=(0, 5))
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.create_enhanced_header()
        self.create_enhanced_status_section()
        self.create_enhanced_settings_section()
        self.create_enhanced_theme_section()
        self.create_enhanced_sync_section()
        
    def create_enhanced_header(self):
        """Create enhanced header"""
        header_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=0,
            fg_color="transparent",
            height=70
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Settings",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF")
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(10, 0))
        
    def create_enhanced_status_section(self):
        """Create enhanced status section"""
        status_container = RoundedFrame(
            self.main_frame,
            corner_radius=16,
            fg_color=("#1c1c1e", "#1c1c1e")
        )
        status_container.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 15))
        
        version_item = EnhancedSettingItem(
            status_container, 
            "Your Drive is up to date",
            has_switch=False, 
            status_text="1.1.22"
        )
        version_item.pack(fill="x", padx=0, pady=0)
        
    def create_enhanced_settings_section(self):
        """Create enhanced settings section"""
        settings_container = RoundedFrame(
            self.main_frame,
            corner_radius=16,
            fg_color=("#1c1c1e", "#1c1c1e")
        )
        settings_container.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        for i, feature in enumerate(self.features):
            if feature["type"] == "switch":
                item = EnhancedSettingItem(
                    settings_container, 
                    feature["title"],
                    has_switch=True, 
                    callback=self.on_feature_change
                )
                item.pack(fill="x", padx=0, pady=(0, 1))
                self.setting_items[feature["title"]] = item
                
        # Separator
        separator = ctk.CTkFrame(
            settings_container,
            height=1,
            fg_color=("#39393D", "#39393D")
        )
        separator.pack(fill="x", padx=20, pady=8)
        
        # Additional settings
        nav_item = EnhancedSettingItem(
            settings_container,
            "Navigation settings",
            has_switch=False, 
            has_arrow=True
        )
        nav_item.pack(fill="x", padx=0, pady=(0, 1))
        
        units_item = EnhancedSettingItem(
            settings_container,
            "Units",
            has_switch=False, 
            has_arrow=True
        )
        units_item.pack(fill="x", padx=0, pady=0)
        
    def create_enhanced_theme_section(self):
        """Create enhanced theme section"""
        theme_container = RoundedFrame(
            self.main_frame,
            corner_radius=16,
            fg_color=("#1c1c1e", "#1c1c1e")
        )
        theme_container.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))
        
        theme_title = ctk.CTkLabel(
            theme_container,
            text="Theme",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF")
        )
        theme_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        theme_buttons_frame = ctk.CTkFrame(theme_container, fg_color="transparent")
        theme_buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.theme_buttons = {}
        for i, theme_name in enumerate(self.themes.keys()):
            btn = ctk.CTkButton(
                theme_buttons_frame,
                text=theme_name,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda t=theme_name: self.change_theme(t),
                corner_radius=10,
                height=38,
                fg_color=("#39393d", "#39393d"),
                hover_color=("#4a4a4d", "#4a4a4d"),
                text_color=("#FFFFFF", "#FFFFFF")
            )
            
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=(0, 8) if col == 0 else (8, 0), 
                    pady=(0, 8) if row == 0 else (8, 0), sticky="ew")
            
            theme_buttons_frame.grid_columnconfigure(col, weight=1)
            self.theme_buttons[theme_name] = btn
            
        self.update_theme_buttons()
        
    def create_enhanced_sync_section(self):
        """Create enhanced sync section"""
        sync_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        sync_frame.grid(row=4, column=0, sticky="ew", padx=15, pady=15)
        
        self.sync_button = ctk.CTkButton(
            sync_frame,
            text="Sync Settings",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.sync_settings,
            corner_radius=14,
            height=52,
            fg_color=("#007AFF", "#007AFF"),
            hover_color=("#0051D5", "#0051D5"),
            text_color=("#FFFFFF", "#FFFFFF")
        )
        self.sync_button.pack(fill="x", pady=(0, 12))
        
        self.status_label = ctk.CTkLabel(
            sync_frame,
            text="Ready",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#8E8E93", "#8E8E93")
        )
        self.status_label.pack()
        
    def on_feature_change(self, feature_name, is_on):
        """Handle feature state change"""
        self.feature_states[feature_name] = is_on
        status_text = "enabled" if is_on else "disabled"
        self.status_label.configure(text=f"{feature_name} {status_text} (pending sync)")
        
    def change_theme(self, theme_name):
        """Change theme setting for target device"""
        self.current_theme = theme_name
        self.update_theme_buttons()
        self.status_label.configure(text=f"Theme set to {theme_name} for target device")
        
    def update_theme_buttons(self):
        """Update theme button styles"""
        for theme_name, btn in self.theme_buttons.items():
            if theme_name == self.current_theme:
                theme_color = self.themes[theme_name]["color"]
                btn.configure(fg_color=theme_color, hover_color=theme_color)
            else:
                btn.configure(
                    fg_color=("#39393d", "#39393d"),
                    hover_color=("#4a4a4d", "#4a4a4d")
                )
        
    def sync_settings(self):
        """Sync settings with enhanced feedback"""
        self.sync_button.configure(text="Syncing...", state="disabled")
        
        # Animate Dynamic Island
        self.dynamic_island.toggle_island()
        
        self.root.update()
        self.root.after(1500, self.sync_complete)
        
    def sync_complete(self):
        """Sync complete with enhanced feedback"""
        self.sync_button.configure(text="Sync Settings", state="normal")
        
        # Reset Dynamic Island
        if self.dynamic_island.is_expanded:
            self.dynamic_island.toggle_island()
        
        active_features = [name for name, status in self.feature_states.items() if status]
        
        if active_features:
            self.status_label.configure(text=f"Synced to device - {len(active_features)} features enabled")
        else:
            self.status_label.configure(text="Synced to device - All features disabled")

def main():
    """Main function with enhanced rendering"""
    root = ctk.CTk()
    
    # Enable high-quality rendering
    try:
        root.tk.call('tk', 'scaling', 2.0)  # High-DPI scaling
    except:
        pass
    
    app = EnhancedHUDApp(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()