import os
import json
import random
import sys

from time import sleep
from modules import *


class EdgeProfileManager(QMainWindow):

    def __init__(self, profiles):
        super().__init__()
        self.profiles = profiles
        self.init_ui()

    def init_ui(self):
        # Set window icon
        # self.setWindowIcon(QIcon('icon.png'))

        # FRAME SETTINGS
        ############################################
        # Set window size
        self.resize(UISettings.UI_WIDTH, UISettings.UI_HEIGHT)

        # Set window title
        self.setWindowTitle('Microsoft Edge Profile Manager')

        self.setStyleSheet('''
            QMainWindow {
                background-image: url("images/background.png");
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
        ''')

        self.setMinimumSize(UISettings.UI_WIDTH, UISettings.UI_HEIGHT)

        # No rounded corners
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create central widget and layout
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.setRowStretch(0, 1)
        layout.setContentsMargins(0, 0, 0, 0)

        central_widget.setLayout(layout)
        central_widget.setStyleSheet(UISettings.PROFILE_FRAME_STYLE)

        self.create_buttons()

        # PROFILES
        ############################################

        # Profiles layout cannot be separated, it need to be centralized
        # in the main layout
        profiles_temp_frame = QWidget()
        layout.addWidget(profiles_temp_frame, 0, 0, Qt.AlignCenter)

        # Add grid layout to the frame
        profiles_layout = QGridLayout()
        profiles_temp_frame.setLayout(profiles_layout)
        profiles_layout.setSpacing(20)

        row = 0
        col = 0
        for profile in self.profiles:
            # Main profile frame
            profiles_layout.addWidget(UIController.create_profile(self, profile), row, col)

            col += 1
            if col >= 3:
                row += 1
                col = 0

        adder_json = {'name': 'Create new profile', 'folder': "New", "avatar": "images/add.png"}
        profiles_layout.addWidget(UIController.create_profile(self, adder_json), row, col)

        # Footer
        ############################################
        footer = QFrame()
        footer.setFixedHeight(100)
        footer.setStyleSheet('''
            QFrame {
                border-top: 3px solid #C3C3C3;
                border-left: 0px;
                border-right: 0px;
                border-bottom: 0px;
                border-radius: 0px;
            }
            
            QFrame:hover {
                border-left: 0px;
                border-right: 0px;
                border-bottom: 0px;
                border-top: 3px solid #C3C3C3;
            }
        ''')
        layout.addWidget(footer, 1, 0, Qt.AlignBottom)

        # Create mouse move event
        ############################################
        self.mouse_pos = None
        self.mouse_moving = False

        self.mouseMoveEvent = self.move_window
        self.mousePressEvent = self.mouse_press
        self.mouseReleaseEvent = self.mouse_release

        # Create grip handle
        ############################################
        self.grip = QFrame(self)
        self.grip.resize(10, 10)
        self.grip.move(self.width() - 10, self.height() - 10)
        self.grip.setStyleSheet('''
            QFrame {
                background-color: #C3C3C3;
                border-radius: 5px;
            }
        ''')

        # Resize grip handle
        self.grip.mouseMoveEvent = self.resize_window
        self.grip.mousePressEvent = self.mouse_press
        self.grip.mouseReleaseEvent = self.mouse_release

        self.show()

    def mouse_press(self, event):
        self.mouse_pos = event.globalPos()
        self.mouse_moving = True

    def mouse_release(self, event):
        self.mouse_moving = False

    def move_window(self, event):
        if self.mouse_moving:
            delta = QPoint(event.globalPos() - self.mouse_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.mouse_pos = event.globalPos()

    def resize_window(self, event):
        if self.mouse_moving:
            delta = QPoint(event.globalPos() - self.mouse_pos)
            self.resize(self.width() + delta.x(), self.height() + delta.y())
            self.mouse_pos = event.globalPos()

            # Resize grip handle
            self.grip.move(self.width() - 10, self.height() - 10)
            self.buttons_frame.move(self.width() - self.buttons_frame.width(), 0)

    def create_buttons(self):
        # Create close and minimize buttons
        style = '''
                    QPushButton {
                        color: gray;
                        border: 0px;
                        border-radius: 0px;
                    }
                    QPushButton:hover {
                        background-color: #C3C3C3;
                    }
                '''

        buttons_size = QSize(UISettings.BUTTON_WIDTH, UISettings.BUTTON_HEIGHT)

        self.buttons_frame = QFrame(self)
        self.buttons_frame.resize(buttons_size.width() * 2, buttons_size.height())
        self.buttons_frame.move(self.width() - buttons_size.width() * 2, 0)

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_frame.setLayout(buttons_layout)

        # Add close and minimize buttons
        close_btn = QPushButton('✕', self)
        close_btn.clicked.connect(lambda x: self.shutdown())
        close_btn.resize(buttons_size)
        close_btn.move(self.width() - buttons_size.width(), 0)
        close_btn.setStyleSheet(style)

        min_btn = QPushButton('─', self)
        min_btn.clicked.connect(self.showMinimized)
        min_btn.resize(buttons_size)
        min_btn.move(self.width() - buttons_size.width() * 2, 0)
        min_btn.setStyleSheet(style)

        buttons_layout.addWidget(min_btn)
        buttons_layout.addWidget(close_btn)

    def shutdown(self):
        self.destroy()
        self.close()
        os._exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    edge_profiles = EdgeController.get_edge_profiles()
    window = EdgeProfileManager(edge_profiles)
    window.show()
    sys.exit(app.exec_())
