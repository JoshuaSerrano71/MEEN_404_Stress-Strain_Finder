# main.py
import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFileDialog, QTextEdit, QHBoxLayout)
from PyQt5.QtGui import QIcon  # Import QIcon to set the application icon
'''
def run_analysis(self):
    if not self.experimental_data_path or not self.dimension_data_path:
        self.results_text.setText("Please upload both files first.")
        return

    try:
        # Get absolute path to stress-strain.py in the same directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "stress-strain.py")
        
        # Debug output
        print(f"Running: python {script_path} {self.experimental_data_path} {self.dimension_data_path}")
        
        # Run with explicit paths and capture all output
        result = subprocess.run(
            ["python", script_path, 
             self.experimental_data_path, 
             self.dimension_data_path],
            capture_output=True, 
            text=True,
            check=True
        )
        
        # Show both stdout and stderr
        output = f"SUCCESS:\n{result.stdout}"
        if result.stderr:
            output += f"\nERRORS:\n{result.stderr}"
        self.results_text.setText(output)
        
    except subprocess.CalledProcessError as e:
        self.results_text.setText(
            f"Analysis failed (code {e.returncode}):\n"
            f"STDOUT:\n{e.stdout}\n"
            f"STDERR:\n{e.stderr}"
        )
    except Exception as e:
        self.results_text.setText(f"Unexpected error: {str(e)}")
'''    
    
class StressStrainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle("Stress-Strain Calculator")
        self.setGeometry(100, 100, 600, 400)

        # Set the application icon
        icon_path = os.path.join(os.path.dirname(__file__), "app_icon.ico")  # Path to the icon file
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Icon file not found: {icon_path}")

        # Create a central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Add a label for instructions
        self.label = QLabel("Upload the experimental data and dimension data files:")
        layout.addWidget(self.label)

        # Add a button to load the experimental data file
        self.experimental_data_button = QPushButton("Load Experimental Data (CSV)")
        self.experimental_data_button.clicked.connect(self.load_experimental_data)
        layout.addWidget(self.experimental_data_button)

        # Add a button to load the dimension data file
        self.dimension_data_button = QPushButton("Load Dimension Data (CSV)")
        self.dimension_data_button.clicked.connect(self.load_dimension_data)
        layout.addWidget(self.dimension_data_button)

        # Add a text area to display results
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.results_text)

        # Add a button to run the analysis
        self.run_button = QPushButton("Run Analysis")
        self.run_button.clicked.connect(self.run_analysis)
        layout.addWidget(self.run_button)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

        # Initialize file paths
        self.experimental_data_path = None
        self.dimension_data_path = None

    def load_experimental_data(self):
        # Open a file dialog to select the experimental data CSV file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Experimental Data CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.experimental_data_path = file_path
            self.label.setText(f"Experimental Data File: {os.path.basename(file_path)}")

    def load_dimension_data(self):
        # Open a file dialog to select the dimension data CSV file
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Dimension Data CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.dimension_data_path = file_path
            self.label.setText(f"Dimension Data File: {os.path.basename(file_path)}")

    def run_analysis(self):
        # Check if both files have been selected
        if not self.experimental_data_path or not self.dimension_data_path:
            self.results_text.setText("Please upload both the experimental data and dimension data files.")
            return

        # Call the stress-strain.py script with the selected files
        try:
            result = subprocess.run(
                ["python", "stress-strain.py", self.experimental_data_path, self.dimension_data_path],
                capture_output=True, text=True, check=True
            )
            # Display the output in the text area
            self.results_text.setText(result.stdout)
        except subprocess.CalledProcessError as e:
            self.results_text.setText(f"Error: {e.stderr}")
        except FileNotFoundError:
            self.results_text.setText("Error: stress-strain.py not found.")

# Main function to run the application
def main():
    app = QApplication(sys.argv)

    # Set the application name and display name (for Windows taskbar icon)
    app.setApplicationName("StressStrainApp")
    app.setApplicationDisplayName("Stress-Strain Calculator")

    # Create and show the main window
    window = StressStrainApp()
    window.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()