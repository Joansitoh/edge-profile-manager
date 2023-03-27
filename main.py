import os
import json
import random
import sys

from PyQt5 import uic
from time import sleep

from modules import *
from widgets import *


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

        # PROFILES
        ############################################
        profile_frame = self.ui.profiles_frame
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

        adder_json = {'name': 'Create new profile', 'folder': "New", "avatar": UISettings.get_total_path('images/add.png')}
        profiles_layout.addWidget(UIController.create_holder(self, adder_json), row, col)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    edge_profiles = EdgeController.get_edge_profiles()
    window = EdgeProfileManager(edge_profiles)
    window.show()
    sys.exit(app.exec_())
