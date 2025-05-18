import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets

# ---------------------------
# Custom Video Widget for Fullscreen Handling
# ---------------------------
class CustomVideoWidget(QtMultimediaWidgets.QVideoWidget):
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
        else:
            super().keyPressEvent(event)



# ---------------------------
# Video Player Module
# ---------------------------
class VideoPlayerWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mediaPlayer = QtMultimedia.QMediaPlayer(self)
        # Use our custom video widget for better fullscreen handling.
        self.videoWidget = CustomVideoWidget(self)
        self.init_ui()

    def init_ui(self):

        main_layout = QtWidgets.QHBoxLayout(self)
        
        
        layout_vid = QtWidgets.QVBoxLayout()
        layout_vid.addWidget(self.videoWidget)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        

        # Video control buttons
        control_layout = QtWidgets.QVBoxLayout()
        play_button = self.but_style("Play")
        play_button.clicked.connect(self.play_video)
        control_layout.addWidget(play_button)

        pause_button = self.but_style("Pause")
        pause_button.clicked.connect(self.pause_video)
        control_layout.addWidget(pause_button)
        
        stop_button = self.but_style("Stop")
        stop_button.clicked.connect(self.stop_video)
        control_layout.addWidget(stop_button)
        
        ful_screen = self.but_style("Fullscreen")
        ful_screen.clicked.connect(self.toggle_fullscreen)
        control_layout.addWidget(ful_screen)


        # Video seeking slider
        self.position_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.position_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #bbb;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background: #3498db;
                border: 1px solid #2980b9;
                width: 16px;
                height: 16px;
                margin: -6px 0; /* to center the round handle vertically */
                border-radius: 8px; /* makes it round */
            }
        """)

        
        self.position_slider.sliderMoved.connect(self.set_position)
        layout_vid.addWidget(self.position_slider)

        main_layout.addLayout(control_layout)
        main_layout.addLayout(layout_vid)

        # Connect media player signals
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
    def but_style(self, text):
        self.button = QtWidgets.QPushButton(text)

        self.button.setStyleSheet("""
            QPushButton {
                background-color: #6b9bbb;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 6px 16px;
                border-radius: 6px;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        """)
        return self.button

    def play_video(self):
        self.mediaPlayer.play()

    def pause_video(self):
        self.mediaPlayer.pause()

    def stop_video(self):
        self.mediaPlayer.stop()
        
    def toggle_fullscreen(self):
        if self.videoWidget.isFullScreen():
            self.videoWidget.setFullScreen(False)
        else:
            self.videoWidget.setFullScreen(True)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def load_video(self, video_path):
        if os.path.exists(video_path):
            url = QtCore.QUrl.fromLocalFile(video_path)
            self.mediaPlayer.setSource(url)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Video file not found.")

