import os
import json
import random
import sys

from PyQt5 import uic
from time import sleep

from PyQt5.QtWidgets import QLineEdit

from modules import *


class EdgeProfileManager(QMainWindow):

    def __init__(self, profiles):
        super().__init__()
        self.ui = uic.loadUi(UISettings.get_total_path("profiles.ui"), self)
        self.profiles = profiles

        UISettings.UI_HEIGHT = UISettings.UI_HEIGHT + ((UISettings.PROFILE_HEIGHT - 50) * (len(self.profiles) // 3))

        self.init_ui()

    def init_ui(self):
        # Set window icon
        # self.setWindowIcon(QIcon('icon.png'))

        # FRAME SETTINGS
        ############################################
        self.setMinimumSize(UISettings.UI_WIDTH, UISettings.UI_HEIGHT)
        # Set the background image scaled to fit the window

        # Set the background image scaled to fit the window
        pixmap = QPixmap(UISettings.get_total_path('images/background.png'))
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

        self.setWindowTitle('Edge Profile Manager')
        self.setWindowIcon(QIcon(UISettings.get_total_path('images/icon.png')))

        if EdgeController.get_canary():
            self.ui.canary_check.setChecked(True)

        self.ui.btn_guest.clicked.connect(lambda _: EdgeController.open_hidden_mode())
        self.ui.canary_check.stateChanged.connect(lambda _: EdgeController.set_canary())

        # PROFILES
        ############################################
        profiles_layout = self.ui.profiles_layout

        pixmap = QPixmap(UISettings.get_total_path('images/icon.png'))
        pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.banner_logo.setPixmap(pixmap)

        row = 0
        col = 0
        for profile in self.profiles:
            # Main profile frame
            profiles_layout.addWidget(UIController.create_holder(self, profile), row, col)

            col += 1
            if col >= 3:
                row += 1
                col = 0

        adder_json = {'name': 'Add', 'folder': "New", "avatar": UISettings.get_total_path('images/add.png')}
        holder_frame = UIController.create_holder(self, adder_json)
        holder_frame.setStyleSheet(UISettings.PROFILE_ADD_HOLDER_STYLE)
        holder_frame.setStyleSheet(holder_frame.styleSheet() + "border-style: dotted;")

        profiles_layout.addWidget(holder_frame, row, col)

        # Connect the function to the resize event of the window
        self.resizeEvent = self.onResize

        self.show()

    def on_guest_clicked(self):
        # Open in incognito mode
        EdgeController.open_hidden_mode()

    def mousePressEvent(self, event):
        focused_widget = self.focusWidget()
        if focused_widget:
            focused_widget.clearFocus()

            if isinstance(focused_widget, QLineEdit):
                profile_frame = focused_widget.parent()
                profile_name = profile_frame.objectName().replace(UISettings.PROFILE_FRAME_PREFIX, "")
                EdgeController.set_edge_profile_name(profile_name, focused_widget.text())
        super(EdgeProfileManager, self).mousePressEvent(event)

    def setBackgroundImage(self):
        # Set the background image scaled to fit the window
        pixmap = QPixmap(UISettings.get_total_path('images/background.png'))
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

    def onResize(self, event):
        # Call the setBackgroundImage function every time the window is resized
        self.setBackgroundImage()
        QMainWindow.resizeEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    edge_profiles = EdgeController.get_edge_profiles()
    window = EdgeProfileManager(edge_profiles)
    window.show()
    sys.exit(app.exec_())
