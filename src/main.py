import os
import json
import random
from time import sleep

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from edge_controller import open_edge_profile

class EdgeProfileManager(QWidget):

    def __init__(self, profiles):
        super().__init__()
        self.profiles = profiles
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        # Set window icon
        #self.setWindowIcon(QIcon('icon.png'))

        # FRAME SETTINGS
        ############################################
        # Set window size
        self.resize(700, 350)

        # Set window title
        self.setWindowTitle('Microsoft Edge Profile Manager')

        # No rounded corners
        self.setWindowFlags(Qt.FramelessWindowHint)

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

        buttons_size = QSize(40, 20)
        
        close_btn = QPushButton('✕', self)
        close_btn.clicked.connect(self.close)
        close_btn.resize(buttons_size)
        close_btn.move(self.width() - buttons_size.width(), 0)
        close_btn.setStyleSheet(style)

        min_btn = QPushButton('─', self)
        min_btn.clicked.connect(self.showMinimized)
        min_btn.resize(buttons_size)
        min_btn.move(self.width() - buttons_size.width() * 2, 0)
        min_btn.setStyleSheet(style)

        # PROFILES
        ############################################

        row = 0
        col = 0
        for profile in self.profiles:
            # Main profile frame
            layout.addWidget(self.create_profile(profile), row, col)

            col += 1
            if col >= 3:
                row += 1
                col = 0

        self.setLayout(layout)
        self.setWindowTitle('Microsoft Edge Profile Manager')


    def create_profile(self, profile):

        # MAIN FRAME
        ############################################
        profile_frame = QFrame(self)
        profile_id = random.randint(0, 1000000)
        profile_frame.setObjectName(f'profile_{profile_id}')

        profile_frame.setStyleSheet('''
            QFrame#profile_''' + str(profile_id) + ''' {
                border: 1px solid #C3C3C3;
                border-radius: 5px;
            }
            
            QFrame#profile_''' + str(profile_id) + ''':hover {
                border: 2px solid #C3C3C3;
            }
        ''')

        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(profile_frame.sizePolicy().hasHeightForWidth())

        profile_frame.setSizePolicy(sizePolicy)
        profile_frame.setMaximumSize(QSize(165, 180))

        # Open profile on click
        profile_frame.mousePressEvent = lambda event: self.open_edge_profile(profile['folder'])

        gridLayout = QGridLayout(profile_frame)

        # EDGE PROFILE NAME
        ############################################
        title = QLabel(profile_frame)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(title.sizePolicy().hasHeightForWidth())

        title.setSizePolicy(sizePolicy)
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet('''
            border-bottom: 1px solid #C3C3C3;
            border-radius: 0px;
            padding: 5px;
        ''')

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(13)

        title.setFont(font)
        title.setText(profile['name'])
        title.setMaximumWidth(165)  # Limita el ancho máximo de la etiqueta del título

        gridLayout.addWidget(title, 0, 0, 1, 1)

        # EDGE PROFILE AVATAR
        ############################################
        avatar = QLabel(profile_frame)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(avatar.sizePolicy().hasHeightForWidth())

        avatar.setSizePolicy(sizePolicy)
        avatar.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap()
        if profile['avatar'] == '':
            # Get project path
            project_path = os.path.dirname(os.path.abspath(__file__))
            # Load default avatar
            default_avatar_path = os.path.join(project_path, 'images/avatar.png')
            pixmap.load(default_avatar_path)
        else:
            pixmap = QPixmap(profile['avatar'])

        pixmap = pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Cargar la imagen PNG del círculo
        mask_path = 'images/circle_mask.png'
        mask = QPixmap(mask_path)

        # Ajustar la resolución de la imagen del círculo a la del QPixmap original
        mask = mask.scaled(pixmap.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Combinar la imagen del círculo con el QPixmap original
        pixmap.setMask(mask.createMaskFromColor(Qt.transparent))

        avatar.setPixmap(pixmap)

        gridLayout.addWidget(avatar, 1, 0, 1, 1)

        return profile_frame

    def open_edge_profile(self, profile_folder):
        open_edge_profile(profile_folder)
        sleep(0.1)
        self.close()


def get_edge_profiles():
    local_app_data = os.environ['LOCALAPPDATA']
    edge_base_path = os.path.join(local_app_data, r'Microsoft\Edge\User Data')
    profile_list_path = os.path.join(edge_base_path, 'Local State')

    profiles = []

    with open(profile_list_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key, value in data['profile']['info_cache'].items():
            profile_folder = os.path.join(edge_base_path, key)
            avatar_path = os.path.join(profile_folder, 'Google Profile Picture.png')
            profiles.append({
                'name': value['name'],
                'folder': key,
                'avatar': avatar_path if os.path.exists(avatar_path) else ''
            })

    return profiles

if __name__ == '__main__':
    app = QApplication([])
    edge_profiles = get_edge_profiles()
    profile_manager = EdgeProfileManager(edge_profiles)
    profile_manager.show()
    app.exec_()
