import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
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
        import tkinter.font as tkFont
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
            fg_color=("#939393", "#525252"),  # off color
            progress_color=("#32D74B", "#32D74B"),  # on color
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
            height=55  # Reduced from 60 to 55
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
            # Status text
            self.status_label = ctk.CTkLabel(
                self,
                text=self.status_text,
                font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=14, weight="bold"),
                text_color=("#8E8E93", "#8E8E93")
            )
            self.status_label.grid(row=0, column=2, padx=(0, 15), pady=12, sticky="e")  # Reduced padding
        
        if self.has_switch:
            # Switch control
            self.switch = ModernSwitch(
                self, 
                callback=self.on_switch_change
            )
            self.switch.grid(row=0, column=3, padx=(0, 20), pady=12, sticky="e")  # Reduced padding
        elif self.has_arrow:
            # Arrow indicator
            arrow_label = ctk.CTkLabel(
                self,
                text="›",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=("#8E8E93", "#8E8E93")
            )
            arrow_label.grid(row=0, column=3, padx=(0, 20), pady=12, sticky="e")  # Reduced padding
        
    def on_switch_change(self):
        """Handle switch state change"""
        if hasattr(self, 'switch'):
            self.is_active = self.switch.get_state()
            if self.callback:
                self.callback(self.title, self.is_active)

