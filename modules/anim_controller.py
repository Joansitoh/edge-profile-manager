from .ui_controller import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from . app_settings import UISettings
from . edge_controller import EdgeController


class AnimationManager(EdgeProfileManager):

    def hide_profile_frame(self, settings_frame, end_callback):
        self.animation = QPropertyAnimation(settings_frame, b"maximumHeight")
        self.animation.setDuration(150)
        self.animation.setStartValue(settings_frame.height())
        self.animation.setEndValue(0)
        if end_callback is not None:
            self.animation.finished.connect(end_callback)
        self.animation.start()

    def show_profile_frame(self, settings_frame, end_callback):
        self.animation = QPropertyAnimation(settings_frame, b"maximumHeight")
        self.animation.setDuration(150)
        self.animation.setStartValue(0)
        self.animation.setEndValue(UISettings.PROFILE_HEIGHT)
        if end_callback is not None:
            self.animation.finished.connect(end_callback)
        self.animation.start()

    def toggle_profile(self, profile):
        # Get profile frame
        profile_frame = self.ui.findChild(QFrame, "profile_frame_" + profile['folder'])
        settings_frame = self.ui.findChild(QFrame, "profile_frame_settings_" + profile['folder'])

        # If profile is not opened
        if profile_frame.height() == 0:
            # Hide settings and show profile
            AnimationManager.hide_profile_frame(self, settings_frame, lambda: AnimationManager.show_profile_frame(self, profile_frame, None))
        else:
            # Hide profile and show settings
            AnimationManager.hide_profile_frame(self, profile_frame, lambda: AnimationManager.show_profile_frame(self, settings_frame, None))


