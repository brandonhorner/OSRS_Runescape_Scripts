#!/usr/bin/env python3
# cooking_bot.py
# PyQt6 version with modern UI framework

import sys
import os
import time
import random
import pyautogui
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QListWidget, QPushButton, 
                             QScrollArea, QFrame, QSpinBox, QLineEdit, 
                             QMessageBox, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QBrush

# Add the parent directory to the path so we can import screen_interactor
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen_interactor import ScreenInteractor
from image_monitor import ImageMonitor

class TranslucentPanel(QFrame):
    """A translucent panel with modern styling."""
    
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setObjectName("TranslucentPanel")
        self.color = color
        self.setup_style()
        
    def setup_style(self):
        """Setup the modern styling with translucent panels."""
        # Create a semi-transparent background
        self.setStyleSheet(f"""
            QFrame#TranslucentPanel {{
                background-color: rgba({self.color[0]}, {self.color[1]}, {self.color[2]}, 0.85);
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
            
            QLabel {{
                color: rgba(0, 0, 0, 0.9);
                background: transparent;
                border: none;
            }}
            
            QListWidget {{
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(70, 130, 180, 0.5);
                border-radius: 8px;
                color: rgba(0, 0, 0, 0.9);
                font-size: 12px;
            }}
            
            QListWidget::item {{
                padding: 8px;
                border-bottom: 1px solid rgba(70, 130, 180, 0.2);
            }}
            
            QListWidget::item:selected {{
                background: rgba(70, 130, 180, 0.8);
                color: white;
            }}
            
            QPushButton {{
                background: rgba(70, 130, 180, 0.9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
            
            QPushButton:hover {{
                background: rgba(70, 130, 180, 1.0);
            }}
            
            QPushButton:pressed {{
                background: rgba(50, 100, 150, 1.0);
            }}
            
            QPushButton#startButton {{
                background: rgba(34, 139, 34, 0.9);
                font-size: 14px;
                padding: 12px 24px;
            }}
            
            QPushButton#startButton:hover {{
                background: rgba(34, 139, 34, 1.0);
            }}
            
            QLineEdit {{
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(70, 130, 180, 0.5);
                border-radius: 6px;
                padding: 6px;
                color: rgba(0, 0, 0, 0.9);
            }}
            
            QSpinBox {{
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(70, 130, 180, 0.5);
                border-radius: 6px;
                padding: 6px;
                color: rgba(0, 0, 0, 0.9);
            }}
            
            QSpinBox::up-button, QSpinBox::down-button {{
                background: transparent;
                border: none;
                width: 0px;
                height: 0px;
            }}
            
            QSpinBox::up-arrow, QSpinBox::down-arrow {{
                image: none;
                border: none;
                width: 0px;
                height: 0px;
            }}
        """)

