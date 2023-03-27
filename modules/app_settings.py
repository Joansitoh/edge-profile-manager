import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QPixmap


class UISettings:

    @staticmethod
    def round_image(image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        project_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(project_path, '../images/circle_mask.png')
        mask = QPixmap(img_path)

        mask = mask.scaled(pixmap.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap.setMask(mask.createMaskFromColor(Qt.transparent))

        return pixmap

    @staticmethod
    def elide(label, text):
        # Get width of text
        font = QFontMetrics(label.font())
        width = font.width(text)
        max = int(UISettings.PROFILE_WIDTH / 2) - 10

        if width > max:
            return font.elidedText(text, Qt.ElideRight, max)
        return text

    PROFILE_HEIGHT = 170
    PROFILE_WIDTH = 150

    UI_HEIGHT = 550
    UI_WIDTH = 950

    BUTTON_WIDTH = 40
    BUTTON_HEIGHT = 20

    PROFILE_FRAME_PREFIX = "profile_frame_"
    PROFILE_FRAME_SETTINGS_PREFIX = "profile_frame_settings_"

    PROFILE_HOLDER_STYLE = '''
        QFrame {
            border: 1px solid gray;
            border-radius: 7px;
        }
        
        QFrame:hover {
            border: 3px solid gray;
        }
        
        QLabel {
            font: 57 8pt "Inter Medium";
            border: 0px;
        }
        
        QLabel:hover {
            border: 0px;
        }
    '''

    PROFILE_STYLE = '''
        QFrame {
            border: 0px;
        }
        
        QFrame:hover {
            border: 0px;
        }
        
        QLineEdit {
            border: 0px;
            background-color: transparent;
        }
    '''

    PROFILE_TITLE_STYLE = '''
        QLabel, QLineEdit {
            color: #7d7d7d;
            font-size: 18px;
            border: 0px;
            border-radius: 0px;
            padding: 5px;
        }
    '''

    PROFILE_AVATAR_STYLE = '''
        border: 0px;
        padding: 5px;
        background-color: transparent;
    '''

    PROFILE_SETTINGS_BUTTON_STYLE = '''
        QPushButton {
            color: gray;
            padding: 5px;
            
            border-width: 0px;
            border-radius: 10px;
        }

        QPushButton:hover {
            background-color: #6b6b6b;
            border-width: 0px;
            border-radius: 10px;
        }
    '''

    @staticmethod
    def get_total_path(path):
        project_path = os.path.dirname(os.path.abspath(__file__))
        # remove 'modules' from path
        project_path = os.path.dirname(project_path)
        img_path = os.path.join(project_path, path)
        return img_path
