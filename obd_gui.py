import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer
from obd_simulator import OBD_Simulator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class OBDApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OBD-II Vehicle Diagnostics (Simulated)")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        self.layout = QVBoxLayout()

        # Labels to display data
        self.rpm_label = QLabel("RPM: Fetching...", self)
        self.speed_label = QLabel("Speed: Fetching...", self)
        self.temp_label = QLabel("Coolant Temp: Fetching...", self)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh Data", self)
        self.refresh_button.clicked.connect(self.update_data)

        # Matplotlib figure for live graph
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Add widgets to layout
        self.layout.addWidget(self.rpm_label)
        self.layout.addWidget(self.speed_label)
        self.layout.addWidget(self.temp_label)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        # Create an instance of the simulator
        self.simulator = OBD_Simulator()

        # Data storage for plotting
        self.time_data = []
        self.rpm_data = []
        self.speed_data = []
        self.counter = 0

        # Auto-refresh data every 3 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(3000)  # Update every 3 seconds

        # Set up live graph animation
        self.ani = animation.FuncAnimation(self.figure, self.update_graph, interval=3000)

    def update_data(self):
        """Fetch and update simulated data"""
        data = self.simulator.get_all_data()
        self.rpm_label.setText(f"RPM: {data['RPM']}")
        self.speed_label.setText(f"Speed: {data['Speed']} km/h")
        self.temp_label.setText(f"Coolant Temp: {data['Coolant Temp']} °C")

        # Save data for plotting
        self.time_data.append(self.counter)
        self.rpm_data.append(data['RPM'])
        self.speed_data.append(data['Speed'])
        self.counter += 1

        # Log data
        with open("obd_log.txt", "a") as log_file:
            log_file.write(f"{self.counter}, {data['RPM']}, {data['Speed']}, {data['Coolant Temp']}\n")

    def update_graph(self, frame):
        """Update the live graph"""
        self.ax.clear()
        self.ax.plot(self.time_data, self.rpm_data, label="RPM", color="r")
        self.ax.plot(self.time_data, self.speed_data, label="Speed (km/h)", color="b")
        self.ax.set_title("Live Vehicle Data")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OBDApp()
    window.show()
    sys.exit(app.exec_())
