import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets

#### this gives the media player of the app


# Custom Video Widget for Fullscreen Handling

class CustomVideoWidget(QtMultimediaWidgets.QVideoWidget):
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Escape and self.isFullScreen():
            self.setFullScreen(False)
        else:
            super().keyPressEvent(event)



# Video Player Module 

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

        groupBox = QtWidgets.QGroupBox("Video")  # ✅ This is your title
        groupLayout = QtWidgets.QVBoxLayout()
        groupLayout.addWidget(self.videoWidget)
        groupBox.setLayout(groupLayout)

        layout_vid.addWidget(groupBox)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        # Create audio output and set it on the player
##        self.audio_output = QtMultimedia.QAudioOutput()
##        self.mediaPlayer.setAudioOutput(self.audio_output)
##        self.audio_output.setVolume(1.0)  # Max is 1.0

        # Video control buttons
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)  # Align to left
        
        play_button = self.but_style()
##        self.play_button = QtWidgets.QPushButton()
        play_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay))
        play_button.setToolTip("Play")
        play_button.setFixedSize(50, 32)
        play_button.clicked.connect(self.play_video)
        control_layout.addWidget(play_button)

        pause_button = self.but_style()
        pause_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPause))
        pause_button.setToolTip("Pause")        
        pause_button.setFixedSize(50, 32)
        pause_button.clicked.connect(self.pause_video)
        control_layout.addWidget(pause_button)
        
        stop_button = self.but_style()
        stop_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaStop))
        stop_button.setToolTip("Stop")                
        stop_button.setFixedSize(50, 32)        
        stop_button.clicked.connect(self.stop_video)
        control_layout.addWidget(stop_button)
        
        ful_screen = self.but_style()
        ful_screen.setIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_TitleBarMaxButton))
        ful_screen.setToolTip("Fullscreen")
        ful_screen.setFixedSize(50, 32)
        ful_screen.clicked.connect(self.toggle_fullscreen)
        control_layout.addWidget(ful_screen)

## volum slider
        self.volumeSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.volumeSlider.setStyleSheet("""
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
##        self.volumeSlider.sliderMoved.connect(self.set_vol)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)  # Default volume
        self.volumeSlider.setFixedWidth(200)


        control_layout.addStretch()

        self.vol_label = QtWidgets.QLabel("Volume")
        control_layout.addWidget(self.vol_label)

        control_layout.addWidget(self.volumeSlider)

        self.volumeSlider.valueChanged.connect(self.set_vol)
##        self.volumeSlider.valueChanged.connect(self.setVolume)
        self.set_vol(50)        

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
        layout_vid.addLayout(control_layout)

        main_layout.addLayout(control_layout)
        main_layout.addLayout(layout_vid)

        # Connect media player signals
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        
    def but_style(self):
        self.button = QtWidgets.QPushButton()

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
            QtCore.QTimer.singleShot(100, self.showExitHint)  # 👈 Delay ensures it's drawn
            


    def showExitHint(self):
        self.hintLabel = QtWidgets.QLabel("Press Esc to exit full screen", self)
        self.hintLabel.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: white;
            font-size: 19px;
            padding: 6px 12px;
            border-radius: 5px;
        """)
        self.hintLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hintLabel.adjustSize()

        # Center on screen, a bit down from top
        screen_geometry = QtGui.QGuiApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.hintLabel.width()) // 2
        y = 40
        self.hintLabel.move(x, y)

        self.hintLabel.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.ToolTip  # Keeps it floating but non-intrusive
        )
        self.hintLabel.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hintLabel.setAttribute(QtCore.Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.hintLabel.show()
        self.hintLabel.raise_()

        # Auto-hide after 3 seconds
        QtCore.QTimer.singleShot(5000, self.hintLabel.close)




    def set_vol(self, value):
        self.audio_output = QtMultimedia.QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(value)  # Max is 1.0


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

