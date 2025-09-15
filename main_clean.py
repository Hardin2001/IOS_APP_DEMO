import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkFont
import math
import os
from pathlib import Path

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Load custom fonts
def load_custom_fonts():
    """Use modern rounded system fonts"""
    # Use system fonts that are more rounded and modern
    fonts = {
        "regular": "Segoe UI Variable",    # Windows 11's modern variable font
        "bold": "Segoe UI Variable",       # Same font family for consistency
        "medium": "Segoe UI Variable"      # Same font family
    }
    
    # Fallback to regular Segoe UI if variable version not available
    fallback_fonts = {
        "regular": "Segoe UI",
        "bold": "Segoe UI",  
        "medium": "Segoe UI"
    }
    
    # Test if fonts are available, otherwise use fallback
    try:
        available_fonts = tkFont.families()
        
        for weight in fonts:
            if fonts[weight] not in available_fonts:
                fonts[weight] = fallback_fonts[weight]
                
    except Exception:
        fonts = fallback_fonts
    
    return fonts

# Load fonts at startup
CUSTOM_FONTS = load_custom_fonts()

class ModernSwitch(ctk.CTkSwitch):
    """Modern customtkinter switch control with proper callbacks"""
    def __init__(self, parent, text="", callback=None, **kwargs):
        # Store callback before calling super().__init__
        self._callback = callback
        super().__init__(parent, text=text, command=self._handle_toggle, **kwargs)
        
        # Configure switch appearance
        self.configure(
            width=50,
            height=24,
            switch_width=48,
            switch_height=22,
            corner_radius=12,
            border_width=0,
            fg_color=("#939393", "#525252"),  # Gray when off
            progress_color=("#32D74B", "#32D74B"),  # Green when on
            button_color=("#FFFFFF", "#FFFFFF"),
            text=""
        )
        
    def _handle_toggle(self):
        """Internal toggle handler"""
        if self._callback:
            self._callback(self.get() == 1)
    
    def set_state(self, state):
        """Set switch state programmatically"""
        if state:
            self.select()
        else:
            self.deselect()
    
    def get_state(self):
        """Get current switch state"""
        return self.get() == 1