class HUDApp:
    def __init__(self, root):
        self.root = root
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
        
        # Enable high-DPI support if available
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
            # Enable scaling for better rendering
            self.root.tk.call('tk', 'scaling', 1.5)
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
        
        # Configure grid
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.create_header()
        
        # Status section
        self.create_status_section()
        
        # Settings section
        self.create_settings_section()
        
        # Theme section
        self.create_theme_section()
        
        # Sync button
        self.create_sync_section()
        
    def create_header(self):
        """Create beautiful header section without back button"""
        header_frame = ctk.CTkFrame(
            self.main_frame,
            corner_radius=0,
            fg_color="transparent",
            height=80  # Reduced from 100 to 80
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 8))  # Reduced padding
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_propagate(False)
        
        # Title with premium font - centered and bold
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Settings",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=32, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF")
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(10, 0))
        
    def create_status_section(self):
        """Create status section with modern card design"""
        status_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=16,
            fg_color=("#1c1c1e", "#1c1c1e"),
            border_width=0
        )
        status_container.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        # Version info item
        version_item = SettingItem(
            status_container, 
            "Your Drive is up to date",
            has_switch=False, 
            has_arrow=False,
            status_text="1.1.22"
        )
        version_item.pack(fill="x", padx=0, pady=0)
        
    def create_settings_section(self):
        """Create settings section with beautiful cards"""
        settings_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=16,
            fg_color=("#1c1c1e", "#1c1c1e"),
            border_width=0
        )
        settings_container.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Create setting items for each feature
        for i, feature in enumerate(self.features):
            if feature["type"] == "switch":
                item = SettingItem(
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
        separator.pack(fill="x", padx=20, pady=10)
        
        # Additional settings with arrows
        nav_item = SettingItem(
            settings_container,
            "Navigation settings",
            has_switch=False, 
            has_arrow=True
        )
        nav_item.pack(fill="x", padx=0, pady=(0, 1))
        
        units_item = SettingItem(
            settings_container,
            "Units",
            has_switch=False, 
            has_arrow=True
        )
        units_item.pack(fill="x", padx=0, pady=0)
        
    def create_theme_section(self):
        """Create beautiful theme selection section"""
        theme_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=16,
            fg_color=("#1c1c1e", "#1c1c1e"),
            border_width=0
        )
        theme_container.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Theme title
        theme_title = ctk.CTkLabel(
            theme_container,
            text="Theme",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=18, weight="bold"),
            text_color=("#FFFFFF", "#FFFFFF")
        )
        theme_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Theme buttons frame
        theme_buttons_frame = ctk.CTkFrame(
            theme_container,
            fg_color="transparent"
        )
        theme_buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.theme_buttons = {}
        # Create theme buttons in a grid
        for i, theme_name in enumerate(self.themes.keys()):
            btn = ctk.CTkButton(
                theme_buttons_frame,
                text=theme_name,
                font=ctk.CTkFont(family=CUSTOM_FONTS.get("regular", "Segoe UI"), size=14, weight="bold"),
                command=lambda t=theme_name: self.change_theme(t),
                corner_radius=8,
                height=36,
                fg_color=("#39393d", "#39393d"),
                hover_color=("#4a4a4d", "#4a4a4d"),
                text_color=("#FFFFFF", "#FFFFFF")
            )
            
            # Arrange in 2x2 grid
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=(0, 8) if col == 0 else (8, 0), 
                    pady=(0, 8) if row == 0 else (8, 0), sticky="ew")
            
            theme_buttons_frame.grid_columnconfigure(col, weight=1)
            self.theme_buttons[theme_name] = btn
            
        self.update_theme_buttons()
        
    def create_sync_section(self):
        """Create sync section with modern button"""
        sync_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        sync_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=20)
        
        # Modern sync button
        self.sync_button = ctk.CTkButton(
            sync_frame,
            text="Sync Settings",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=18, weight="bold"),
            command=self.sync_settings,
            corner_radius=12,
            height=50,
            fg_color=("#007AFF", "#007AFF"),
            hover_color=("#0051D5", "#0051D5"),
            text_color=("#FFFFFF", "#FFFFFF")
        )
        self.sync_button.pack(fill="x", pady=(0, 15))
        
        # Status label - bold
        self.status_label = ctk.CTkLabel(
            sync_frame,
            text="Ready",
            font=ctk.CTkFont(family=CUSTOM_FONTS.get("bold", "Segoe UI"), size=14, weight="bold"),
            text_color=("#8E8E93", "#8E8E93")
        )
        self.status_label.pack()
        
    def on_feature_change(self, feature_name, is_on):
        """Handle feature state change"""
        self.feature_states[feature_name] = is_on
        status_text = "enabled" if is_on else "disabled"
        self.status_label.configure(text=f"{feature_name} {status_text} (pending sync)")
        
    def change_theme(self, theme_name):
        """Change theme setting for target device (no visual change to current app)"""
        self.current_theme = theme_name
        
        # Only update button styles and status - no actual theme change to app
        self.update_theme_buttons()
        self.status_label.configure(text=f"Theme set to {theme_name} for target device")
        
    def update_theme_buttons(self):
        """Update theme button styles"""
        for theme_name, btn in self.theme_buttons.items():
            if theme_name == self.current_theme:
                btn.configure(
                    fg_color=("#007AFF", "#007AFF"),
                    hover_color=("#0051D5", "#0051D5")
                )
            else:
                btn.configure(
                    fg_color=("#39393d", "#39393d"),
                    hover_color=("#4a4a4d", "#4a4a4d")
                )
        
    def sync_settings(self):
        """Sync settings with animation"""
        self.sync_button.configure(text="Syncing...", state="disabled")
        self.root.update()
        
        # Simulate sync delay
        self.root.after(1500, self.sync_complete)
        
    def sync_complete(self):
        """Sync complete"""
        self.sync_button.configure(text="Sync Settings", state="normal")
        
        active_features = [name for name, status in self.feature_states.items() if status]
        
        if active_features:
            self.status_label.configure(text=f"Synced to device - {len(active_features)} features enabled")
        else:
            self.status_label.configure(text="Synced to device - All features disabled")

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
        
    def create_interface(self):
        """Create main interface"""
        # Main container with scrolling
        main_canvas = tk.Canvas(self.root, bg="#000000", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="#000000")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        self.create_header(scrollable_frame)
        
        # Status section
        self.create_status_section(scrollable_frame)
        
        # Settings section
        self.create_settings_section(scrollable_frame)
        
        # Theme section
        self.create_theme_section(scrollable_frame)
        
        # Sync button
        self.create_sync_section(scrollable_frame)
        
        # Layout
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
    def create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg="#000000", height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Back button
        back_btn = tk.Label(header_frame, text="‹", 
                           font=("Segoe UI", 28),
                           bg="#000000", fg="white")
        back_btn.pack(side=tk.LEFT, anchor="w")
        
        # Title
        self.title_label = tk.Label(header_frame, text="Settings", 
                                   font=("Segoe UI", 32, "bold"),
                                   bg="#000000", fg="white")
        self.title_label.pack(anchor="w", pady=(10, 0))
        
        self.header_widgets = [header_frame, back_btn, self.title_label]
        
    def create_status_section(self, parent):
        """Create status section"""
        status_frame = tk.Frame(parent, bg="#1C1C1E")
        status_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        # Version info item
        version_item = SettingItem(status_frame, "Your Drive is up to date",
                                  has_switch=False, has_arrow=False,
                                  status_text="1.1.22")
        version_item.pack(fill=tk.X)
        
        self.status_widgets = [status_frame, version_item]
        
    def create_settings_section(self, parent):
        """Create settings section"""
        settings_frame = tk.Frame(parent, bg="#1C1C1E")
        settings_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Create setting items for each feature
        for feature in self.features:
            if feature["type"] == "switch":
                item = SettingItem(settings_frame, feature["title"],
                                  has_switch=True, callback=self.on_feature_change)
                item.pack(fill=tk.X)
                self.setting_items[feature["title"]] = item
                
        # Add separator and additional settings
        separator = tk.Frame(settings_frame, bg="#39393D", height=1)
        separator.pack(fill=tk.X, pady=10)
        
        # Navigation settings
        nav_item = SettingItem(settings_frame, "Navigation settings",
                              has_switch=False, has_arrow=True)
        nav_item.pack(fill=tk.X)
        
        # Units
        units_item = SettingItem(settings_frame, "Units",
                                has_switch=False, has_arrow=True)
        units_item.pack(fill=tk.X)
        
        self.settings_widgets = [settings_frame, separator, nav_item, units_item]
        
    def create_theme_section(self, parent):
        """Create theme selection section"""
        theme_frame = tk.Frame(parent, bg="#1C1C1E")
        theme_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Theme title
        theme_title = tk.Label(theme_frame, text="Theme",
                              font=("Segoe UI", 18),
                              bg="#2C2C2E", fg="white")
        theme_title.pack(fill=tk.X, padx=20, pady=10)
        
        # Theme buttons
        theme_buttons_frame = tk.Frame(theme_frame, bg="#2C2C2E")
        theme_buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.theme_buttons = {}
        for i, theme_name in enumerate(self.themes.keys()):
            btn = tk.Button(theme_buttons_frame, text=theme_name,
                          font=("Segoe UI", 14),
                          command=lambda t=theme_name: self.change_theme(t),
                          relief="flat", bd=0, padx=15, pady=8)
            btn.pack(side=tk.LEFT, padx=(0, 10) if i < len(self.themes)-1 else 0)
            self.theme_buttons[theme_name] = btn
            
        self.theme_widgets = [theme_frame, theme_title, theme_buttons_frame]
        
    def create_sync_section(self, parent):
        """Create sync section"""
        sync_frame = tk.Frame(parent, bg="#000000")
        sync_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.sync_button = tk.Button(sync_frame, text="Sync Settings",
                                   font=("Segoe UI", 18, "bold"),
                                   command=self.sync_settings,
                                   relief="flat", bd=0,
                                   pady=15, bg="#007AFF", fg="white")
        self.sync_button.pack(fill=tk.X)
        
        # Status
        self.status_label = tk.Label(sync_frame, text="Ready",
                                   font=("Segoe UI", 14),
                                   bg="#000000", fg="#8E8E93")
        self.status_label.pack(pady=(10, 0))
        
    def on_feature_change(self, feature_name, is_on):
        """Handle feature state change"""
        self.feature_states[feature_name] = is_on
        status_text = "enabled" if is_on else "disabled"
        self.status_label.config(text=f"{feature_name} {status_text}")
        
    def change_theme(self, theme_name):
        """Change theme"""
        self.current_theme = theme_name
        self.apply_theme()
        self.update_theme_buttons()
        self.status_label.config(text=f"Switched to {theme_name} theme")
        
    def update_theme_buttons(self):
        """Update theme button styles"""
        for theme_name, btn in self.theme_buttons.items():
            if theme_name == self.current_theme:
                btn.config(bg="#007AFF", fg="white")
            else:
                btn.config(bg="#39393D", fg="white")
                
    def apply_theme(self):
        """Apply current theme"""
        theme = self.themes[self.current_theme]
        
        # Apply to root
        self.root.config(bg=theme["bg"])
        
        # Apply to header
        for widget in self.header_widgets:
            try:
                if isinstance(widget, tk.Label):
                    widget.config(bg=theme["bg"], fg=theme["text_primary"])
                else:
                    widget.config(bg=theme["bg"])
            except:
                pass
                
        # Apply to settings
        for item in self.setting_items.values():
            try:
                item.config(bg=theme["card_bg"])
                for child in item.winfo_children():
                    self.apply_theme_to_widget(child, theme)
            except:
                pass
        
        # Apply to sync button
        self.sync_button.config(bg=theme["button_bg"])
        self.status_label.config(bg=theme["bg"], fg=theme["text_secondary"])
        
        self.update_theme_buttons()
        
    def apply_theme_to_widget(self, widget, theme):
        """Recursively apply theme to widget"""
        try:
            if isinstance(widget, tk.Frame):
                widget.config(bg=theme["item_bg"])
            elif isinstance(widget, tk.Label):
                widget.config(bg=theme["item_bg"], fg=theme["text_primary"])
            
            for child in widget.winfo_children():
                self.apply_theme_to_widget(child, theme)
        except:
            pass
        
    def sync_settings(self):
        """Sync settings"""
        self.sync_button.config(text="Syncing...", state="disabled")
        self.root.update()
        
        # Simulate sync delay
        self.root.after(1500, self.sync_complete)
        
    def sync_complete(self):
        """Sync complete"""
        self.sync_button.config(text="Sync Settings", state="normal")
        
        active_features = [name for name, status in self.feature_states.items() if status]
        
        if active_features:
            self.status_label.config(text=f"Sync complete - {len(active_features)} features enabled")
        else:
            self.status_label.config(text="Sync complete - All features disabled")

