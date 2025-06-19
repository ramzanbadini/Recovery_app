from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
import sys

# ==== ChatBot Window with Sidebar ====
class ChatBotWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 ChatBot Assistant")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QListWidget {
                background-color: #2c3e50;
                color: white;
                border: none;
            }
            QTextEdit {
                background-color: #fdfdfd;
                border: 1px solid #ccc;
                padding: 10px;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #bbb;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        # === Main horizontal layout ===
        main_layout = QtWidgets.QHBoxLayout(self)

        # === Sidebar (History) ===
        self.history_list = QtWidgets.QListWidget()
        self.history_list.setFixedWidth(200)
        self.history_list.addItem("New Chat")
        main_layout.addWidget(self.history_list)

        # === Right side (Chat area) ===
        right_layout = QtWidgets.QVBoxLayout()

        # Chat history area
        self.chat_area = QtWidgets.QTextEdit()
        self.chat_area.setReadOnly(True)
        right_layout.addWidget(self.chat_area)

        # Input + send button layout
        input_layout = QtWidgets.QHBoxLayout()
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("Ask about Radar & Comm systems...")
        self.input_field.returnPressed.connect(self.handle_send)
        input_layout.addWidget(self.input_field)

        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self.handle_send)
        input_layout.addWidget(self.send_button)

        right_layout.addLayout(input_layout)

        # Add right side layout to main layout
        main_layout.addLayout(right_layout)

    def handle_send(self):
        user_msg = self.input_field.text().strip()
        if not user_msg:
            return

        self.append_message("You", user_msg)
        self.input_field.clear()

        # Simulated bot response
        QtCore.QTimer.singleShot(400, lambda: self.append_message("Bot", f"Echo: {user_msg}"))

    def append_message(self, sender, message):
        color = "#2e86de" if sender == "You" else "#27ae60"
        self.chat_area.append(f'<b style="color:{color};">{sender}:</b> {message}')