class SettingItem(ctk.CTkFrame):
    """Modern setting item widget using customtkinter"""
    def __init__(self, parent, title, has_switch=True, has_arrow=False, 
                 status_text="", callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.has_switch = has_switch
        self.has_arrow = has_arrow
        self.status_text = status_text
        self.callback = callback
        self.is_active = False
        
        # Configure frame appearance - more compact
        self.configure(
            corner_radius=12,
            fg_color=("#2b2b2b", "#2b2b2b"),
            border_width=0,
            height=55  # Reduced height for better spacing
        )
        
        self.grid_propagate(False)
        self.create_widgets()
        
    def create_widgets(self):
        # Configure grid weights
        self.grid_columnconfigure(1, weight=1)
        
        # Title label with rounded font - bold
        self.title_label = ctk.CTkLabel(
            self, 
            text=self.title,
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=16, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF"),
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, padx=(20, 10), pady=12, sticky="w")  # Reduced padding
        
        if self.status_text:
            self.status_label = ctk.CTkLabel(
                self, 
                text=self.status_text,
                font=ctk.CTkFont(family=CUSTOM_FONTS.get("regular", "Segoe UI"), size=12),
                text_color=("#999999", "#999999"),
                anchor="w"
            )
            self.status_label.grid(row=1, column=0, padx=(20, 10), pady=(0, 5), sticky="w")
        
        if self.has_switch:
            self.switch = ModernSwitch(self, callback=self.on_switch_change)
            self.switch.grid(row=0, column=1, padx=(10, 20), pady=12, sticky="e")
        elif self.has_arrow:
            # Create arrow indicator
            pass
        
    def on_switch_change(self, value):
        """Handle switch state change"""
        if hasattr(self, 'switch'):
            self.is_active = value
            if self.callback:
                self.callback(self.title, value)

class HUDApp:
    def __init__(self, root):
        self.root = root
        self.is_closing = False  # Add flag to track closing state
        self.setup_window()
        
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
        
        # Theme configurations optimized for customtkinter
        self.themes = {
            "Dark": {
                "appearance_mode": "dark",
                "color_theme": "blue"
            },
            "Light": {
                "appearance_mode": "light", 
                "color_theme": "blue"
            },
            "Nature": {
                "appearance_mode": "dark",
                "color_theme": "green"
            },
            "Cyber": {
                "appearance_mode": "system",
                "color_theme": "dark-blue"
            }
        }
        
        self.current_theme = "Dark"
        
        self.create_interface()
        
    def setup_window(self):
        """Setup window properties with enhanced rendering"""
        self.root.title("HUD Settings")
        # Enhanced dimensions with better proportions
        self.root.geometry("440x780")
        self.root.resizable(False, False)
        
        # Configure window appearance with anti-aliasing hints
        self.root.configure(bg="#000000")
        
        # Set up proper window closing protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Enable high-DPI support if available
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
        
    def create_interface(self):
        """Create main interface with customtkinter"""
        # Main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            corner_radius=0,
            fg_color=("#000000", "#000000"),
            scrollbar_button_color=("#333333", "#333333"),
            scrollbar_button_hover_color=("#555555", "#555555")
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Create interface sections
        self.create_header()
        self.create_status_section()
        self.create_settings_section()
        self.create_theme_section()
        self.create_sync_section()
        
    def create_header(self):
        """Create header with title"""
        header_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=0,
            fg_color="transparent",
            height=80
        )
        header_frame.pack(fill="x", padx=0, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Title - bold and prominent
        title_label = ctk.CTkLabel(
            header_frame,
            text="HUD Settings",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=28, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF")
        )
        title_label.pack(expand=True)
        
    def create_status_section(self):
        """Create status section"""
        status_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=12,
            fg_color=("#1a1a1a", "#1a1a1a"),
            height=60
        )
        status_frame.pack(fill="x", padx=20, pady=10)
        status_frame.pack_propagate(False)
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="Configure HUD display settings for target device",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("regular", "Segoe UI"), size=14),
            text_color=("#AAAAAA", "#AAAAAA")
        )
        status_label.pack(expand=True)
        
    def create_settings_section(self):
        """Create settings section with all HUD features"""
        # Settings container
        for i, feature in enumerate(self.features):
            setting_item = SettingItem(
                self.main_frame,
                title=feature["title"],
                has_switch=True,
                callback=self.on_feature_change
            )
            setting_item.pack(fill="x", padx=20, pady=2)
            self.setting_items[feature["title"]] = setting_item
        
    def create_theme_section(self):
        """Create theme selection section"""
        # Theme section header
        theme_header = ctk.CTkLabel(
            self.main_frame,
            text="Theme",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=18, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF"),
            anchor="w"
        )
        theme_header.pack(fill="x", padx=20, pady=(20, 10))
        
        # Theme buttons frame
        theme_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=12,
            fg_color=("#1a1a1a", "#1a1a1a")
        )
        theme_frame.pack(fill="x", padx=20, pady=5)
        
        # Theme buttons
        self.theme_buttons = {}
        for i, theme_name in enumerate(self.themes.keys()):
            btn = ctk.CTkButton(
                theme_frame,
                text=theme_name,
                font=ctk.CTkFont(family=CUSTOM_FONTS.get("medium", "Segoe UI"), size=14),
                corner_radius=8,
                height=35,
                command=lambda t=theme_name: self.change_theme(t)
            )
            btn.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            self.theme_buttons[theme_name] = btn
            
        # Configure grid weights
        for i in range(len(self.themes)):
            theme_frame.grid_columnconfigure(i, weight=1)
            
        self.update_theme_buttons()
        
    def create_sync_section(self):
        """Create sync section"""
        # Sync button
        self.sync_button = ctk.CTkButton(
            self.main_frame,
            text="Sync to Device",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=16, weight="bold"),
            corner_radius=12,
            height=50,
            fg_color=("#007AFF", "#007AFF"),
            hover_color=("#0051D5", "#0051D5"),
            command=self.sync_settings
        )
        self.sync_button.pack(fill="x", padx=20, pady=20)
        
        # Add some bottom spacing
        spacer = ctk.CTkFrame(
            self.main_frame,
            corner_radius=0,
            fg_color="transparent",
            height=50
        )
        spacer.pack(fill="x")
        
    def on_feature_change(self, feature_name, is_on):
        """Handle feature toggle"""
        self.feature_states[feature_name] = is_on
        print(f"{feature_name}: {'ON' if is_on else 'OFF'}")
        
    def change_theme(self, theme_name):
        """Change application theme"""
        self.current_theme = theme_name
        theme_config = self.themes[theme_name]
        ctk.set_appearance_mode(theme_config["appearance_mode"])
        ctk.set_default_color_theme(theme_config["color_theme"])
        self.update_theme_buttons()
        
    def update_theme_buttons(self):
        """Update theme button appearances"""
        for theme_name, button in self.theme_buttons.items():
            if theme_name == self.current_theme:
                button.configure(fg_color=("#007AFF", "#007AFF"))
            else:
                button.configure(fg_color=("#333333", "#333333"))
        
    def sync_settings(self):
        """Sync settings to device"""
        self.sync_button.configure(text="Syncing...", state="disabled")
        # Simulate sync process
        self.root.after(2000, self.sync_complete)
        
    def sync_complete(self):
        """Complete sync process"""
        self.sync_button.configure(text="Sync to Device", state="normal")
        print("Settings synced successfully!")

def main():
    # Create main window
    root = ctk.CTk()
    app = HUDApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()