def main():
    root = tk.Tk()
    app = HUDApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
        
    def create_interface(self):
        """创建主界面"""
        # 主滚动框架
        main_canvas = tk.Canvas(self.root, bg="#F2F2F7", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg="#F2F2F7")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # 标题栏
        self.create_header(scrollable_frame)
        
        # 主题选择
        self.create_theme_selector(scrollable_frame)
        
        # 功能卡片区域
        self.create_feature_cards(scrollable_frame)
        
        # 同步按钮
        self.create_sync_button(scrollable_frame)
        
        # 状态栏
        self.create_status_bar(scrollable_frame)
        
        # 布局
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 鼠标滚轮绑定
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
    def create_header(self, parent):
        """创建标题栏"""
        header_frame = tk.Frame(parent, bg="#F2F2F7", height=100)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # 时间显示
        time_label = tk.Label(header_frame, text="9:41", 
                            font=("Arial", 18, "normal"),
                            bg="#F2F2F7", fg="#1C1C1E")
        time_label.pack(anchor="w")
        
        # 应用标题
        title_label = tk.Label(header_frame, text="HUD Control", 
                             font=("Arial", 32, "bold"),
                             bg="#F2F2F7", fg="#1C1C1E")
        title_label.pack(anchor="w", pady=(5, 0))
        
        self.header_widgets = [header_frame, time_label, title_label]
        
    def create_theme_selector(self, parent):
        """创建主题选择器"""
        theme_frame = tk.Frame(parent, bg="#F2F2F7")
        theme_frame.pack(fill=tk.X, padx=20, pady=20)
        
        theme_label = tk.Label(theme_frame, text="主题", 
                             font=("Arial", 18, "normal"),
                             bg="#F2F2F7", fg="#1C1C1E")
        theme_label.pack(anchor="w", pady=(0, 10))
        
        # 主题按钮容器
        buttons_frame = tk.Frame(theme_frame, bg="#F2F2F7")
        buttons_frame.pack(fill=tk.X)
        
        self.theme_buttons = {}
        for i, theme_name in enumerate(self.themes.keys()):
            btn = tk.Button(buttons_frame, text=theme_name,
                          font=("Arial", 14),
                          command=lambda t=theme_name: self.change_theme(t),
                          relief="flat", bd=0, padx=20, pady=8)
            btn.pack(side=tk.LEFT, padx=(0, 10) if i < len(self.themes)-1 else 0)
            self.theme_buttons[theme_name] = btn
            
        self.theme_widgets = [theme_frame, theme_label, buttons_frame]
        self.update_theme_buttons()
        
    def create_feature_cards(self, parent):
        """创建功能卡片"""
        cards_frame = tk.Frame(parent, bg="#F2F2F7")
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        for feature_name, feature_info in self.features.items():
            card = FeatureCard(cards_frame, feature_name, 
                             feature_info["icon"],
                             callback=self.on_feature_change)
            card.pack(fill=tk.X, pady=(0, 12))
            self.feature_cards[feature_name] = card
            
    def create_sync_button(self, parent):
        """创建同步按钮"""
        sync_frame = tk.Frame(parent, bg="#F2F2F7")
        sync_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.sync_button = tk.Button(sync_frame, text="同步设置",
                                   font=("Arial", 18, "normal"),
                                   command=self.sync_settings,
                                   relief="flat", bd=0,
                                   pady=15, bg="#007AFF", fg="white")
        self.sync_button.pack(fill=tk.X)
        
        # 添加圆角效果（模拟）
        self.sync_button.config(relief="flat", bd=0)
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = tk.Frame(parent, bg="#F2F2F7")
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 30))
        
        self.status_label = tk.Label(status_frame, text="就绪",
                                   font=("Arial", 14),
                                   bg="#F2F2F7", fg="#8E8E93")
        self.status_label.pack()
        
    def on_feature_change(self, feature_name, is_on):
        """功能状态改变回调"""
        self.features[feature_name]["status"] = is_on
        status_text = "开启" if is_on else "关闭"
        self.status_label.config(text=f"{feature_name} 已{status_text}")
        
    def change_theme(self, theme_name):
        """切换主题"""
        self.current_theme = theme_name
        self.apply_theme()
        self.update_theme_buttons()
        self.status_label.config(text=f"已切换到{theme_name}主题")
        
    def update_theme_buttons(self):
        """更新主题按钮样式"""
        for theme_name, btn in self.theme_buttons.items():
            if theme_name == self.current_theme:
                btn.config(bg="#007AFF", fg="white")
            else:
                btn.config(bg="#E5E5EA", fg="#1C1C1E")
                
    def apply_theme(self):
        """应用主题"""
        theme = self.themes[self.current_theme]
        
        # 应用到根窗口
        self.root.config(bg=theme["bg"])
        
        # 应用到标题栏
        for widget in self.header_widgets:
            try:
                if isinstance(widget, tk.Label):
                    widget.config(bg=theme["bg"], fg=theme["text_primary"])
                else:
                    widget.config(bg=theme["bg"])
            except:
                pass
                
        # 应用到主题选择器
        for widget in self.theme_widgets:
            try:
                if isinstance(widget, tk.Label):
                    widget.config(bg=theme["bg"], fg=theme["text_primary"])
                else:
                    widget.config(bg=theme["bg"])
            except:
                pass
        
        # 应用到同步按钮
        self.sync_button.config(bg=theme["accent"], fg="white")
        
        # 应用到状态栏
        self.status_label.config(bg=theme["bg"], fg=theme["text_secondary"])
        
        self.update_theme_buttons()
        
    def sync_settings(self):
        """同步设置"""
        self.sync_button.config(text="同步中...", state="disabled")
        self.root.update()
        
        # 模拟同步延迟
        self.root.after(1500, self.sync_complete)
        
    def sync_complete(self):
        """同步完成"""
        self.sync_button.config(text="同步设置", state="normal")
        
        active_features = [name for name, info in self.features.items() 
                         if info["status"]]
        
        if active_features:
            self.status_label.config(text=f"同步完成 - {len(active_features)}个功能已启用")
        else:
            self.status_label.config(text="同步完成 - 所有功能均已关闭")

def main():
    root = tk.Tk()
    app = HUDApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()