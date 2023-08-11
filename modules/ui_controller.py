from main import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from . app_settings import UISettings
from . edge_controller import EdgeController
from . anim_controller import AnimationManager


class UIController(EdgeProfileManager):

    def create_holder(self, profile):
        # HOLDER FRAME
        ############################################
        holder_frame = QFrame(self)
        holder_layout = QGridLayout(holder_frame)
        holder_layout.setContentsMargins(0, 0, 0, 0)
        holder_layout.setSpacing(0)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        holder_frame.setSizePolicy(sizePolicy)
        holder_frame.setStyleSheet(UISettings.PROFILE_HOLDER_STYLE)
        holder_frame.setFixedSize(QSize(UISettings.PROFILE_WIDTH, UISettings.PROFILE_HEIGHT))

        # SETTINGS FRAME
        ############################################
        holder_layout.addWidget(UIController.create_profile(self, profile), 0, 0, 1, 1)

        return holder_frame

    def create_profile(self, profile):
        # MAIN FRAME
        ############################################
        profile_frame = QFrame(self)
        profile_frame.setStyleSheet(UISettings.PROFILE_STYLE)
        profile_frame.setObjectName(UISettings.PROFILE_FRAME_PREFIX + profile['folder'])

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        profile_frame.setSizePolicy(sizePolicy)

        # Open profile on click
        profile_frame.mousePressEvent = lambda event: EdgeController.open_edge_profile(profile['folder'], self.destroy)

        gridLayout = QGridLayout(profile_frame)

        # EDGE PROFILE NAME
        ##############################################################
        title = QLineEdit(profile_frame)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        title.setSizePolicy(sizePolicy)
        title.setAlignment(Qt.AlignCenter)

        # On click out of the title, save the new name and unfocus
        title_text = profile['name']
        new_text = title.text()

        #print("Title text: " + title_text)
        #print("New text: " + new_text)
        title.editingFinished.connect(lambda: EdgeController.set_edge_profile_name(profile['folder'], title.text()))

        # On click on any part of the window unfocus the title

        title.setStyleSheet(UISettings.PROFILE_TITLE_STYLE)

        title.setText(UISettings.elide(title, profile['name']))
        title.setToolTip(profile['name'])
        title.setMaximumWidth(UISettings.PROFILE_WIDTH)

        gridLayout.addWidget(title, 0, 0, 1, 1)

        # EDGE PROFILE AVATAR
        ############################################
        avatar = QLabel(profile_frame)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        avatar.setSizePolicy(sizePolicy)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(UISettings.PROFILE_AVATAR_STYLE)

        img_path = profile['avatar']
        #print("Path: " + str(img_path))
        if img_path == '':
            print("Empty path")
            project_path = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(project_path, '../images/avatar.png')
        else:
            print("Path: " + str(img_path))

        pixmap = UISettings.round_image(img_path)
        avatar.setPixmap(pixmap)

        gridLayout.addWidget(avatar, 1, 0, 1, 1)

        # SETTINGS BUTTON
        ##############################################

        # Add settings button on bottom right corner
        #UIController.add_settings_btn(self, profile_frame, lambda x: AnimationManager.toggle_profile(self, profile))
        return profile_frame

    def mousePressEvent(self, *args, **kwargs):
        super().mousePressEvent(*args, **kwargs)
        print("Mouse pressed")

    def create_settings_frame(self, profile):
        # SETTINGS FRAME
        ############################################

        settings_frame = QFrame(self)
        settings_frame.setObjectName(UISettings.PROFILE_FRAME_SETTINGS_PREFIX + profile['folder'])
        settings_frame.setStyleSheet(UISettings.PROFILE_STYLE)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        settings_frame.setSizePolicy(sizePolicy)
        settings_frame.setMaximumSize(QSize(UISettings.PROFILE_WIDTH, 0))
        settings_frame.setMinimumSize(QSize(UISettings.PROFILE_WIDTH, 0))

        gridLayout = QGridLayout(settings_frame)

        # PROFILE NAME
        ############################################

        name_input = QLineEdit(settings_frame)
        name_input.setText(profile['name'])
        name_input.setAlignment(Qt.AlignCenter)
        name_input.setStyleSheet(UISettings.PROFILE_TITLE_STYLE)

        gridLayout.addWidget(name_input, 0, 0, 1, 1)

        # PROFILE AVATAR
        ############################################

        avatar_input = QLabel(settings_frame)
        avatar_input.setAlignment(Qt.AlignCenter)
        avatar_input.setStyleSheet(UISettings.PROFILE_AVATAR_STYLE)

        img_path = profile['avatar']
        if img_path == '':
            project_path = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(project_path, '../images/avatar.png')

        pixmap = UISettings.round_image(img_path)
        avatar_input.setPixmap(pixmap)

        gridLayout.addWidget(avatar_input, 1, 0, 1, 1)

        # On click open file explorer
        avatar_input.mousePressEvent = lambda event: UIController.upload_avatar(self, avatar_input, name_input, profile)

        # SAVE BUTTON
        ############################################

        save_btn = QPushButton('Save', settings_frame)
        save_btn.clicked.connect(lambda: UIController.save_profile(self, name_input, avatar_input, profile))

        gridLayout.addWidget(save_btn, 2, 0, 1, 1)

        # Add settings button on bottom right corner
        UIController.add_settings_btn(self, settings_frame, lambda x: AnimationManager.toggle_profile(self, profile))
        return settings_frame

    def add_settings_btn(self, profile_frame, function):
        settings_btn = QPushButton('⚙', profile_frame)
        settings_btn.setStyleSheet(UISettings.PROFILE_SETTINGS_BUTTON_STYLE)
        settings_btn.setFixedSize(20, 20)
        settings_btn.move(UISettings.PROFILE_WIDTH - 26, 4)
        settings_btn.clicked.connect(function)

    def save_profile_settings(self, profile, name, avatar):
        # Save profile settings
        profile['name'] = name
        profile['avatar'] = avatar

        EdgeController.set_edge_profile_name(profile['folder'], name)

class ProfileDialog(QDialog):
    def __init__(self, profile, parent=None):
        super(ProfileDialog, self).__init__(parent)
        self.profile = profile

        self.setWindowTitle('Editar Perfil')
        self.setFixedSize(400, 300)

        # Widgets de la ventana de diálogo
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(128, 128)
        self.avatar_label.setPixmap(QPixmap('avatar.png'))
        self.avatar_label.mouseDoubleClickEvent = self.open_file_dialog
        self.name_label = QLabel('Nombre:')
        self.name_edit = QLineEdit()
        self.save_button = QPushButton('Guardar')

        # Diseño de la ventana de diálogo
        layout = QVBoxLayout()
        layout.addWidget(self.avatar_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.save_button, alignment=Qt.AlignRight)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Borde inferior en los títulos
        self.name_label.setStyleSheet('border-bottom: 1px solid gray;')

        # Conexión de señales y slots
        self.save_button.clicked.connect(self.save_profile)

        self.setLayout(layout)

    def open_file_dialog(self, event):
        filename, _ = QFileDialog.getOpenFileName(self, 'Seleccionar avatar', '', 'Archivos de imagen (*.png *.jpg *.jpeg)')
        if filename:
            self.avatar_label.setPixmap(QPixmap(filename))

    def save_profile(self):
        name = self.name_edit.text()
        avatar = self.avatar_label.pixmap().toImage()

        if name != '':
            EdgeController.set_edge_profile_name(self.profile['folder'], name)
            self.profile['name'] = name

        self.accept()
