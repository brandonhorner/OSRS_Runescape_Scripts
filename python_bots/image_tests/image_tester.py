#!/usr/bin/env python3
# combined_image_tester_pyqt6.py
# PyQt6 version with native translucent panels and modern UI

import sys
import os
import time
import cv2
import numpy as np
import pyautogui
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QCheckBox, QPushButton, 
                             QScrollArea, QFrame, QSpinBox, QLineEdit, 
                             QMessageBox, QFileDialog, QGridLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPalette, QBrush, QLinearGradient
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QPoint

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from screen_interactor import ScreenInteractor

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

class TransparentAreaOverlay(QWidget):
    """Creates a transparent overlay window with only borders visible."""
    
    def __init__(self, x, y, width, height, area_name="", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # Position and size
        self.setGeometry(x, y, width, height)
        
        # Make click-through
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        # Store area info
        self.area_name = area_name
        
    def paintEvent(self, event):
        """Custom paint event to draw the border."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw semi-transparent red border
        pen = painter.pen()
        pen.setColor(QColor(255, 0, 0, 180))
        pen.setWidth(3)
        painter.setPen(pen)
        
        # Draw border rectangle
        painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
        
        # Draw area name label
        if self.area_name:
            painter.setPen(QColor(255, 0, 0, 255))
            font = QFont("Arial", 10, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(10, 20, self.area_name)

class CombinedImageTesterPyQt6(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Combined Image Tester - CV2 & CV3 (PyQt6)")
        self.setGeometry(100, 100, 1920, 1000)
        
        # Set minimum window size to maintain 3 columns in left panel
        # 1600px is the threshold for 3 columns, so we'll set minimum to 1700px
        self.setMinimumSize(1700, 800)
        
        # Create screen interactor
        self.si = ScreenInteractor()
        
        # Store overlays and variables
        self.area_overlays = {}
        self.area_vars = {}
        self.image_vars = {}
        self.cv3_variations = {}
        
        # Background scaling variables
        self.original_background_path = "image_library\\UI_backgrounds\\studio-gbli-1.png"
        self.last_window_size = (1920, 1000)
        self.resize_timer = None  # For throttling resize events
        
        # Get available images
        self.available_images = self.get_available_images()
        
        # Setup UI
        self.setup_ui()
        self.setup_background()
        
        # Connect resize event
        self.resizeEvent = self.on_resize
        
        # Store the scroll layout for responsive updates
        self.image_scroll_layout = None
        
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
        title_label = QLabel("Combined Image Tester - CV2 & CV3")
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
        
        # Left panel - Images (Soft Blue) - Larger size
        self.images_panel = self.create_images_panel()
        panels_layout.addWidget(self.images_panel, stretch=4)  # 4 parts
        
        # Middle panel - Areas (Soft Sunset Orange) - Smaller size
        self.areas_panel = self.create_areas_panel()
        panels_layout.addWidget(self.areas_panel, stretch=2)  # 2 parts (about 30% smaller)
        
        # Right panel - Search Methods (Soft Green) - Keep same size
        self.search_panel = self.create_search_methods_panel()
        panels_layout.addWidget(self.search_panel, stretch=3)  # 3 parts
        
        main_layout.addLayout(panels_layout)
        
        # Run button at bottom
        run_button = QPushButton("Run Image Test")
        run_button.setStyleSheet("""
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
        run_button.clicked.connect(self.run_image_test)
        main_layout.addWidget(run_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
    def create_images_panel(self):
        """Create the images selection panel."""
        panel = TranslucentPanel((230, 243, 255))  # Soft light blue
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Images to Test")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Select one or more images to test\nImages are organized in columns for easy selection")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Scrollable image list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(8)
        
        # Store reference for responsive updates
        self.image_scroll_layout = scroll_layout
        
        # Create image checkboxes in responsive columns
        self.image_vars = {}
        self.image_checkboxes = []  # Store references for layout updates
        
        for i, image_name in enumerate(self.available_images):
            var = QCheckBox(image_name)
            self.image_vars[image_name] = var
            self.image_checkboxes.append(var)
        
        # Initial layout with 3 columns
        self.update_image_layout()
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Custom image path
        custom_label = QLabel("Custom image path:")
        custom_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(custom_label)
        
        self.custom_image_var = QLineEdit()
        layout.addWidget(self.custom_image_var)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Select All Images")
        select_all_btn.clicked.connect(self.select_all_images)
        buttons_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all_images)
        buttons_layout.addWidget(deselect_all_btn)
        
        layout.addLayout(buttons_layout)
        
        return panel
        
    def create_areas_panel(self):
        """Create the areas selection panel."""
        panel = TranslucentPanel((255, 242, 230))  # Soft sunset yellow-orange
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Screen Areas")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("Toggle areas on/off to see search regions highlighted\nRed borders will show the exact search areas")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Scrollable areas list
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)
        
        # Get all available areas
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
            "bank_pane": "Bank pane area",
            "bank_pane_with_menus": "Bank pane area with menus",
            "chat_area": "Chat area (alternative)",
            "runelite_right_menu": "RuneLite right menu area",
            "game_screen_middle_horizontal": "Middle horizontal game area",
            "bottom_of_char_zoom_8": "Below character (zoom 8)",
            "left_of_char_zoom_8": "Left of character (zoom 8)"
        }
        
        # Create area checkboxes
        for area_name, description in areas.items():
            var = QCheckBox(f"{area_name} - {description}")
            self.area_vars[area_name] = var
            var.toggled.connect(lambda checked, name=area_name: self.toggle_area(name, checked))
            scroll_layout.addWidget(var)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Select All Areas")
        select_all_btn.clicked.connect(self.select_all_areas)
        buttons_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.deselect_all_areas)
        buttons_layout.addWidget(deselect_all_btn)
        
        clear_btn = QPushButton("Clear Overlays")
        clear_btn.clicked.connect(self.clear_all_overlays)
        buttons_layout.addWidget(clear_btn)
        
        layout.addLayout(buttons_layout)
        
        return panel
        
    def create_search_methods_panel(self):
        """Create the search methods configuration panel."""
        panel = TranslucentPanel((230, 247, 230))  # Soft green
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Search Methods")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Detection Methods
        method_label = QLabel("Detection Methods:")
        method_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(method_label)
        
        self.cv2_var = QCheckBox("CV2 Template Matching")
        self.cv2_var.setChecked(True)
        layout.addWidget(self.cv2_var)
        
        self.cv3_var = QCheckBox("CV3 Enhanced Matching")
        self.cv3_var.setChecked(True)
        layout.addWidget(self.cv3_var)
        
        # CV3 variations
        cv3_label = QLabel("CV3 Weight Variations:")
        cv3_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(cv3_label)
        
        cv3_variations_data = [
            ("Strong Color", 0.1, 0.9, "Emphasizes color over shape"),
            ("Color Focused", 0.2, 0.8, "High color weight"),
            ("Balanced", 0.5, 0.5, "Equal shape and color weight"),
            ("Shape Focused", 0.8, 0.2, "High shape weight"),
            ("Strong Shape", 0.9, 0.1, "Emphasizes shape over color"),
            ("Ultra Strict", 0.1, 0.9, "Maximum color validation")
        ]
        
        for name, shape_w, color_w, desc in cv3_variations_data:
            var = QCheckBox(f"{name} (Shape: {shape_w}, Color: {color_w}) - {desc}")
            var.setChecked(True)
            self.cv3_variations[name] = {"var": var, "shape": shape_w, "color": color_w, "desc": desc}
            layout.addWidget(var)
        
        # Confidence threshold
        confidence_label = QLabel("Confidence Threshold:")
        confidence_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(confidence_label)
        
        self.confidence_var = QSpinBox()
        self.confidence_var.setRange(70, 100)
        self.confidence_var.setValue(85)
        self.confidence_var.setSuffix("%")
        layout.addWidget(self.confidence_var)
        
        # CV3 specific thresholds
        cv3_threshold_label = QLabel("CV3 Thresholds:")
        cv3_threshold_label.setStyleSheet("font-weight: bold; margin-top: 15px;")
        layout.addWidget(cv3_threshold_label)
        
        # Shape threshold
        shape_layout = QHBoxLayout()
        shape_label = QLabel("Shape:")
        shape_label.setStyleSheet("min-width: 50px;")
        shape_layout.addWidget(shape_label)
        
        self.shape_threshold_var = QSpinBox()
        self.shape_threshold_var.setRange(70, 100)
        self.shape_threshold_var.setValue(95)
        self.shape_threshold_var.setSuffix("%")
        shape_layout.addWidget(self.shape_threshold_var)
        layout.addLayout(shape_layout)
        
        # Color threshold
        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        color_label.setStyleSheet("min-width: 50px;")
        color_layout.addWidget(color_label)
        
        self.color_threshold_var = QSpinBox()
        self.color_threshold_var.setRange(70, 100)
        self.color_threshold_var.setValue(95)
        self.color_threshold_var.setSuffix("%")
        color_layout.addWidget(self.color_threshold_var)
        layout.addLayout(color_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return panel
        
    def setup_background(self):
        """Setup the beautiful background image."""
        # Set window background to the Ghibli image
        background_path = "image_library\\UI_backgrounds\\studio-gbli-1.png"
        
        if os.path.exists(background_path):
            print(f"Background image found at: {background_path}")
            
            # Scale the image to fit the window dimensions (1920x800)
            try:
                from PyQt6.QtGui import QPixmap
                from PyQt6.QtCore import Qt
                
                # Load and scale the background image to window size
                pixmap = QPixmap(background_path)
                scaled_pixmap = pixmap.scaled(1920, 1000, 
                                            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                            Qt.TransformationMode.SmoothTransformation)
                
                # Create a temporary file for the scaled image
                import tempfile
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, "startup_background.png")
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
            print(f"Background image not found at: {background_path}")
            print("Using fallback gradient background")
            # Fallback gradient background
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFB366, stop:1 #FF8C42);
                }
            """)
    
    def get_available_images(self):
        """Get list of available PNG images from the image_library folder."""
        image_library_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "image_library")
        print(f"Looking for images in: {image_library_path}")
        images = []
        
        if os.path.exists(image_library_path):
            print(f"Image library path exists")
            for file in os.listdir(image_library_path):
                if file.lower().endswith('.png'):
                    images.append(file)
            print(f"Found {len(images)} PNG images")
        else:
            print(f"Image library path does not exist")
        
        return sorted(images)
    
    def select_all_images(self):
        """Select all image checkboxes."""
        for var in self.image_vars.values():
            var.setChecked(True)
    
    def deselect_all_images(self):
        """Deselect all image checkboxes."""
        for var in self.image_vars.values():
            var.setChecked(False)
    
    def toggle_area(self, area_name, checked):
        """Toggle the visibility of a specific area overlay."""
        if checked:
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
            overlay = TransparentAreaOverlay(x, y, width, height, area_name)
            overlay.show()
            
            # Store the overlay
            self.area_overlays[area_name] = overlay
            
        except Exception as e:
            print(f"Error showing overlay for {area_name}: {e}")
    
    def hide_area_overlay(self, area_name):
        """Hide the overlay for a specific area."""
        if area_name in self.area_overlays:
            self.area_overlays[area_name].close()
            del self.area_overlays[area_name]
    
    def select_all_areas(self):
        """Select all area checkboxes and show all overlays."""
        for area_name, var in self.area_vars.items():
            var.setChecked(True)
    
    def deselect_all_areas(self):
        """Deselect all area checkboxes and hide all overlays."""
        for area_name, var in self.area_vars.items():
            var.setChecked(False)
        for overlay in self.area_overlays.values():
            overlay.close()
        self.area_overlays.clear()
    
    def clear_all_overlays(self):
        """Clear all overlays from screen."""
        for overlay in self.area_overlays.values():
            overlay.close()
        self.area_overlays.clear()
        
        # Also deselect all checkboxes
        for var in self.area_vars.values():
            var.setChecked(False)
    
    def update_image_layout(self):
        """Update the image layout based on available width."""
        if self.image_scroll_layout is None or len(self.image_checkboxes) == 0:
            return
        
        # Clear existing layout
        for i in reversed(range(self.image_scroll_layout.count())):
            widget = self.image_scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Determine number of columns based on window width
        window_width = self.width()
        if window_width < 1200:
            num_columns = 1
        elif window_width < 1600:
            num_columns = 2
        else:
            num_columns = 3
        
        # Recreate layout with new column count
        for i, checkbox in enumerate(self.image_checkboxes):
            row = i // num_columns
            col = i % num_columns
            self.image_scroll_layout.addWidget(checkbox, row, col)
        
        print(f"Image layout updated: {num_columns} columns for {window_width}px width")
    
    def run_image_test(self):
        """Run the image test with selected parameters."""
        print("\n" + "="*60)
        print("STARTING IMAGE TEST")
        print("="*60)
        
        # Get selected areas
        selected_areas = [name for name, var in self.area_vars.items() if var.isChecked()]
        
        if not selected_areas:
            QMessageBox.warning(self, "Warning", "Please select at least one screen area to test.")
            return
        
        # Get selected images
        selected_images = [name for name, var in self.image_vars.items() if var.isChecked()]
        custom_image = self.custom_image_var.text().strip()
        
        if not selected_images and not custom_image:
            QMessageBox.warning(self, "Warning", "Please select at least one image or enter a custom path.")
            return
        
        # Add custom image if provided
        if custom_image:
            selected_images.append(custom_image)
        
        # Get method selection
        if not self.cv2_var.isChecked() and not self.cv3_var.isChecked():
            QMessageBox.warning(self, "Warning", "Please select at least one detection method (CV2 or CV3).")
            return
        
        # Get confidence threshold
        confidence = self.confidence_var.value() / 100.0
        
        print(f"Test Configuration:")
        print(f"  Areas: {', '.join(selected_areas)}")
        print(f"  Images: {', '.join(selected_images)}")
        print(f"  Confidence: {confidence:.2f}")
        print(f"  CV2: {self.cv2_var.isChecked()}")
        print(f"  CV3: {self.cv3_var.isChecked()}")
        
        # Create log directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join("logs", f"image_test_{timestamp}")
        os.makedirs(log_dir, exist_ok=True)
        
        print(f"\nLog directory created: {log_dir}")
        
        # Create log file
        log_file = os.path.join(log_dir, "test_results.txt")
        
        # Run tests for each image in each area
        total_tests = len(selected_images) * len(selected_areas)
        current_test = 0
        
        with open(log_file, 'w') as f:
            f.write(f"Image Test Results - {timestamp}\n")
            f.write("="*60 + "\n")
            f.write(f"Areas: {', '.join(selected_areas)}\n")
            f.write(f"Images: {', '.join(selected_images)}\n")
            f.write(f"Confidence: {confidence:.2f}\n")
            f.write(f"CV2: {self.cv2_var.isChecked()}\n")
            f.write(f"CV3: {self.cv3_var.isChecked()}\n\n")
            
            for image_name in selected_images:
                # Handle both library images and custom paths
                if os.path.exists(image_name):
                    image_path = image_name
                else:
                    # Assume it's a library image
                    image_path = os.path.join("image_library", image_name)
                
                if not os.path.exists(image_path):
                    print(f"  ✗ Image not found: {image_path}")
                    f.write(f"✗ Image not found: {image_path}\n")
                    continue
                
                print(f"\nTesting image: {image_name}")
                f.write(f"\nImage: {image_name}\n")
                f.write("-" * 40 + "\n")
                
                for area_name in selected_areas:
                    current_test += 1
                    print(f"  [{current_test}/{total_tests}] Testing area: {area_name}")
                    f.write(f"Area: {area_name}\n")
                    
                    try:
                        # Test the area
                        results = self.test_single_area(image_path, area_name, confidence, log_dir, f)
                        
                        if results:
                            print(f"    ✓ Test completed successfully")
                            f.write(f"  [OK] Test completed successfully\n")
                        else:
                            print(f"    ✗ Test failed")
                            f.write(f"  [FAIL] Test failed\n")
                            
                    except Exception as e:
                        error_msg = f"Error testing {area_name} with {image_name}: {e}"
                        print(f"    ✗ {error_msg}")
                        f.write(f"  [ERROR] {error_msg}\n")
        
        print(f"\n" + "="*60)
        print(f"TEST COMPLETED - {total_tests} tests run")
        print(f"Results saved to: {log_dir}")
        print("="*60)
        
        # Show completion message
        QMessageBox.information(self, "Test Complete", 
                               f"Image test completed!\n"
                               f"Total tests: {total_tests}\n"
                               f"Results saved to: {log_dir}")
    
    def test_single_area(self, image_path, area_name, confidence, log_dir, log_file):
        """Test a single image in a single area with all selected methods."""
        print(f"    Testing {os.path.basename(image_path)} in {area_name}")
        log_file.write(f"  Testing {os.path.basename(image_path)} in {area_name}\n")
        
        # Get region coordinates
        try:
            region = self.si.get_scan_area(area_name)
            print(f"      Region coordinates: {region}")
            log_file.write(f"    Region coordinates: {region}\n")
        except Exception as e:
            error_msg = f"Failed to get region coordinates: {e}"
            print(f"      ✗ {error_msg}")
            log_file.write(f"    ✗ {error_msg}\n")
            return None
        
        # Take screenshot of the region
        try:
            screenshot = pyautogui.screenshot(region=region)
            screenshot_filename = os.path.join(log_dir, f"{area_name}_{os.path.basename(image_path)}_screenshot.png")
            screenshot.save(screenshot_filename)
            print(f"      Screenshot saved: {screenshot_filename}")
            log_file.write(f"    Screenshot saved: {screenshot_filename}\n")
        except Exception as e:
            error_msg = f"Failed to take screenshot: {e}"
            print(f"      ✗ {error_msg}")
            log_file.write(f"    ✗ {error_msg}\n")
            return None
        
        # Convert screenshot to CV2 format
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Load template image
        template = cv2.imread(image_path)
        if template is None:
            error_msg = f"Failed to load template image: {image_path}"
            print(f"      ✗ {error_msg}")
            log_file.write(f"    ✗ {error_msg}\n")
            return None
        
        results = {}
        
        # Test CV2 if selected
        if self.cv2_var.isChecked():
            print(f"      Testing CV2...")
            log_file.write(f"    Testing CV2...\n")
            cv2_results = self.test_cv2(screenshot_cv, template, region, confidence)
            results['CV2'] = cv2_results
            
            # Save CV2 annotated image
            if cv2_results['found']:
                cv2_annotated = screenshot_cv.copy()
                self.annotate_cv2_results(cv2_annotated, cv2_results, template)
                cv2_filename = os.path.join(log_dir, f"{area_name}_{os.path.basename(image_path)}_cv2_annotated.png")
                cv2.imwrite(cv2_filename, cv2_annotated)
                print(f"        CV2 annotated image saved: {cv2_filename}")
                log_file.write(f"      CV2 annotated image saved: {cv2_filename}\n")
        
        # Test CV3 variations if selected
        if self.cv3_var.isChecked():
            print(f"      Testing CV3 variations...")
            log_file.write(f"    Testing CV3 variations...\n")
            cv3_results = {}
            
            for var_name, var_data in self.cv3_variations.items():
                if var_data["var"].isChecked():  # Only test selected variations
                    print(f"        Testing {var_name} (Shape: {var_data['shape']}, Color: {var_data['color']})")
                    log_file.write(f"      Testing {var_name} (Shape: {var_data['shape']}, Color: {var_data['color']})\n")
                    
                    result = self.test_cv3(image_path, region, 
                                          self.shape_threshold_var.value() / 100.0,
                                          self.color_threshold_var.value() / 100.0,
                                          var_data['shape'], var_data['color'])
                    cv3_results[var_name] = result
                    
                    # Save CV3 annotated image if found
                    if result['found']:
                        cv3_annotated = screenshot_cv.copy()
                        self.annotate_cv3_results(cv3_annotated, result, template, region)
                        cv3_filename = os.path.join(log_dir, f"{area_name}_{os.path.basename(image_path)}_{var_name}_cv3_annotated.png")
                        cv2.imwrite(cv3_filename, cv3_annotated)
                        print(f"          CV3 annotated image saved: {cv3_filename}")
                        log_file.write(f"        CV3 annotated image saved: {cv3_filename}\n")
            
            results['CV3'] = cv3_results
        
        # Log summary
        self.log_test_summary(results, log_file)
        
        return results
    
    def test_cv2(self, screenshot_cv, template, region, confidence):
        """Test CV2 template matching."""
        try:
            # Use CV2 template matching directly for more control
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            print(f"        CV2 max match value: {max_val:.4f}")
            
            if max_val >= confidence:
                # Calculate center point relative to the screenshot region
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                print(f"        CV2 Success - Found at ({center_x}, {center_y}) with score {max_val:.4f}")
                
                return {
                    'found': True,
                    'coordinates': (center_x, center_y),  # Return region-relative coordinates
                    'confidence': max_val,
                    'method': 'CV2'
                }
            else:
                print(f"        CV2 Failed - No valid match found above threshold {confidence}")
                return {
                    'found': False,
                    'confidence': max_val,
                    'method': 'CV2'
                }
                
        except Exception as e:
            print(f"        CV2 Error: {e}")
            return {
                'found': False,
                'error': str(e),
                'method': 'CV2'
            }
    
    def test_cv3(self, image_path, region, shape_threshold, color_threshold, shape_weight, color_weight):
        """Test CV3 enhanced matching."""
        try:
            # Use ScreenInteractor's CV3 method
            result = self.si.find_image_cv3(
                image_path, 
                region=region, 
                threshold=min(shape_threshold, color_threshold),  # Use the lower of the two thresholds
                shape_weight=shape_weight,
                color_weight=color_weight
            )
            
            if result:
                # CV3 returns screen coordinates
                print(f"        CV3 Success - Found valid match at {result} with thresholds S:{shape_threshold:.2f}, C:{color_threshold:.2f}")
                return {
                    'found': True,
                    'coordinates': result,  # These are screen coordinates
                    'shape_threshold': shape_threshold,
                    'color_threshold': color_threshold,
                    'shape_weight': shape_weight,
                    'color_weight': color_weight,
                    'method': 'CV3',
                    'is_screen_coords': True  # Flag to indicate these are screen coordinates
                }
            else:
                print(f"        CV3 Failed - No valid match found with thresholds S:{shape_threshold:.2f}, C:{color_threshold:.2f}")
                return {
                    'found': False,
                    'shape_threshold': shape_threshold,
                    'color_threshold': color_threshold,
                    'shape_weight': shape_weight,
                    'color_weight': color_weight,
                    'method': 'CV3',
                    'is_screen_coords': False
                }
                
        except Exception as e:
            print(f"        CV3 Error: {e}")
            return {
                'found': False,
                'error': str(e),
                'shape_threshold': shape_threshold,
                'color_threshold': color_threshold,
                'shape_weight': shape_weight,
                'color_weight': color_weight,
                'method': 'CV3',
                'is_screen_coords': False
            }
    
    def annotate_cv2_results(self, image, results, template):
        """Annotate CV2 results on the image."""
        if not results['found']:
            return
        
        # Get coordinates - handle both tuple and single coordinate formats
        coords = results['coordinates']
        if isinstance(coords, (list, tuple)) and len(coords) >= 2:
            x, y = coords[0], coords[1]
        else:
            print(f"Warning: Unexpected CV2 coordinate format: {coords}")
            return
        
        h, w = template.shape[:2]
        
        # Draw rectangle around match (convert to int for OpenCV)
        x, y = int(x), int(y)
        
        # Calculate rectangle corners relative to the screenshot (not screen coordinates)
        # Since we're working with the screenshot image, coordinates are relative to the region
        x1, y1 = max(0, x - w//2), max(0, y - h//2)
        x2, y2 = min(image.shape[1], x + w//2), min(image.shape[0], y + h//2)
        
        # Draw rectangle around match
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        # Draw confidence text
        cv2.putText(image, f"CV2: {results['confidence']:.2f}", 
                   (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        print(f"CV2 annotation: Drew rectangle at ({x1},{y1}) to ({x2},{y2})")
    
    def annotate_cv3_results(self, image, results, template, region):
        """Annotate CV3 results on the image."""
        if not results['found']:
            return
        
        # Get coordinates - handle both tuple and single coordinate formats
        coords = results['coordinates']
        if isinstance(coords, (list, tuple)) and len(coords) >= 2:
            x, y = coords[0], coords[1]
        else:
            print(f"Warning: Unexpected CV3 coordinate format: {coords}")
            return
        
        h, w = template.shape[:2]
        
        # Draw rectangle around match (convert to int for OpenCV)
        x, y = int(x), int(y)
        
        # CV3 returns screen coordinates, but we need region-relative coordinates for annotation
        # Since we're working with the screenshot image, we need to convert
        if results.get('is_screen_coords', False):
            # These are screen coordinates, convert to region-relative
            # The screenshot was taken from the region, so we need to subtract region offset
            region_x, region_y = region[0], region[1]  # Region top-left corner
            x = x - region_x  # Convert screen x to region-relative x
            y = y - region_y  # Convert screen y to region-relative y
            print(f"CV3 annotation: Converted screen coords ({x + region_x},{y + region_y}) to region coords ({x},{y})")
        
        # Calculate rectangle corners relative to the screenshot (not screen coordinates)
        # Since we're working with the screenshot image, coordinates are relative to the region
        x1, y1 = max(0, x - w//2), max(0, y - h//2)
        x2, y2 = min(image.shape[1], x + w//2), min(image.shape[0], y + h//2)
        
        # Draw rectangle around match
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
        
        # Draw confidence and weight text
        text = f"CV3: S:{results['shape_threshold']:.2f}, C:{results['color_threshold']:.2f} (W:S:{results['shape_weight']:.1f}, C:{results['color_weight']:.1f})"
        cv2.putText(image, text, (x1, y1-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        print(f"CV3 annotation: Drew rectangle at ({x1},{y1}) to ({x2},{y2})")
    
    def log_test_summary(self, results, log_file):
        """Log a summary of test results."""
        log_file.write(f"    Test Summary:\n")
        
        if 'CV2' in results:
            cv2_result = results['CV2']
            if cv2_result['found']:
                log_file.write(f"      CV2: Found at {cv2_result['coordinates']} (confidence: {cv2_result['confidence']:.4f})\n")
            else:
                log_file.write(f"      CV2: Not found")
                if 'confidence' in cv2_result:
                    log_file.write(f" (best match: {cv2_result['confidence']:.4f})")
                if 'error' in cv2_result:
                    log_file.write(f" (Error: {cv2_result['error']})")
                log_file.write(f"\n")
        
        if 'CV3' in results:
            log_file.write(f"      CV3 Results:\n")
            for var_name, cv3_result in results['CV3'].items():
                if cv3_result['found']:
                    log_file.write(f"        {var_name}: Found at {cv3_result['coordinates']} (S:{cv3_result['shape_threshold']:.2f}, C:{cv3_result['color_threshold']:.2f})\n")
                else:
                    log_file.write(f"        {var_name}: Not found (S:{cv3_result['shape_threshold']:.2f}, C:{cv3_result['color_threshold']:.2f})")
                    if 'error' in cv3_result:
                        log_file.write(f" (Error: {cv3_result['error']})")
                    log_file.write(f"\n")

    def on_resize(self, event):
        """Handle window resize to adjust background scaling - much more efficient now."""
        # Cancel any pending resize timer
        if self.resize_timer:
            self.resize_timer.stop()
        
        # Set a new timer to delay the actual resize operation
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(lambda: self._delayed_resize())
        self.resize_timer.start(300)  # Wait 300ms after resize stops
    
    def _delayed_resize(self):
        """Actually perform the background resize after the delay."""
        new_width = self.width()
        new_height = self.height()
        
        # Only resize background if the change is significant (more than 50px)
        if (abs(new_width - self.last_window_size[0]) < 50 and 
            abs(new_height - self.last_window_size[1]) < 50):
            self.last_window_size = (new_width, new_height)
            return
        
        # Only resize background if the change is substantial (more than 100px)
        if (abs(new_width - self.last_window_size[0]) < 100 and 
            abs(new_height - self.last_window_size[1]) < 100):
            self.last_window_size = (new_width, new_height)
            return
        
        print(f"Window resized significantly: {new_width}x{new_height}")
        
        # Update background with new size
        self.update_background_size(new_width, new_height)
        
        self.last_window_size = (new_width, new_height)
    
    def update_background_size(self, width, height):
        """Update the background image size for the new window dimensions."""
        if os.path.exists(self.original_background_path):
            try:
                from PyQt6.QtGui import QPixmap
                from PyQt6.QtCore import Qt
                
                # Load and scale the background image
                pixmap = QPixmap(self.original_background_path)
                scaled_pixmap = pixmap.scaled(width, height, 
                                            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                            Qt.TransformationMode.SmoothTransformation)
                
                # Create a temporary file for the scaled image
                import tempfile
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, "temp_background.png")
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
                css_path = self.original_background_path.replace('\\', '/')
                self.setStyleSheet(f"""
                    QMainWindow {{
                        background-image: url("{css_path}");
                        background-position: center;
                        background-repeat: no-repeat;
                    }}
                """)
        else:
            print(f"Background image not found at: {self.original_background_path}")
            print("Using fallback gradient background")
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #FFB366, stop:1 #FF8C42);
                }
            """)

def main():
    """Main function to run the PyQt6 combined image tester."""
    print("Starting Combined Image Tester (PyQt6)...")
    print("This tool combines area testing with CV2 and CV3 image detection.")
    print("Features:")
    print("- Native PyQt6 translucent panels with blur effects")
    print("- Visual area overlays with click-through borders")
    print("- Multiple image selection with column layout")
    print("- 6 predefined CV3 weight variations")
    print("- Modern UI with smooth animations")
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = CombinedImageTesterPyQt6()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
