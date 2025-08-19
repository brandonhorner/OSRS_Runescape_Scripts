# area_tester_advanced.py
import tkinter as tk
from tkinter import ttk
import pyautogui
import time
from screen_interactor import ScreenInteractor

class AreaOverlay:
    """Creates a transparent overlay window to highlight screen areas."""
    def __init__(self, x, y, width, height, color="red", alpha=0.3):
        self.window = tk.Toplevel()
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.attributes('-topmost', True)  # Keep on top
        self.window.attributes('-alpha', alpha)  # Set transparency
        self.window.configure(bg=color)
        
        # Position and size the window
        self.window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make the window click-through (transparent to mouse events)
        self.window.attributes('-transparentcolor', color)
        
        # Add a border for visibility
        self.border = tk.Frame(self.window, bg="black", width=2)
        self.border.pack(fill="both", expand=True)
        
        # Add label with area name
        self.label = tk.Label(self.window, text="", bg=color, fg="white", font=("Arial", 8))
        self.label.pack(pady=2)
    
    def set_text(self, text):
        """Set the text displayed on the overlay."""
        self.label.config(text=text)
    
    def destroy(self):
        """Destroy the overlay window."""
        self.window.destroy()

class AdvancedAreaTester:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Screen Area Tester")
        self.root.geometry("450x700")
        
        # Create screen interactor
        self.si = ScreenInteractor()
        
        # Dictionary to store area checkboxes, their states, and overlays
        self.area_vars = {}
        self.area_overlays = {}
        
        # Create the UI
        self.create_ui()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Advanced Screen Area Tester", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(self.root, text="Toggle areas on/off to see search regions highlighted on screen\nRed boxes will appear showing the exact search areas", 
                              wraplength=400, justify="center")
        instructions.pack(pady=5)
        
        # Create scrollable frame for checkboxes
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get all available areas with descriptions
        areas = {
            "game_screen": "Main game area (excludes UI)",
            "center": "Center vertical strip",
            "p1": "Top-left quadrant",
            "p2": "Top-center quadrant", 
            "p3": "Top-right quadrant",
            "p4": "Bottom-left quadrant",
            "p5": "Bottom-center quadrant",
            "p6": "Bottom-right quadrant",
            "h1": "Top half of screen",
            "h2": "Bottom half of screen",
            "v1": "Left third of screen",
            "v2": "Center third of screen",
            "v3": "Right third of screen",
            "bag": "Inventory/bag area",
            "chat": "Chat box area",
            "activity_pane": "Activity panel area",
            "chat_area": "Chat area (alternative)",
            "runelite_right_menu": "RuneLite right menu area",
            "game_screen_middle_horizontal": "Middle horizontal game area",
            "bottom_of_char_zoom_8": "Below character (zoom 8)",
            "left_of_char_zoom_8": "Left of character (zoom 8)"
        }
        
        # Create checkboxes for each area
        for area_name, description in areas.items():
            var = tk.BooleanVar()
            self.area_vars[area_name] = var
            
            # Create frame for each area
            area_frame = tk.Frame(scrollable_frame)
            area_frame.pack(fill="x", padx=10, pady=2)
            
            # Checkbox
            cb = tk.Checkbutton(area_frame, text=area_name, variable=var, 
                               command=lambda name=area_name: self.toggle_area(name))
            cb.pack(side="left")
            
            # Description
            desc_label = tk.Label(area_frame, text=f" - {description}", 
                                 wraplength=300, justify="left")
            desc_label.pack(side="left", padx=(5, 0))
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        # Select all button
        select_all_btn = tk.Button(button_frame, text="Select All", 
                                  command=self.select_all_areas)
        select_all_btn.pack(side="left", padx=5)
        
        # Deselect all button
        deselect_all_btn = tk.Button(button_frame, text="Deselect All", 
                                    command=self.deselect_all_areas)
        deselect_all_btn.pack(side="left", padx=5)
        
        # Clear overlay button
        clear_btn = tk.Button(button_frame, text="Clear All Overlays", 
                             command=self.clear_all_overlays)
        clear_btn.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(button_frame, text="Refresh Areas", 
                               command=self.refresh_areas)
        refresh_btn.pack(side="left", padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready - Toggle areas to see overlays", fg="green")
        self.status_label.pack(pady=5)
        
        # Info label
        info_label = tk.Label(self.root, text="Tip: Switch to your game window to see the overlays", 
                             fg="blue", font=("Arial", 9))
        info_label.pack(pady=2)
    
    def toggle_area(self, area_name):
        """Toggle the visibility of a specific area overlay."""
        if self.area_vars[area_name].get():
            self.show_area_overlay(area_name)
        else:
            self.hide_area_overlay(area_name)
    
    def show_area_overlay(self, area_name):
        """Show the overlay for a specific area."""
        try:
            # Get the coordinates for the area
            coords = self.si.get_scan_area(area_name)
            x, y, width, height = coords
            
            # Create overlay
            overlay = AreaOverlay(x, y, width, height, color="red", alpha=0.3)
            overlay.set_text(area_name)
            
            # Store the overlay
            self.area_overlays[area_name] = overlay
            
            # Update status
            self.status_label.config(text=f"Showing overlay for {area_name}", fg="blue")
            print(f"Showing overlay for {area_name}: {coords}")
            
        except Exception as e:
            self.status_label.config(text=f"Error showing {area_name}: {str(e)}", fg="red")
            print(f"Error showing overlay for {area_name}: {e}")
    
    def hide_area_overlay(self, area_name):
        """Hide the overlay for a specific area."""
        if area_name in self.area_overlays:
            self.area_overlays[area_name].destroy()
            del self.area_overlays[area_name]
            self.status_label.config(text=f"Hidden overlay for {area_name}", fg="orange")
            print(f"Hidden overlay for {area_name}")
    
    def select_all_areas(self):
        """Select all area checkboxes and show all overlays."""
        for area_name, var in self.area_vars.items():
            var.set(True)
            self.show_area_overlay(area_name)
        self.status_label.config(text="Showing all area overlays", fg="blue")
    
    def deselect_all_areas(self):
        """Deselect all area checkboxes and hide all overlays."""
        for area_name, var in self.area_vars.items():
            var.set(False)
            self.hide_area_overlay(area_name)
        self.status_label.config(text="Hidden all area overlays", fg="red")
    
    def clear_all_overlays(self):
        """Clear all overlays from screen."""
        for overlay in self.area_overlays.values():
            overlay.destroy()
        self.area_overlays.clear()
        
        # Also deselect all checkboxes
        for var in self.area_vars.values():
            var.set(False)
        
        self.status_label.config(text="All overlays cleared", fg="green")
    
    def refresh_areas(self):
        """Refresh all visible overlays (useful if screen resolution changed)."""
        visible_areas = [name for name, var in self.area_vars.items() if var.get()]
        
        # Clear all overlays
        for overlay in self.area_overlays.values():
            overlay.destroy()
        self.area_overlays.clear()
        
        # Recreate overlays for visible areas
        for area_name in visible_areas:
            self.show_area_overlay(area_name)
        
        self.status_label.config(text=f"Refreshed {len(visible_areas)} overlays", fg="blue")
    
    def on_closing(self):
        """Handle window closing - clean up all overlays."""
        self.clear_all_overlays()
        self.root.destroy()
    
    def run(self):
        """Start the tester application."""
        self.root.mainloop()

def main():
    """Main function to run the advanced area tester."""
    print("Starting Advanced Screen Area Tester...")
    print("This will create visual overlays on your screen showing the search areas.")
    print("Make sure to switch to your game window to see the overlays!")
    
    # Wait a moment for user to switch to game window
    print("Starting...")
    
    # Create and run the tester
    tester = AdvancedAreaTester()
    tester.run()

if __name__ == "__main__":
    main()