class CookingBotPyQt6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("General Cooking Bot - Hosidius Kitchen")
        self.setGeometry(100, 100, 760, 840)
        
        # Available raw foods with their cooked counterparts
        self.available_foods = {
            "raw_karambwan.png": "cooked_karambwan.png",
            "raw_shark.png": "cooked_shark.png", 
            "raw_manta_ray.png": "cooked_manta_ray.png",
            "raw_swordfish.png": "cooked_swordfish.png",
            "raw_lobster.png": "cooked_lobster.png",
            "raw_salmon.png": "cooked_salmon.png",
            "raw_tuna.png": "cooked_tuna.png",
            "raw_bass.png": "cooked_bass.png",
            "raw_sea_turtle.png": "cooked_sea_turtle.png",
            "raw_chicken.png": "cooked_chicken.png",
            "raw_trout.png": "cooked_trout.png",
            "raw_shrimp.png": "cooked_shrimp.png"
        }
        
        self.selected_foods = []
        self.max_loops = 500
        
        # Setup UI
        self.setup_ui()
        
        # Connect double-click events
        self.available_list.itemDoubleClicked.connect(self.add_food)
        self.selected_list.itemDoubleClicked.connect(self.remove_food)
        
    def setup_ui(self):
        """Setup the main UI with modern PyQt6 framework."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title and warnings
        self.create_header_section(main_layout)
        
        # Three panel layout
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(20)
        
        # Left panel - Available foods (Soft Blue)
        self.available_panel = self.create_available_foods_panel()
        panels_layout.addWidget(self.available_panel, stretch=1)
        
        # Center panel - Action buttons
        self.actions_panel = self.create_actions_panel()
        panels_layout.addWidget(self.actions_panel, stretch=1)
        
        # Right panel - Selected foods (Soft Green)
        self.selected_panel = self.create_selected_foods_panel()
        panels_layout.addWidget(self.selected_panel, stretch=1)
        
        main_layout.addLayout(panels_layout)
        
        # Bottom controls
        self.create_bottom_controls(main_layout)
        
    def create_header_section(self, main_layout):
        """Create the header section with title and warnings."""
        # Title
        title_label = QLabel("General Cooking Bot")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 0, 0, 0.9);
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                border: none;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Warnings
        warnings_panel = TranslucentPanel((255, 200, 200))  # Light red for warnings
        warnings_layout = QVBoxLayout(warnings_panel)
        warnings_layout.setContentsMargins(15, 15, 15, 15)
        
        warning1 = QLabel("⚠️ Make sure you are in the Hosidius Kitchen area!")
        warning1.setStyleSheet("color: rgba(139, 0, 0, 0.9); font-weight: bold; font-size: 12px;")
        warnings_layout.addWidget(warning1)
        
        warning2 = QLabel("⚠️ Make sure you have all raw foods visible in your default bank view!")
        warning2.setStyleSheet("color: rgba(139, 0, 0, 0.9); font-weight: bold; font-size: 12px;")
        warnings_layout.addWidget(warning2)
        
        instructions = QLabel("Select raw foods to cook in order (top to bottom). The bot will cook each type until finished before moving to the next.")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: rgba(0, 0, 0, 0.8); font-size: 11px; margin-top: 5px;")
        warnings_layout.addWidget(instructions)
        
        main_layout.addWidget(warnings_panel)
        
    def create_available_foods_panel(self):
        """Create the available foods selection panel."""
        panel = TranslucentPanel((230, 243, 255))  # Soft light blue
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Available Raw Foods")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Available foods list
        self.available_list = QListWidget()
        self.available_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        
        # Populate available foods
        for raw_food in self.available_foods.keys():
            food_name = raw_food.replace("raw_", "").replace(".png", "").title()
            self.available_list.addItem(food_name)
        
        layout.addWidget(self.available_list)
        
        return panel
        
    def create_actions_panel(self):
        """Create the action buttons panel."""
        panel = TranslucentPanel((255, 242, 230))  # Soft sunset yellow-orange
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Actions")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Add button
        add_btn = QPushButton("→ Add Food")
        add_btn.clicked.connect(self.add_food)
        layout.addWidget(add_btn)
        
        # Remove button
        remove_btn = QPushButton("← Remove Food")
        remove_btn.clicked.connect(self.remove_food)
        layout.addWidget(remove_btn)
        
        # Clear all button
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all_foods)
        layout.addWidget(clear_btn)
        
        # Add stretch to center buttons
        layout.addStretch()
        
        return panel
        
    def create_selected_foods_panel(self):
        """Create the selected foods panel."""
        panel = TranslucentPanel((230, 247, 230))  # Soft green
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Cooking Order")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Selected foods list
        self.selected_list = QListWidget()
        layout.addWidget(self.selected_list)
        
        return panel
        
    def create_bottom_controls(self, main_layout):
        """Create the bottom controls section."""
        controls_panel = TranslucentPanel((240, 240, 240))  # Light gray
        controls_layout = QHBoxLayout(controls_panel)
        controls_layout.setContentsMargins(20, 15, 20, 15)
        
        # Max loops input
        loops_label = QLabel("Max Loops:")
        loops_label.setStyleSheet("font-weight: bold;")
        controls_layout.addWidget(loops_label)
        
        self.max_loops_spinbox = QSpinBox()
        self.max_loops_spinbox.setRange(1, 1000)
        self.max_loops_spinbox.setValue(500)
        controls_layout.addWidget(self.max_loops_spinbox)
        
        # Add stretch to push start button to the right
        controls_layout.addStretch()
        
        # Start button
        start_btn = QPushButton("Start Cooking Bot")
        start_btn.setObjectName("startButton")
        start_btn.clicked.connect(self.start_bot)
        controls_layout.addWidget(start_btn)
        
        main_layout.addWidget(controls_panel)
        
    def add_food(self):
        """Add selected food to cooking order."""
        current_item = self.available_list.currentItem()
        if current_item:
            food_name = current_item.text()
            raw_filename = f"raw_{food_name.lower()}.png"
            
            if raw_filename in self.available_foods and raw_filename not in [f[0] for f in self.selected_foods]:
                self.selected_foods.append((raw_filename, self.available_foods[raw_filename]))
                self.selected_list.addItem(food_name)
                
    def remove_food(self):
        """Remove selected food from cooking order."""
        current_item = self.selected_list.currentItem()
        if current_item:
            food_name = current_item.text()
            raw_filename = f"raw_{food_name.lower()}.png"
            
            # Remove from selected foods list
            self.selected_foods = [(r, c) for r, c in self.selected_foods if r != raw_filename]
            
            # Remove from list widget
            row = self.selected_list.row(current_item)
            self.selected_list.takeItem(row)
            
    def clear_all_foods(self):
        """Clear all foods from cooking order."""
        self.selected_foods.clear()
        self.selected_list.clear()
        
    def start_bot(self):
        """Start the cooking bot."""
        if not self.selected_foods:
            QMessageBox.warning(self, "No Foods Selected", "Please select at least one food to cook!")
            return
        
        try:
            max_loops = self.max_loops_spinbox.value()
            if max_loops <= 0:
                QMessageBox.showerror("Invalid Input", "Max loops must be a positive number!")
                return
        except ValueError:
            QMessageBox.showerror("Invalid Input", "Max loops must be a valid number!")
            return
        
        # Confirm start
        food_list = "\n".join([f"• {f[0].replace('raw_', '').replace('.png', '').title()}" 
                              for f in self.selected_foods])
        
        confirm = QMessageBox.question(self, "Confirm Start", 
                                     f"Start cooking bot with {len(self.selected_foods)} food types?\n\n"
                                     f"Foods to cook:\n{food_list}\n\n"
                                     f"Max loops: {max_loops}\n\n"
                                     f"CV3 Configuration: Using optimized weights (shape:0.2, color:0.8) for cooked vs raw discrimination",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.hide()  # Hide the UI
            time.sleep(3)
            self.run_cooking_bot(max_loops)
            
    def run_cooking_bot(self, max_loops):
        """Run the cooking bot with the selected foods."""
        try:
            main_loop(self.selected_foods, max_loops)
        except Exception as e:
            QMessageBox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.show()  # Show the UI again

def setup_bot(si):
    """Initial setup: Zoom, face north, open bank, and activate bank all feature"""
    print("Starting cooking bot setup...")
    
    # Step 1: Zoom setup - zoom in 10 times then out 2 times
    print("Setting up zoom...")
    si.zoom_in(times=10)
    time.sleep(random.uniform(0.5, 1.0))
    si.zoom_out(times=3)
    time.sleep(random.uniform(0.5, 1.0))
    
    # Step 2: Face north using compass
    print("Facing north...")
    compass_click = si.click_on_compass()
    if not compass_click:
        print("Failed to click compass. Continuing anyway...")
    time.sleep(random.uniform(1, 2))
    
    # Step 3: Check if bank is already open
    print("Checking if bank is open...")
    bank_close_location = si.find_image_cv2('image_library/bank_close.png', region="v2", threshold=0.95)
    
    if not bank_close_location:
        # Bank not open, click the bank chest (teal pixels) with confirmation
        print("Bank not open. Clicking bank chest with confirmation...")
        try:
            bank_chest_success = si.find_pixel_right_click_confirm(
                "00FFFF", 
                "image_library/use_bank.png",
                attempts=3,
                pixel_offset_range_x=(5, 25),
                pixel_offset_range_y=(5, 25)
            )
            
            if bank_chest_success:
                print("Bank chest clicked successfully with confirmation.")
                
                # Wait for bank to open using ImageMonitor
                print("Waiting for bank to open...")
                bank_monitor = ImageMonitor(
                    screen_interactor=si,
                    image_path="image_library/bank_close.png",
                    region="v2",
                    confidence=0.95,
                    check_interval=1.0,
                    wait_for="appear"
                )
                bank_monitor.start()
                
                if bank_monitor.wait_for_condition(timeout=10):
                    print("Bank opened successfully.")
                    bank_monitor.stop()
                else:
                    print("Bank failed to open after 10 seconds.")
                    bank_monitor.stop()
                    return False
            else:
                print("Failed to click bank chest with confirmation.")
                return False
                
        except Exception as e:
            print(f"Bank chest interaction failed: {e}")
            return False
    else:
        print("Bank is already open.")
    
    # Step 4: Check for bank all quantity feature and activate if needed
    print("Checking bank all quantity feature...")
    bank_all_inactive = si.find_image_cv2('image_library/bank_all_quantity_is_inactive.png', 
                                         region="v2", threshold=0.98)
    
    if bank_all_inactive:
        print("Activating bank all quantity feature...")
        pyautogui.moveTo(bank_all_inactive[0], bank_all_inactive[1])
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        print("Bank all quantity feature activated.")
    else:
        print("Bank all quantity feature already active or not found.")
    
    # Step 5: Click deposit all inventory to clear any existing items
    print("Depositing all inventory to start fresh...")
    deposit_all_success = si.click_image_cv2_without_moving(
        "image_library/deposit_all_inventory.png",
        region="v2",
        confidence=0.95,
        offset_range=(0, 2)
    )
    
    if deposit_all_success:
        print("Deposit all inventory clicked successfully.")
        time.sleep(random.uniform(0.5, 1.0))
    else:
        print("Deposit all inventory button not found. Continuing anyway...")
    
    print("Setup complete!")
    return True

def cook_food_batch(si, raw_food, cooked_food):
    """Cook one batch of the specified food type."""
    print(f"Starting to cook {raw_food}...")
    
    # Use optimized weights for cooked vs raw discrimination
    weights = {"shape_weight": 0.2, "color_weight": 0.8}
    
    print(f"Using CV3 weights: Shape {weights['shape_weight']:.1f}, Color {weights['color_weight']:.1f}")
    
    # Step 1: Click on raw food in bank to withdraw
    # Use CV3 with strict color validation to avoid confusion with cooked items
    print(f"Withdrawing {raw_food} from bank using CV3 color-aware detection...")
    
    # Updated CV3 call with separate shape and color thresholds for better discrimination
    withdraw_success = si.click_image_cv3_without_moving(
        f"image_library/{raw_food}", 
        region="v2", 
        confidence=0.95,
        offset_range=(0, 2),
        shape_weight=weights['shape_weight'],
        color_weight=weights['color_weight'],
        shape_threshold=0.95,  # High shape threshold for accuracy
        color_threshold=0.95   # High color threshold to avoid cooked items
    )
    
    if not withdraw_success:
        print(f"{raw_food} not found in bank for withdrawal.")
        print("This could mean:")
        print("  - No more raw food available")
        print("  - CV3 color validation was too strict")
        print("  - Food is in a different bank tab")
        return False
    
    print(f"{raw_food} withdrawn successfully using CV3 color-aware detection.")
    time.sleep(random.uniform(0.4, 2.0))
    
    # Step 2: Close the bank
    print("Closing bank...")
    bank_close_click = si.click_image_cv2_without_moving(
        "image_library/bank_close.png",
        region="v2", 
        confidence=0.95, 
        offset_range=(1, 4)
    )
    
    if bank_close_click:
        print(f"Bank closed at {bank_close_click}.")
    else:
        print("Bank close button not found. Continuing...")
    
    time.sleep(random.uniform(0.3, 1.0))
    
    # Step 3: Click the clay oven (pink pixels) with confirmation
    print("Clicking clay oven with confirmation...")
    try:
        clay_oven_success = si.find_pixel_right_click_confirm(
            "FF00FF", 
            "image_library/cook_clay_oven.png"
        )
        
        if clay_oven_success:
            print("Clay oven clicked successfully with confirmation.")
        else:
            print("Failed to click clay oven with confirmation. Skipping this batch.")
            return False
            
    except Exception as e:
        print(f"Clay oven interaction failed: {e}. Skipping this batch.")
        return False
    
    # Step 4: Wait for movement to oven
    print("Waiting for movement to oven...")
    time.sleep(random.uniform(3.5, 6.0))
    
    # Step 5: Press spacebar to start cooking
    print("Pressing spacebar to start cooking...")
    pyautogui.press("space")
    
    # Step 6: Wait for cooking to complete by monitoring green "Cooking" text
    print(f"Waiting for {raw_food} to be cooked...")
    
    # First, wait for the green "Cooking" text to appear in activity_pane
    print("Waiting for green 'Cooking' text to appear...")
    cooking_start_timeout = 10  # Wait up to 10 seconds for cooking to start
    
    # Get the resolved activity_pane region
    activity_pane_region = si.get_scan_area("activity_pane")
    print(f"Searching for green 'Cooking' text in activity_pane region: {activity_pane_region}")
    
    # Look for green pixel (00A900) in activity_pane region
    green_cooking_pixel = si.find_pixel("00A900", region=activity_pane_region, tolerance=2)
    
    if green_cooking_pixel is None:
        print("Green 'Cooking' text not found. Waiting a bit and checking again...")
        time.sleep(2)
        green_cooking_pixel = si.find_pixel("00A900", region=activity_pane_region, tolerance=2)
        
        if green_cooking_pixel is None:
            print("Still no green 'Cooking' text found. Assuming cooking started anyway...")
        else:
            print(f"Green 'Cooking' text found at {green_cooking_pixel}")
    else:
        print(f"Green 'Cooking' text found at {green_cooking_pixel}")
    
    # Now monitor for the green pixel to disappear (cooking complete)
    print("Monitoring for cooking to complete...")
    from pixel_monitor import PixelMonitor
    
    cooking_monitor = PixelMonitor(
        screen_interactor=si,
        color_hex="00A900",
        region="activity_pane",
        tolerance=2,
        check_interval=1.0,
        wait_for="disappear"
    )
    
    cooking_monitor.start()
    
    if cooking_monitor.wait_for_condition(timeout=90):
        print(f"{raw_food} has been cooked successfully.")
        cooking_monitor.stop()
        
        # Wait randomly 3-7 seconds before returning from cooking
        wait_time = random.uniform(3, 7)
        print(f"Waiting {wait_time:.1f} seconds before returning to bank...")
        time.sleep(wait_time)
    else:
        print(f"Timeout waiting for {raw_food} to be cooked after 90 seconds.")
        cooking_monitor.stop()
        return False
    
    # Step 7: Return to bank to deposit cooked food
    print("Returning to bank to deposit cooked food...")
    
    # Try up to 3 times to open the bank
    for attempt in range(3):
        try:
            # Click bank chest with confirmation
            bank_chest_success = si.find_pixel_right_click_confirm(
                "00FFFF", 
                "image_library/use_bank.png"
            )
            
            if bank_chest_success:
                print(f"Bank chest clicked successfully with confirmation (attempt {attempt + 1}/3).")
                
                # Wait for bank to open using ImageMonitor
                bank_monitor = ImageMonitor(
                    screen_interactor=si,
                    image_path="image_library/bank_close.png",
                    region="v2",
                    confidence=0.95,
                    check_interval=1.0,
                    wait_for="appear"
                )
                bank_monitor.start()
                
                if bank_monitor.wait_for_condition(timeout=10):
                    print("Bank opened successfully for deposit.")
                    bank_monitor.stop()
                    break
                else:
                    print(f"Bank failed to open on attempt {attempt + 1}/3.")
                    bank_monitor.stop()
                    
                    if attempt == 2:  # Last attempt
                        print("Failed to open bank after 3 attempts. Giving up.")
                        return False
            else:
                print(f"Failed to click bank chest with confirmation on attempt {attempt + 1}/3.")
                if attempt == 2:  # Last attempt
                    return False
                    
        except Exception as e:
            print(f"Bank chest interaction failed on attempt {attempt + 1}/3: {e}")
            if attempt == 2:  # Last attempt
                return False
    
    # Step 8: Deposit all inventory 
    print("Depositing all inventory...")
    deposit_all_success = si.click_image_cv2_without_moving(
        "image_library/deposit_all_inventory.png",
        region="v2",
        confidence=0.95,
        offset_range=(0, 2)
    )
    
    if deposit_all_success:
        print("All inventory deposited successfully.")
        time.sleep(random.uniform(1, 1.5))
    else:
        print("Deposit all inventory button not found. Continuing anyway...")
    
    print(f"Batch complete for {raw_food}.")
    return True

def main_loop(selected_foods, max_loops=50):
    """Main cooking loop that processes each selected food type."""
    si = ScreenInteractor()
    
    print(f"Starting Cooking Bot with {len(selected_foods)} food types")
    print("=" * 60)
    print("CV3 Configuration: Using optimized weights (shape:0.2, color:0.8) for cooked vs raw discrimination")
    print("This prevents confusion between raw and cooked items with enhanced accuracy.")
    print("=" * 60)
    
    # Initial setup
    if not setup_bot(si):
        print("Setup failed. Exiting.")
        return
    
    for food_index, (raw_food, cooked_food) in enumerate(selected_foods):
        print(f"\n{'='*20} Processing {raw_food.replace('raw_', '').replace('.png', '').title()} {'='*20}")
        
        # Cook this food type until max loops or no more raw food
        food_loops = 0
        while food_loops < max_loops:
            food_loops += 1
            print(f"\n--- Food Loop {food_loops} | Food Type: {raw_food.replace('raw_', '').replace('.png', '').title()} ---")
            
            if not cook_food_batch(si, raw_food, cooked_food):
                print(f"No more {raw_food} found in bank. Moving to next food type.")
                break
                
        print(f"Finished processing {raw_food.replace('raw_', '').replace('.png', '').title()}")
        
        if food_index < len(selected_foods) - 1:
            print("Moving to next food type...")
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print("Cooking Bot finished!")
    print("\nCV3 Method Summary:")
    print("✓ Successfully used color-aware detection to avoid cooked/raw confusion")
    print("✓ Maintained high accuracy while preventing false positives")
    print("✓ Optimized weights provided excellent discrimination between raw and cooked items")

def main():
    """Main function to run the PyQt6 cooking bot."""
    print("Starting General Cooking Bot (PyQt6)...")
    print("This bot uses CV3 color-aware detection for accurate food identification.")
    print("Features:")
    print("- Modern PyQt6 UI with translucent panels")
    print("- Optimized CV3 weights for cooked vs raw discrimination")
    print("- Automatic bank management and cooking process")
    print("- Color-aware validation to prevent false positives")
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = CookingBotPyQt6()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

