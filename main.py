import sys
import random

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)
import pyqtgraph as pg


class BarnsleyFernApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barnsley Fern Visualizer")
        self.resize(1080, 700)

        self.points = []
        self.x = 0.0
        self.y = 0.0
        self.is_running = False

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

        parameters_group = QGroupBox("Parameters")
        parameters_layout = QVBoxLayout()
        parameters_group.setLayout(parameters_layout)

        self.points_per_frame_label = QLabel("Points per frame: 500")
        self.points_per_frame_slider = QSlider(Qt.Horizontal)
        self.points_per_frame_slider.setRange(10, 5000)
        self.points_per_frame_slider.setValue(500)
        self.points_per_frame_slider.valueChanged.connect(self.update_parameter_labels)

        parameters_layout.addWidget(self.points_per_frame_label)
        parameters_layout.addWidget(self.points_per_frame_slider)

        self.max_points_label = QLabel("Max points: 20000")
        self.max_points_slider = QSlider(Qt.Horizontal)
        self.max_points_slider.setRange(1000, 100000)
        self.max_points_slider.setSingleStep(1000)
        self.max_points_slider.setValue(20000)
        self.max_points_slider.valueChanged.connect(self.update_parameter_labels)

        parameters_layout.addWidget(self.max_points_label)
        parameters_layout.addWidget(self.max_points_slider)

        self.point_size_label = QLabel("Point size: 2")
        self.point_size_slider = QSlider(Qt.Horizontal)
        self.point_size_slider.setRange(1, 8)
        self.point_size_slider.setValue(2)
        self.point_size_slider.valueChanged.connect(self.update_point_size)

        parameters_layout.addWidget(self.point_size_label)
        parameters_layout.addWidget(self.point_size_slider)

        self.speed_label = QLabel("Timer interval: 30 ms")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(10, 200)
        self.speed_slider.setValue(30)
        self.speed_slider.valueChanged.connect(self.update_speed)

        parameters_layout.addWidget(self.speed_label)
        parameters_layout.addWidget(self.speed_slider)

        controls_layout.addWidget(parameters_group)

        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        controls_layout.addWidget(self.status_label)

        self.points_label = QLabel("Generated points: 0")
        self.points_label.setStyleSheet("font-size: 14px;")
        controls_layout.addWidget(self.points_label)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout, 1)

    def update_parameter_labels(self):
        self.points_per_frame_label.setText(
            f"Points per frame: {self.points_per_frame_slider.value()}"
        )
        self.max_points_label.setText(
            f"Max points: {self.max_points_slider.value()}"
        )

    def update_point_size(self):
        size = self.point_size_slider.value()
        self.point_size_label.setText(f"Point size: {size}")
        self.scatter.setSize(size)

    def update_speed(self):
        interval = self.speed_slider.value()
        self.speed_label.setText(f"Timer interval: {interval} ms")

        if self.is_running:
            self.timer.start(interval)

    def start_animation(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.setText("Status: Running")
            self.timer.start(self.speed_slider.value())

    def pause_animation(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            self.status_label.setText("Status: Paused")

    def reset_fern(self):
        self.is_running = False
        self.timer.stop()
        self.points = []
        self.x = 0.0
        self.y = 0.0
        self.scatter.setData([], [])
        self.points_label.setText("Generated points: 0")
        self.status_label.setText("Status: Ready")

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
        max_points = self.max_points_slider.value()
        points_per_frame = self.points_per_frame_slider.value()

        if len(self.points) >= max_points:
            self.is_running = False
            self.timer.stop()
            self.status_label.setText("Status: Finished")
            return

        new_points_count = min(points_per_frame, max_points - len(self.points))

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