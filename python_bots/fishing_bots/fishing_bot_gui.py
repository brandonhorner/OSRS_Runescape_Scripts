#!/usr/bin/env python3
# fishing_bot_gui.py
# PyQt6 GUI application for the anglerfish fishing bot with logging and inventory control

import sys
import os
import time
import logging
import threading
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QCheckBox, QPushButton, 
                             QScrollArea, QFrame, QSpinBox, QLineEdit, 
                             QMessageBox, QFileDialog, QGridLayout, QProgressBar,
                             QTextEdit)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPalette, QBrush, QLinearGradient

# Add the parent directory to the path so we can import the bot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fish_anglers import AnglerfishBot

class TranslucentPanel(QFrame):
    """A translucent panel with blur effect and transparency."""
    
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setObjectName("TranslucentPanel")
        self.color = color
        self.setup_style()
        
    def setup_style(self):
        """Setup the translucent styling with blur effect."""
        # Create a semi-transparent background with blur
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
            
            QCheckBox {{
                color: rgba(0, 0, 0, 0.9);
                background: transparent;
                border: none;
                spacing: 8px;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid rgba(0, 0, 0, 0.6);
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.8);
            }}
            
            QCheckBox::indicator:checked {{
                background: rgba(70, 130, 180, 0.9);
                border: 2px solid rgba(70, 130, 180, 1.0);
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
            
            QPushButton:disabled {{
                background: rgba(128, 128, 128, 0.5);
                color: rgba(255, 255, 255, 0.5);
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
            
            QProgressBar {{
                border: 2px solid rgba(70, 130, 180, 0.5);
                border-radius: 6px;
                text-align: center;
                background: rgba(255, 255, 255, 0.8);
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(70, 130, 180, 0.9), stop:1 rgba(50, 100, 150, 0.9));
                border-radius: 4px;
            }}
            
            QTextEdit {{
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(70, 130, 180, 0.5);
                border-radius: 6px;
                color: rgba(0, 0, 0, 0.9);
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10px;
            }}
        """)

class BotThread(QThread):
    """Thread for running the bot without blocking the GUI."""
    status_update = pyqtSignal(str, str)  # message, level
    progress_update = pyqtSignal(int, int)  # current, target
    inventory_update = pyqtSignal(int)  # successful trips
    
    def __init__(self, target_inventories):
        super().__init__()
        self.target_inventories = target_inventories
        self.bot = None
        self.is_running = False
        self.current_inventories = 0
        
    def run(self):
        """Run the bot in the thread."""
        try:
            self.is_running = True
            self.status_update.emit("Starting bot...", "INFO")
            
            # Create bot instance
            self.bot = AnglerfishBot()
            
            # Run setup
            if not self.bot.setup():
                self.status_update.emit("Setup failed", "ERROR")
                return
            
            self.status_update.emit("Setup completed successfully", "INFO")
            # Update status to show bot is now running
            self.status_update.emit("Bot is now running", "STATUS")
            
            # Main bot loop with inventory counting
            loop_count = 0
            max_loops = 50000  # Safety limit
            
            while self.is_running and self.current_inventories < self.target_inventories and loop_count < max_loops:
                loop_count += 1
                
                # Check login status
                login_resolved = self.bot.si.resolveLogin()
                if not login_resolved:
                    self.status_update.emit("Login resolution failed, retrying...", "WARNING")
                    time.sleep(10)
                    continue
                
                # Check if we need to log login events
                if hasattr(self.bot.si, 'last_login_time'):
                    if not hasattr(self, 'last_logged_login') or self.bot.si.last_login_time != self.last_logged_login:
                        self.status_update.emit("Bot logged in successfully", "INFO")
                        self.last_logged_login = self.bot.si.last_login_time
                
                # Check for disconnection events
                if hasattr(self.bot.si, 'disconnection_detected') and self.bot.si.disconnection_detected:
                    self.status_update.emit("Disconnection detected, attempting to reconnect", "WARNING")
                    self.bot.si.disconnection_detected = False
                
                # Check for client restart events
                if hasattr(self.bot.si, 'client_restart_detected') and self.bot.si.client_restart_detected:
                    self.status_update.emit("Client restart detected, reinitializing", "WARNING")
                    self.bot.si.client_restart_detected = False
                
                # Run one iteration of the bot logic
                success = self.run_bot_iteration()
                
                # Check if we're out of bait
                if self.bot.state == "NO_BAIT":
                    self.status_update.emit("Bot stopped: No bait left. Please re-up and try again.", "ERROR")
                    break
                
                if success and self.bot.state == "NEED_BANK":
                    # Inventory was filled, count it
                    self.current_inventories += 1
                    self.bot.successful_trips = self.current_inventories  # Keep them in sync
                    
                    # Update UI
                    self.inventory_update.emit(self.current_inventories)
                    self.progress_update.emit(self.current_inventories, self.target_inventories)
                    
                    self.status_update.emit(f"Inventory {self.current_inventories}/{self.target_inventories} completed", "INFO")
                    
                    # Check if we've reached our target
                    if self.current_inventories >= self.target_inventories:
                        self.status_update.emit(f"Target of {self.target_inventories} inventories reached!", "INFO")
                        break
                
                # Small delay between iterations
                time.sleep(0.1)
            
            # Bot finished
            if self.current_inventories >= self.target_inventories:
                self.status_update.emit(f"Bot completed successfully! Finished {self.current_inventories} inventories", "INFO")
            elif loop_count >= max_loops:
                self.status_update.emit("Bot reached maximum loop limit", "WARNING")
            else:
                self.status_update.emit("Bot stopped by user", "INFO")
            
        except Exception as e:
            error_msg = f"Bot error: {str(e)}"
            print(f"Bot thread error: {error_msg}")
            self.status_update.emit(error_msg, "ERROR")
    
    def run_bot_iteration(self):
        """Run one iteration of the bot logic."""
        try:
            # Check inventory status first
            raw_angler_in_bag = self.bot.si.ensure_bag_open_and_check_last_slot('image_library/raw_anglerfish.png')
            
            if raw_angler_in_bag:
                self.bot.state = "NEED_BANK"
            
            # Handle current state
            if self.bot.state == "NEED_BANK":
                return self.bot.handle_banking_state()
            elif self.bot.state == "WALK_TO_FISH":
                return self.bot.handle_walking_state()
            elif self.bot.state == "READY_TO_FISH":
                return self.bot.handle_fishing_state()
            elif self.bot.state == "NO_BAIT":
                # No bait left - stop the bot
                self.status_update.emit("No bait left. Please re-up and try again.", "ERROR")
                return False
            else:
                self.bot.assess_state()
                return False
                
        except Exception as e:
            error_msg = f"Bot iteration error: {str(e)}"
            print(f"Bot iteration error: {error_msg}")
            self.status_update.emit(error_msg, "ERROR")
            return False
    
    def stop(self):
        """Stop the bot thread."""
        self.is_running = False

class FishingBotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anglerfish Fishing Bot - PyQt6")
        self.setGeometry(100, 100, 1000, 500)  # Start even smaller
        self.setMinimumSize(1000, 500)
        
        # Bot control variables
        self.bot_thread = None
        self.target_inventories = 0
        self.current_inventories = 0
        self.successful_trips = 0  # This will be kept in sync with current_inventories
        
        # Setup logging
        self.setup_logging()
        
        # Setup UI
        self.setup_ui()
        self.setup_background()
        
    def setup_logging(self):
        """Setup logging system for bot events"""
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger('FishingBot')
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        log_file = os.path.join(log_dir, f"fishing_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Log startup
        self.logger.info("Fishing Bot GUI started")
    
    def setup_ui(self):
        """Setup the main UI with translucent panels."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Anglerfish Fishing Bot")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Three panel layout
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(20)
        
        # Left panel - Controls (Soft Blue) - Same as image_tester.py
        self.controls_panel = self.create_controls_panel()
        panels_layout.addWidget(self.controls_panel, stretch=2)
        
        # Middle panel - Status (Soft Sunset Orange) - Same as image_tester.py
        self.status_panel = self.create_status_panel()
        panels_layout.addWidget(self.status_panel, stretch=2)
        
        # Right panel - Log (Soft Green) - Same as image_tester.py
        self.log_panel = self.create_log_panel()
        panels_layout.addWidget(self.log_panel, stretch=3)
        
        main_layout.addLayout(panels_layout)
        
    def create_controls_panel(self):
        """Create the controls panel."""
        panel = TranslucentPanel((230, 243, 255))  # Soft light blue
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Bot Controls")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Target inventories input
        inventory_layout = QHBoxLayout()
        inventory_layout.addWidget(QLabel("Target Inventories:"))
        self.inventory_spinbox = QSpinBox()
        self.inventory_spinbox.setRange(1, 1000)
        self.inventory_spinbox.setValue(10)
        inventory_layout.addWidget(self.inventory_spinbox)
        layout.addLayout(inventory_layout)
        
        # Start/Stop buttons
        button_layout = QVBoxLayout()
        
        self.start_button = QPushButton("Start Bot")
        self.start_button.setStyleSheet("""
            QPushButton {
                background: rgba(34, 139, 34, 0.9);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-weight: bold;
                font-size: 16px;
                min-height: 50px;
            }
            QPushButton:hover {
                background: rgba(34, 139, 34, 1.0);
            }
        """)
        self.start_button.clicked.connect(self.start_bot)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop Bot")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background: rgba(220, 20, 60, 0.9);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 30px;
                font-weight: bold;
                font-size: 16px;
                min-height: 50px;
            }
            QPushButton:hover {
                background: rgba(220, 20, 60, 1.0);
            }
        """)
        self.stop_button.clicked.connect(self.stop_bot)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return panel
        
    def create_status_panel(self):
        """Create the status panel."""
        panel = TranslucentPanel((255, 242, 230))  # Soft sunset yellow-orange
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Status")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Status labels
        self.status_label = QLabel("Stopped")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(220, 20, 60, 0.9);")
        layout.addWidget(self.status_label)
        
        # Successful trips
        trips_layout = QHBoxLayout()
        trips_layout.addWidget(QLabel("Successful Trips:"))
        self.trips_label = QLabel("0")
        self.trips_label.setStyleSheet("font-weight: bold;")
        trips_layout.addWidget(self.trips_label)
        layout.addLayout(trips_layout)
        
        # Progress bar
        progress_label = QLabel("Progress:")
        progress_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Progress percentage
        self.progress_label = QLabel("0%")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.progress_label)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return panel
        
    def create_log_panel(self):
        """Create the log panel."""
        panel = TranslucentPanel((230, 247, 230))  # Soft green
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Activity Log")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)  # Make it smaller to fit better
        layout.addWidget(self.log_text)
        
        # Clear log button
        clear_log_button = QPushButton("Clear Log")
        clear_log_button.clicked.connect(self.clear_log)
        layout.addWidget(clear_log_button)
        
        return panel
        
    def setup_background(self):
        """Setup the beautiful background image matching image_tester.py."""
        # Try multiple possible paths for the background image
        possible_paths = [
            "../image_library/UI_backgrounds/studio-gbli-1.png",  # Development path
            "image_library/UI_backgrounds/studio-gbli-1.png",     # Executable path
            os.path.join(os.path.dirname(__file__), "..", "image_library", "UI_backgrounds", "studio-gbli-1.png"),
            os.path.join(os.path.dirname(__file__), "image_library", "UI_backgrounds", "studio-gbli-1.png")
        ]
        
        background_path = None
        print("Searching for background image in the following paths:")
        for i, path in enumerate(possible_paths):
            exists = os.path.exists(path)
            print(f"  {i+1}. {path} - {'EXISTS' if exists else 'NOT FOUND'}")
            if exists and background_path is None:
                background_path = path
        
        if background_path:
            print(f"Background image found at: {background_path}")
            
            # Scale the image to fit the window dimensions
            try:
                from PyQt6.QtGui import QPixmap
                from PyQt6.QtCore import Qt
                
                # Load and scale the background image to window size
                pixmap = QPixmap(background_path)
                scaled_pixmap = pixmap.scaled(1000, 600, 
                                            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                            Qt.TransformationMode.SmoothTransformation)
                
                # Create a temporary file for the scaled image
                import tempfile
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, "fishing_bot_background.png")
                scaled_pixmap.save(temp_file)
                
                # Use the scaled image in CSS
                css_path = temp_file.replace('\\', '/')
                self.setStyleSheet(f"""
                    QMainWindow {{
                        background-image: url("{css_path}");
                        background-position: center;
                        background-repeat: no-repeat;
                    }}
                """)
                
            except Exception as e:
                print(f"Error scaling background: {e}")
                # Fallback to original image
                css_path = background_path.replace('\\', '/')
                self.setStyleSheet(f"""
                    QMainWindow {{
                        background-image: url("{css_path}");
                        background-position: center;
                        background-repeat: no-repeat;
                    }}
                """)
        else:
            print("Background image not found in any expected location")
            print("Using fallback gradient background")
            # Fallback gradient background (same as image_tester.py)
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFB366, stop:1 #FF8C42);
                }
            """)
    
    def log_message(self, message, level="INFO"):
        """Add a message to the log display."""
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {level}: {message}"
            
            self.log_text.append(log_entry)
            
            # Handle status updates specially
            if level == "STATUS":
                self.status_label.setText(message)
                if "running" in message.lower():
                    self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(34, 139, 34, 0.9);")
                elif "starting" in message.lower():
                    self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(255, 165, 0, 0.9);")
                elif "stopped" in message.lower() or "completed" in message.lower():
                    self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(220, 20, 60, 0.9);")
                return
            
            # Also log to file (avoid Unicode characters that cause encoding issues)
            safe_message = message.replace('✓', '[OK]').replace('✗', '[FAIL]').replace('⚠', '[WARN]')
            if level == "ERROR":
                self.logger.error(safe_message)
            elif level == "WARNING":
                self.logger.warning(safe_message)
            else:
                self.logger.info(safe_message)
        except Exception as e:
            print(f"Error in log_message: {e}")
            # Fallback to simple logging
            self.log_text.append(f"ERROR: {str(e)}")
    
    def clear_log(self):
        """Clear the log display."""
        self.log_text.clear()
    
    def start_bot(self):
        """Start the fishing bot."""
        try:
            # Get target inventories
            self.target_inventories = self.inventory_spinbox.value()
            
            # Reset counters
            self.current_inventories = 0
            self.successful_trips = 0  # Will be kept in sync
            self.update_display()
            
            # Update UI
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText("Starting...")
            self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(255, 165, 0, 0.9);")
            
            self.log_message(f"Starting bot with target of {self.target_inventories} inventories")
            
            # Create and start bot thread
            self.bot_thread = BotThread(self.target_inventories)
            self.bot_thread.status_update.connect(self.log_message)
            self.bot_thread.progress_update.connect(self.update_progress)
            self.bot_thread.inventory_update.connect(self.update_inventory_count)
            self.bot_thread.finished.connect(self.bot_finished)
            self.bot_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start bot: {str(e)}")
            self.log_message(f"Failed to start bot: {str(e)}", "ERROR")
    
    def stop_bot(self):
        """Stop the fishing bot."""
        if self.bot_thread and self.bot_thread.isRunning():
            self.bot_thread.stop()
            self.bot_thread.wait(5000)  # Wait up to 5 seconds
        
        self.status_label.setText("Stopped")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(220, 20, 60, 0.9);")
        self.log_message(f"Bot stopped. Completed {self.current_inventories}/{self.target_inventories} inventories")
        
        # Update UI
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def update_progress(self, current, target):
        """Update the progress bar and label."""
        self.current_inventories = current
        if target > 0:
            progress = (current / target) * 100
            print(f"DEBUG: Progress update - current: {current}, target: {target}, progress: {progress:.1f}%")
            self.progress_bar.setValue(int(progress))
            self.progress_label.setText(f"{progress:.1f}%")
        else:
            self.progress_bar.setValue(0)
            self.progress_label.setText("0%")
    
    def update_inventory_count(self, count):
        """Update the successful trips count."""
        self.successful_trips = count
        self.trips_label.setText(str(count))
    
    def update_display(self):
        """Update all display elements."""
        self.trips_label.setText(str(self.successful_trips))
        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")
    
    def bot_finished(self):
        """Called when the bot thread finishes."""
        self.status_label.setText("Completed")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: rgba(34, 139, 34, 0.9);")
        
        # Re-enable start button
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def closeEvent(self, event):
        """Handle window closing."""
        if self.bot_thread and self.bot_thread.isRunning():
            reply = QMessageBox.question(self, "Quit", 
                                       "Bot is running. Do you want to stop it and exit?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.stop_bot()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    """Main function to run the GUI."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = FishingBotGUI()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()