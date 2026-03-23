import sys
import random

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
import pyqtgraph as pg


class BarnsleyFernApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barnsley Fern Visualizer")
        self.resize(1000, 650)

        self.points = []
        self.x = 0.0
        self.y = 0.0
        self.is_running = False

        self.points_per_frame = 500
        self.max_points = 20000

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_fern)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground("w")
        self.plot_widget.hideAxis("left")
        self.plot_widget.hideAxis("bottom")
        self.plot_widget.setAspectLocked(True)
        self.plot_widget.setXRange(-3, 3, padding=0)
        self.plot_widget.setYRange(0, 10, padding=0)

        self.scatter = pg.ScatterPlotItem(
            size=2,
            pen=None,
            brush=pg.mkBrush(0, 180, 0),
        )
        self.plot_widget.addItem(self.scatter)

        main_layout.addWidget(self.plot_widget, 4)

        controls_layout = QVBoxLayout()

        title_label = QLabel("Barnsley Fern")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        controls_layout.addWidget(title_label)

        self.start_button = QPushButton("Start")
        self.pause_button = QPushButton("Pause")
        self.reset_button = QPushButton("Reset")

        self.start_button.clicked.connect(self.start_animation)
        self.pause_button.clicked.connect(self.pause_animation)
        self.reset_button.clicked.connect(self.reset_fern)

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.reset_button)

        self.points_label = QLabel("Generated points: 0")
        self.points_label.setStyleSheet("font-size: 14px;")
        controls_layout.addWidget(self.points_label)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout, 1)

    def start_animation(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(30)

    def pause_animation(self):
        self.is_running = False
        self.timer.stop()

    def reset_fern(self):
        self.pause_animation()
        self.points = []
        self.x = 0.0
        self.y = 0.0
        self.scatter.setData([], [])
        self.points_label.setText("Generated points: 0")

    def next_point(self, x, y):
        r = random.random()

        if r < 0.01:
            x_new = 0.0
            y_new = 0.16 * y
        elif r < 0.86:
            x_new = 0.85 * x + 0.04 * y
            y_new = -0.04 * x + 0.85 * y + 1.6
        elif r < 0.93:
            x_new = 0.20 * x - 0.26 * y
            y_new = 0.23 * x + 0.22 * y + 1.6
        else:
            x_new = -0.15 * x + 0.28 * y
            y_new = 0.26 * x + 0.24 * y + 0.44

        return x_new, y_new

    def update_fern(self):
        if len(self.points) >= self.max_points:
            self.pause_animation()
            return

        new_points_count = min(self.points_per_frame, self.max_points - len(self.points))

        for _ in range(new_points_count):
            self.x, self.y = self.next_point(self.x, self.y)
            self.points.append((self.x, self.y))

        xs = [point[0] for point in self.points]
        ys = [point[1] for point in self.points]

        self.scatter.setData(xs, ys)
        self.points_label.setText(f"Generated points: {len(self.points)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarnsleyFernApp()
    window.show()
    sys.exit(app.exec())