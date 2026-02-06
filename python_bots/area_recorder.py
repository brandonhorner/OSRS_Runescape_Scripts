#!/usr/bin/env python3
# area_recorder.py
# Tool for recording screen areas with overlay drawing and multi-resolution support

import sys
import os
import time
import json
import pyautogui
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QScrollArea, QFrame, QSpinBox, QLineEdit, 
                             QMessageBox, QFileDialog, QGridLayout, QComboBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QRect, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPalette, QBrush, QPen

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from screen_interactor import ScreenInteractor

class AreaOverlay(QWidget):
    """Transparent overlay for drawing areas."""
    
    # Custom signal for closing
    closing = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # Use proper window flags for overlay behavior
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.Tool | 
                           Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        # Make the overlay capture ALL mouse events across the entire screen
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        
        # Ensure the overlay captures all events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()
        
        # Ensure the overlay is always on top and captures events
        
        # Make it cover the entire screen
        screen = QApplication.primaryScreen()
        self.setGeometry(screen.geometry())
        
        # Ensure the overlay stays on top and captures events
        self.raise_()
        self.activateWindow()
        
        # Force the overlay to capture all events
        self.grabMouse()
        self.grabKeyboard()
        
        # Drawing state
        self.drawing = False
        self.start_point = None
        self.current_rect = None
        self.areas = []  # List of drawn areas
        self.area_names = []  # Names for each area
        
        # Visual settings
        self.area_colors = [
            QColor(255, 0, 0, 180),      # Red
            QColor(0, 255, 0, 180),      # Green
            QColor(0, 0, 255, 180),      # Blue
            QColor(255, 255, 0, 180),    # Yellow
            QColor(255, 0, 255, 180),    # Magenta
            QColor(0, 255, 255, 180),    # Cyan
            QColor(255, 165, 0, 180),    # Orange
            QColor(128, 0, 128, 180),    # Purple
        ]
        
        # Instructions
        self.instructions = [
            "Click and drag to draw areas",
            "Right-click to delete last area",
            "Press 'S' to save areas",
            "Press 'C' to clear all areas",
            "Press 'ESC' to close overlay"
        ]
        
        # Add a status label for better visibility
        self.status_text = "Overlay Active - Draw areas or press ESC to close"
        
        # Set up a timer to keep the overlay on top
        self.stay_on_top_timer = QTimer()
        self.stay_on_top_timer.timeout.connect(self.ensure_on_top)
        self.stay_on_top_timer.start(1000)  # Check every second
        
        # Track if we're actively drawing to adjust transparency
        self.is_drawing_active = False
        
    def showEvent(self, event):
        """Handle show event to ensure event capture."""
        super().showEvent(event)
        print("Overlay shown - ensuring event capture...")
        
        # Ensure we capture all events immediately
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.grabMouse()
        self.grabKeyboard()
        
    def ensure_on_top(self):
        """Ensure the overlay stays on top."""
        if self.isVisible():
            self.raise_()
            self.activateWindow()
            self.setFocus()  # Always maintain focus
            
            # Make overlay more transparent when not actively drawing
            if not self.is_drawing_active and not self.drawing:
                # Reduce opacity when idle
                self.setWindowOpacity(0.3)
            else:
                # Full opacity when drawing
                self.setWindowOpacity(1.0)
        
    def mousePressEvent(self, event):
        """Handle mouse press events."""
        # Always accept mouse events to prevent them from passing through
        event.accept()
        
        # Ensure we have focus for keyboard events
        self.setFocus()
        
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.is_drawing_active = True
            self.start_point = event.pos()
            self.current_rect = QRect(self.start_point, self.start_point)
            # Reset opacity when starting to draw
            self.setWindowOpacity(1.0)
            print(f"Started drawing at ({self.start_point.x()}, {self.start_point.y()})")
        elif event.button() == Qt.MouseButton.RightButton:
            if self.areas:
                removed_area = self.areas.pop()
                removed_name = self.area_names.pop()
                print(f"Removed area: {removed_name} at {removed_area.x()}, {removed_area.y()}")
                self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        # Always accept mouse events
        event.accept()
        
        # Maintain focus while drawing
        if self.drawing:
            self.setFocus()
        
        if self.drawing and self.start_point:
            self.current_rect = QRect(self.start_point, event.pos()).normalized()
            # Keep full opacity while drawing
            self.setWindowOpacity(1.0)
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        # Always accept mouse events
        event.accept()
        
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            self.is_drawing_active = False
            if self.current_rect and self.current_rect.width() > 10 and self.current_rect.height() > 10:
                # Add the area
                self.areas.append(self.current_rect)
                
                # Generate a name for the area
                area_name = f"area_{len(self.areas)}"
                self.area_names.append(area_name)
                
                print(f"Area {len(self.areas)} drawn: {self.current_rect.x()}, {self.current_rect.y()}, {self.current_rect.width()}, {self.current_rect.height()}")
                
                # Update status
                self.status_text = f"Area {len(self.areas)} drawn - Press ESC to finish or continue drawing"
            else:
                print("Area too small, not added")
                self.status_text = "Area too small - Draw larger areas"
            
            self.current_rect = None
            self.update()
    
    def keyPressEvent(self, event):
        """Handle key press events."""
        # Always accept key events
        event.accept()
        
        if event.key() == Qt.Key.Key_S:
            print("Saving areas...")
            self.save_areas()
        elif event.key() == Qt.Key.Key_C:
            print("Clearing all areas...")
            self.clear_areas()
        elif event.key() == Qt.Key.Key_Escape:
            print("Closing overlay...")
            self.close()
        else:
            print(f"Key pressed: {event.key()}")
    
    def focusInEvent(self, event):
        """Handle focus in events."""
        super().focusInEvent(event)
        print("Overlay gained focus")
    
    def focusOutEvent(self, event):
        """Handle focus out events."""
        super().focusOutEvent(event)
        print("Overlay lost focus - attempting to regain...")
        
        # Try to regain focus and re-grab events
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.grabMouse()
        self.grabKeyboard()
        
    def closeEvent(self, event):
        """Handle close event to clean up timer."""
        print("Overlay closeEvent triggered")
        
        # Release event grabs
        self.releaseMouse()
        self.releaseKeyboard()
        
        if hasattr(self, 'stay_on_top_timer'):
            self.stay_on_top_timer.stop()
        
        # Emit closing signal before closing
        self.closing.emit()
        
        super().closeEvent(event)
        
    def save_areas(self):
        """Save the current areas."""
        if not self.areas:
            return
        
        # Create data structure
        areas_data = []
        for i, (rect, name) in enumerate(zip(self.areas, self.area_names)):
            area_data = {
                "name": name,
                "x": rect.x(),
                "y": rect.y(),
                "width": rect.width(),
                "height": rect.height(),
                "screen_resolution": f"{self.width()}x{self.height()}"
            }
            areas_data.append(area_data)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recorded_areas_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(areas_data, f, indent=2)
            print(f"Areas saved to {filename}")
        except Exception as e:
            print(f"Error saving areas: {e}")
    
    def clear_areas(self):
        """Clear all drawn areas."""
        self.areas.clear()
        self.area_names.clear()
        self.update()
        print("All areas cleared")
    
    def paintEvent(self, event):
        """Custom paint event to draw areas and instructions."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Don't draw a background over the entire screen - this was causing the red layer effect
        # Only draw UI elements and areas
        
        # Draw existing areas
        for i, rect in enumerate(self.areas):
            color = self.area_colors[i % len(self.area_colors)]
            painter.setPen(QPen(color, 3))
            painter.setBrush(QBrush(color.lighter(150)))
            painter.drawRect(rect)
            
            # Draw area number
            painter.setPen(QColor(0, 0, 0, 255))
            painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            painter.drawText(rect.center(), str(i + 1))
            
            # Draw coordinates
            coord_text = f"({rect.x()}, {rect.y()}) {rect.width()}x{rect.height()}"
            painter.setPen(QColor(0, 0, 0, 255))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(rect.x(), rect.y() - 5, coord_text)
        
        # Draw current drawing rectangle
        if self.current_rect:
            painter.setPen(QPen(QColor(255, 255, 255, 255), 2, Qt.PenStyle.DashLine))
            painter.setBrush(QBrush(QColor(255, 255, 255, 50)))
            painter.drawRect(self.current_rect)
        
        # Draw a prominent status bar at the top
        status_rect = QRect(0, 0, self.width(), 60)
        painter.fillRect(status_rect, QColor(0, 0, 0, 180))
        
        # Draw status text
        painter.setPen(QColor(255, 255, 255, 255))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        painter.drawText(20, 25, self.status_text)
        
        # Draw instructions in a more visible box
        instructions_rect = QRect(20, 80, 300, 120)
        painter.fillRect(instructions_rect, QColor(0, 0, 0, 180))
        painter.setPen(QColor(255, 255, 255, 255))
        painter.setFont(QFont("Arial", 10))
        
        y_offset = 100
        for instruction in self.instructions:
            painter.drawText(30, y_offset, instruction)
            y_offset += 20
        
        # Draw area count in the instructions box
        painter.drawText(30, y_offset + 10, f"Areas drawn: {len(self.areas)}")
        
        # Draw a very subtle border around the entire overlay to make it more visible
        # Use almost transparent white to avoid overwhelming the screen
        painter.setPen(QPen(QColor(255, 255, 255, 30), 1))  # Very low opacity
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

class TranslucentPanel(QFrame):
    """A translucent panel with modern styling."""
    
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setObjectName("TranslucentPanel")
        self.color = color
        self.setup_style()
        
    def setup_style(self):
        """Setup the modern styling with translucent panels."""
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
            
            QPushButton#startButton {{
                background: rgba(34, 139, 34, 0.9);
                font-size: 14px;
                padding: 12px 24px;
            }}
            
            QPushButton#startButton:hover {{
                background: rgba(34, 139, 34, 1.0);
            }}
            
            QTextEdit {{
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(70, 130, 180, 0.5);
                border-radius: 8px;
                color: rgba(0, 0, 0, 0.9);
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }}
            
            QComboBox {{
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(70, 130, 180, 0.5);
                border-radius: 6px;
                padding: 6px;
                color: rgba(0, 0, 0, 0.9);
            }}
        """)

class AreaRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Area Recorder")
        self.setGeometry(100, 100, 1200, 800)
        
        # Screen interactor for area calculations
        self.si = ScreenInteractor()
        
        # Current screen resolution
        self.current_resolution = pyautogui.size()
        
        # Target resolutions for conversion
        self.target_resolutions = [
            (1920, 1080),   # 1080p
            (2560, 1440),   # 1440p
            (3840, 2160),   # 4K
            (1366, 768),    # Laptop
            (1600, 900),    # HD+
        ]
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Screen Area Recorder")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 0, 0, 0.9);
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
        
        # Left panel - Controls
        self.controls_panel = self.create_controls_panel()
        panels_layout.addWidget(self.controls_panel, stretch=1)
        
        # Center panel - Area Display
        self.display_panel = self.create_display_panel()
        panels_layout.addWidget(self.display_panel, stretch=2)
        
        # Right panel - Code Generation
        self.code_panel = self.create_code_panel()
        panels_layout.addWidget(self.code_panel, stretch=2)
        
        main_layout.addLayout(panels_layout)
        
        # Bottom panel - Actions
        self.create_bottom_panel(main_layout)
        
    def create_controls_panel(self):
        """Create the controls panel."""
        panel = TranslucentPanel((230, 243, 255))  # Soft light blue
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Controls")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Start overlay button
        start_btn = QPushButton("Start Area Overlay")
        start_btn.setObjectName("startButton")
        start_btn.clicked.connect(self.start_overlay)
        layout.addWidget(start_btn)
        
        # Load areas button
        load_btn = QPushButton("Load Areas")
        load_btn.clicked.connect(self.load_areas)
        layout.addWidget(load_btn)
        
        # Clear areas button
        clear_btn = QPushButton("Clear Areas")
        clear_btn.clicked.connect(self.clear_areas)
        layout.addWidget(clear_btn)
        
        # Resolution info
        res_label = QLabel("Current Resolution:")
        res_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(res_label)
        
        self.resolution_label = QLabel(f"{self.current_resolution.width} x {self.current_resolution.height}")
        layout.addWidget(self.resolution_label)
        
        # Target resolution selector
        target_label = QLabel("Target Resolution:")
        target_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(target_label)
        
        self.target_combo = QComboBox()
        for width, height in self.target_resolutions:
            self.target_combo.addItem(f"{width} x {height}")
        self.target_combo.currentTextChanged.connect(self.update_conversions)
        layout.addWidget(self.target_combo)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Add emergency close button
        emergency_label = QLabel("Emergency Close:")
        emergency_label.setStyleSheet("font-weight: bold; margin-top: 20px; color: rgba(139, 0, 0, 0.9);")
        layout.addWidget(emergency_label)
        
        emergency_btn = QPushButton("Force Close Overlay")
        emergency_btn.setStyleSheet("background: rgba(139, 0, 0, 0.9);")
        emergency_btn.clicked.connect(self.force_close_overlay)
        layout.addWidget(emergency_btn)
        
        return panel
        
    def create_display_panel(self):
        """Create the area display panel."""
        panel = TranslucentPanel((255, 242, 230))  # Soft sunset yellow-orange
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Recorded Areas")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Areas display
        self.areas_display = QTextEdit()
        self.areas_display.setReadOnly(True)
        self.areas_display.setMaximumHeight(300)
        layout.addWidget(self.areas_display)
        
        # Instructions
        instructions = QLabel(
            "Instructions:\n"
            "1. Click 'Start Area Overlay' to begin drawing\n"
            "2. Click and drag to draw areas on screen\n"
            "3. Right-click to delete last area\n"
            "4. Press 'S' to save areas\n"
            "5. Press 'ESC' to close overlay"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: rgba(0, 0, 0, 0.8); font-size: 11px; margin-top: 10px;")
        layout.addWidget(instructions)
        
        return panel
        
    def create_code_panel(self):
        """Create the code generation panel."""
        panel = TranslucentPanel((230, 247, 230))  # Soft green
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Generated Code")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Code display
        self.code_display = QTextEdit()
        self.code_display.setReadOnly(True)
        layout.addWidget(self.code_display)
        
        # Copy button
        copy_btn = QPushButton("Copy Code")
        copy_btn.clicked.connect(self.copy_code)
        layout.addWidget(copy_btn)
        
        return panel
        
    def create_bottom_panel(self, main_layout):
        """Create the bottom panel."""
        bottom_panel = TranslucentPanel((240, 240, 240))  # Light gray
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(20, 15, 20, 15)
        
        # Status label
        self.status_label = QLabel("Ready to record areas")
        self.status_label.setStyleSheet("font-weight: bold;")
        bottom_layout.addWidget(self.status_label)
        
        # Add stretch to push buttons to the right
        bottom_layout.addStretch()
        
        # Export button
        export_btn = QPushButton("Export Areas")
        export_btn.clicked.connect(self.export_areas)
        bottom_layout.addWidget(export_btn)
        
        # Save button
        save_btn = QPushButton("Save Areas")
        save_btn.clicked.connect(self.save_areas)
        bottom_layout.addWidget(save_btn)
        
        main_layout.addWidget(bottom_panel)
        
    def start_overlay(self):
        """Start the area overlay."""
        print("Starting area overlay...")
        self.hide()  # Hide the main window
        time.sleep(1)  # Brief delay
        
        # Create and show the overlay
        self.overlay = AreaOverlay()
        
        # Connect overlay signals BEFORE showing
        self.overlay.destroyed.connect(self.on_overlay_closed)
        self.overlay.closing.connect(self.on_overlay_closing)
        
        # Also connect to the overlay's closeEvent to ensure we get notified
        self.overlay.closeEvent = lambda event: self._overlay_close_event(event)
        
        # Show the overlay
        self.overlay.show()
        
        # Ensure the overlay is properly focused
        self.overlay.raise_()
        self.overlay.activateWindow()
        
        print("Overlay started - you should now see it on screen")
        self.status_label.setText("Overlay active - drawing areas...")
        
        # Add a reminder about how to close
        print("REMEMBER: Press ESC to close the overlay when you're done!")
        
        # Set up a fallback timer to check if overlay is still active
        self.fallback_timer = QTimer()
        self.fallback_timer.timeout.connect(self.check_overlay_status)
        self.fallback_timer.start(2000)  # Check every 2 seconds instead of 5
        
        # Also set up a more aggressive timer for immediate response
        self.immediate_timer = QTimer()
        self.immediate_timer.timeout.connect(self.immediate_overlay_check)
        self.immediate_timer.start(500)  # Check every 500ms for immediate response
        
    def check_overlay_status(self):
        """Fallback check to ensure overlay is still active."""
        if hasattr(self, 'overlay') and self.overlay and self.overlay.isVisible():
            print("Overlay is still active and visible")
        else:
            print("Overlay not found or not visible - restoring main window")
            self.fallback_timer.stop()
            if hasattr(self, 'immediate_timer'):
                self.immediate_timer.stop()
            
            # Try to get areas before cleanup
            if hasattr(self, 'overlay') and self.overlay:
                try:
                    self.areas = self.overlay.areas.copy()
                    self.area_names = self.overlay.area_names.copy()
                    print(f"Retrieved {len(self.areas)} areas from fallback check")
                except Exception as e:
                    print(f"Error retrieving areas in fallback: {e}")
                    self.areas = []
                    self.area_names = []
                
                # Clean up overlay
                self.overlay = None
            
            # Show main window
            self.show()
            self.raise_()
            self.activateWindow()
            
            # Update displays if we have areas
            if hasattr(self, 'areas') and self.areas:
                self.update_displays()
            
            self.status_label.setText("Overlay restored via fallback - areas retrieved")
        
    def immediate_overlay_check(self):
        """Immediate check for overlay status - more aggressive than fallback."""
        if not hasattr(self, 'overlay') or not self.overlay or not self.overlay.isVisible():
            print("Immediate check: Overlay not active - restoring main window")
            self.immediate_timer.stop()
            self.fallback_timer.stop()
            
            # Try to get areas if overlay still exists
            if hasattr(self, 'overlay') and self.overlay:
                try:
                    self.areas = self.overlay.areas.copy()
                    self.area_names = self.overlay.area_names.copy()
                    print(f"Retrieved {len(self.areas)} areas from immediate check")
                except Exception as e:
                    print(f"Error retrieving areas in immediate check: {e}")
                    self.areas = []
                    self.area_names = []
                
                # Clean up overlay
                self.overlay = None
            
            # Show main window
            self.show()
            self.raise_()
            self.activateWindow()
            
            # Update displays if we have areas
            if hasattr(self, 'areas') and self.areas:
                self.update_displays()
            
            self.status_label.setText("Overlay restored via immediate check - areas retrieved")
        
    def _overlay_close_event(self, event):
        """Direct override of overlay's closeEvent to ensure main window restoration."""
        print("Direct overlay closeEvent intercepted - restoring main window...")
        
        # Get areas before the overlay closes
        try:
            self.areas = self.overlay.areas.copy()
            self.area_names = self.overlay.area_names.copy()
            print(f"Retrieved {len(self.areas)} areas from direct closeEvent")
        except Exception as e:
            print(f"Error retrieving areas from direct closeEvent: {e}")
            self.areas = []
            self.area_names = []
        
        # Stop timers
        if hasattr(self, 'fallback_timer'):
            self.fallback_timer.stop()
        if hasattr(self, 'immediate_timer'):
            self.immediate_timer.stop()
        
        # Clean up overlay reference
        self.overlay = None
        
        # Show main window
        self.show()
        self.raise_()
        self.activateWindow()
        
        # Update displays if we have areas
        if hasattr(self, 'areas') and self.areas:
            self.update_displays()
        
        self.status_label.setText("Overlay closed directly - areas retrieved")
        
        # Accept the close event
        event.accept()
        

        
    def on_overlay_closing(self):
        """Handle overlay closing signal."""
        print("Overlay closing signal received...")
        
    def on_overlay_closed(self):
        """Handle overlay closure."""
        print("Overlay closed, restoring main window...")
        
        # Stop the timers
        if hasattr(self, 'fallback_timer'):
            self.fallback_timer.stop()
        if hasattr(self, 'immediate_timer'):
            self.immediate_timer.stop()
        
        # Get areas from overlay if it still exists
        if hasattr(self, 'overlay') and self.overlay:
            try:
                self.areas = self.overlay.areas.copy()
                self.area_names = self.overlay.area_names.copy()
                print(f"Retrieved {len(self.areas)} areas from overlay")
            except Exception as e:
                print(f"Error retrieving areas: {e}")
                self.areas = []
                self.area_names = []
        
        # Clean up overlay reference
        if hasattr(self, 'overlay'):
            self.overlay = None
        
        # Always show the main window
        self.show()
        self.raise_()
        self.activateWindow()
        
        # Update displays if we have areas
        if hasattr(self, 'areas') and self.areas:
            self.update_displays()
        
        self.status_label.setText("Overlay closed - areas recorded")
        print("Main window restored - areas have been recorded")
        
    def force_close_overlay(self):
        """Force close the overlay if it's stuck."""
        print("Force close overlay requested...")
        
        if hasattr(self, 'overlay') and self.overlay:
            print("Force closing overlay...")
            try:
                # Stop any timers
                if hasattr(self, 'fallback_timer'):
                    self.fallback_timer.stop()
                if hasattr(self, 'immediate_timer'):
                    self.immediate_timer.stop()
                
                # Close and cleanup overlay
                self.overlay.close()
                self.overlay.deleteLater()
                
                # Get areas before cleanup
                try:
                    self.areas = self.overlay.areas.copy()
                    self.area_names = self.overlay.area_names.copy()
                    print(f"Retrieved {len(self.areas)} areas from force-closed overlay")
                except Exception as e:
                    print(f"Error retrieving areas: {e}")
                    self.areas = []
                    self.area_names = []
                
                # Show main window
                self.show()
                self.raise_()
                self.activateWindow()
                
                # Update displays if we have areas
                if self.areas:
                    self.update_displays()
                
                self.status_label.setText("Overlay force closed - areas retrieved")
                
            except Exception as e:
                print(f"Error during force close: {e}")
                self.show()
                self.status_label.setText("Error during force close")
        else:
            print("No overlay to close")
            self.show()
            self.raise_()
            self.activateWindow()
            self.status_label.setText("No overlay active")
        
    def update_displays(self):
        """Update the area and code displays."""
        if not hasattr(self, 'areas'):
            return
            
        # Update areas display
        areas_text = ""
        for i, (rect, name) in enumerate(zip(self.areas, self.area_names)):
            areas_text += f"Area {i+1} ({name}):\n"
            areas_text += f"  X: {rect.x()}, Y: {rect.y()}\n"
            areas_text += f"  Width: {rect.width()}, Height: {rect.height()}\n"
            areas_text += f"  Screen: {rect.x()}, {rect.y()}, {rect.width()}, {rect.height()}\n\n"
        
        self.areas_display.setText(areas_text)
        
        # Update code generation
        self.update_conversions()
        
    def update_conversions(self):
        """Update the code conversions for different resolutions."""
        if not hasattr(self, 'areas') or not self.areas:
            return
            
        # Get target resolution
        target_text = self.target_combo.currentText()
        target_width, target_height = map(int, target_text.split(' x '))
        
        # Generate code
        code = self.generate_area_code(target_width, target_height)
        self.code_display.setText(code)
        
    def generate_area_code(self, target_width, target_height):
        """Generate code for the areas in the target resolution."""
        if not hasattr(self, 'areas'):
            return "No areas recorded"
            
        current_width = self.current_resolution.width
        current_height = self.current_resolution.height
        
        code = f"# Screen Areas for {target_width}x{target_height}\n"
        code += f"# Converted from {current_width}x{current_height}\n"
        code += f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        code += "def get_scan_area(self, label):\n"
        code += "    screen_width, screen_height = pyautogui.size()\n"
        code += "    \n"
        code += "    areas = {\n"
        
        for i, (rect, name) in enumerate(zip(self.areas, self.area_names)):
            # Calculate ratios
            x_ratio = rect.x() / current_width
            y_ratio = rect.y() / current_height
            w_ratio = rect.width() / current_width
            h_ratio = rect.height() / current_height
            
            # Calculate target coordinates
            target_x = int(x_ratio * target_width)
            target_y = int(y_ratio * target_height)
            target_w = int(w_ratio * target_width)
            target_h = int(h_ratio * target_height)
            
            code += f"        \"{name}\": (screen_width // {current_width} * {target_x}, "
            code += f"screen_height // {current_height} * {target_y}, "
            code += f"screen_width // {current_width} * {target_w}, "
            code += f"screen_height // {current_height} * {target_h}),\n"
        
        code += "    }\n"
        code += "    \n"
        code += "    return areas.get(label, (0, 0, screen_width, screen_height))\n"
        
        # Add alternative format using floor division
        code += "\n# Alternative format using floor division:\n"
        code += "def get_scan_area_floor(self, label):\n"
        code += "    screen_width, screen_height = pyautogui.size()\n"
        code += "    \n"
        code += "    areas = {\n"
        
        for i, (rect, name) in enumerate(zip(self.areas, self.area_names)):
            # Calculate ratios
            x_ratio = rect.x() / current_width
            y_ratio = rect.y() / current_height
            w_ratio = rect.width() / current_width
            h_ratio = rect.height() / current_height
            
            code += f"        \"{name}\": (floor(screen_width * {x_ratio:.4f}), "
            code += f"floor(screen_height * {y_ratio:.4f}), "
            code += f"floor(screen_width * {w_ratio:.4f}), "
            code += f"floor(screen_height * {h_ratio:.4f})),\n"
        
        code += "    }\n"
        code += "    \n"
        code += "    return areas.get(label, (0, 0, screen_width, screen_height))\n"
        
        return code
        
    def copy_code(self):
        """Copy the generated code to clipboard."""
        code = self.code_display.toPlainText()
        if code:
            clipboard = QApplication.clipboard()
            clipboard.setText(code)
            self.status_label.setText("Code copied to clipboard!")
            
            # Reset status after 2 seconds
            QTimer.singleShot(2000, lambda: self.status_label.setText("Ready to record areas"))
        
    def save_areas(self):
        """Save the current areas to a file."""
        if not hasattr(self, 'areas') or not self.areas:
            QMessageBox.warning(self, "No Areas", "No areas to save!")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Areas", "recorded_areas.json", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                areas_data = []
                for i, (rect, name) in enumerate(zip(self.areas, self.area_names)):
                    area_data = {
                        "name": name,
                        "x": rect.x(),
                        "y": rect.y(),
                        "width": rect.width(),
                        "height": rect.height(),
                        "screen_resolution": f"{self.current_resolution.width}x{self.current_resolution.height}",
                        "ratios": {
                            "x_ratio": rect.x() / self.current_resolution.width,
                            "y_ratio": rect.y() / self.current_resolution.height,
                            "w_ratio": rect.width() / self.current_resolution.width,
                            "h_ratio": rect.height() / self.current_resolution.height
                        }
                    }
                    areas_data.append(area_data)
                
                with open(filename, 'w') as f:
                    json.dump(areas_data, f, indent=2)
                
                self.status_label.setText(f"Areas saved to {filename}")
                QMessageBox.information(self, "Success", f"Areas saved to {filename}")
                
            except Exception as e:
                QMessageBox.showerror("Error", f"Failed to save areas: {e}")
                
    def load_areas(self):
        """Load areas from a file."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Load Areas", "", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    areas_data = json.load(f)
                
                # Convert back to QRect objects
                self.areas = []
                self.area_names = []
                
                for area_data in areas_data:
                    rect = QRect(
                        area_data['x'],
                        area_data['y'],
                        area_data['width'],
                        area_data['height']
                    )
                    self.areas.append(rect)
                    self.area_names.append(area_data['name'])
                
                self.update_displays()
                self.status_label.setText(f"Areas loaded from {filename}")
                
            except Exception as e:
                QMessageBox.showerror("Error", f"Failed to load areas: {e}")
                
    def clear_areas(self):
        """Clear all recorded areas."""
        if hasattr(self, 'areas'):
            self.areas.clear()
            self.area_names.clear()
            self.update_displays()
            self.status_label.setText("All areas cleared")
        
    def export_areas(self):
        """Export areas in multiple formats."""
        if not hasattr(self, 'areas') or not self.areas:
            QMessageBox.warning(self, "No Areas", "No areas to export!")
            return
            
        # Create export data
        export_data = {
            "metadata": {
                "source_resolution": f"{self.current_resolution.width}x{self.current_resolution.height}",
                "export_time": datetime.now().isoformat(),
                "total_areas": len(self.areas)
            },
            "resolutions": {}
        }
        
        # Generate for each target resolution
        for width, height in self.target_resolutions:
            resolution_key = f"{width}x{height}"
            export_data["resolutions"][resolution_key] = []
            
            for rect, name in zip(self.areas, self.area_names):
                # Calculate ratios
                x_ratio = rect.x() / self.current_resolution.width
                y_ratio = rect.y() / self.current_resolution.height
                w_ratio = rect.width() / self.current_resolution.width
                h_ratio = rect.height() / self.current_resolution.height
                
                # Calculate target coordinates
                target_x = int(x_ratio * width)
                target_y = int(y_ratio * height)
                target_w = int(w_ratio * width)
                target_h = int(h_ratio * height)
                
                area_info = {
                    "name": name,
                    "coordinates": (target_x, target_y, target_w, target_h),
                    "ratios": (x_ratio, y_ratio, w_ratio, h_ratio)
                }
                export_data["resolutions"][resolution_key].append(area_info)
        
        # Save export file
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Areas", "exported_areas.json", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(export_data, f, indent=2)
                
                self.status_label.setText(f"Areas exported to {filename}")
                QMessageBox.information(self, "Success", f"Areas exported to {filename}")
                
            except Exception as e:
                QMessageBox.showerror("Error", f"Failed to export areas: {e}")

def main():
    """Main function to run the area recorder."""
    print("Starting Screen Area Recorder...")
    print("This tool helps you record screen areas and generate code for different resolutions.")
    print("Features:")
    print("- Interactive overlay for drawing areas")
    print("- Multi-resolution coordinate conversion")
    print("- Code generation for your ScreenInteractor class")
    print("- Export functionality for different target resolutions")
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = AreaRecorder()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
