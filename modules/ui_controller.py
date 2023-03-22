from main import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from . app_settings import UISettings
from . edge_controller import EdgeController


class UIController(EdgeProfileManager):

    def create_profile(self, profile):
        # MAIN FRAME
        ############################################
        profile_frame = QFrame(self)
        profile_id = random.randint(0, 1000000)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(profile_frame.sizePolicy().hasHeightForWidth())

        profile_frame.setSizePolicy(sizePolicy)
        profile_frame.setMaximumSize(QSize(UISettings.PROFILE_WIDTH, UISettings.PROFILE_HEIGHT))
        profile_frame.setMinimumSize(QSize(UISettings.PROFILE_WIDTH, UISettings.PROFILE_HEIGHT))

        # Open profile on click
        profile_frame.mousePressEvent = lambda event: EdgeController.open_edge_profile(profile['folder'], self.destroy)
        gridLayout = QGridLayout(profile_frame)

        # EDGE PROFILE NAME
        ##############################################################
        title = QLabel(profile_frame)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(title.sizePolicy().hasHeightForWidth())

        title.setSizePolicy(sizePolicy)
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet(UISettings.PROFILE_TITLE_STYLE)

        title.setText(profile['name'])
        title.setToolTip(profile['name'])
        title.setMaximumWidth(UISettings.PROFILE_WIDTH)

        UIController.elide(self, title, profile['name'])
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
        avatar.setStyleSheet(UISettings.PROFILE_AVATAR_STYLE)

        img_path = profile['avatar']
        if img_path == '':
            project_path = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(project_path, '../images/avatar.png')

        pixmap = UIController.round_image(self, img_path)
        avatar.setPixmap(pixmap)

        gridLayout.addWidget(avatar, 1, 0, 1, 1)

        # SETTINGS BUTTON
        ##############################################

        # Add settings button on bottom right corner
        settings_btn = QPushButton('⚙', profile_frame)
        settings_btn.clicked.connect(lambda x: UIController.open_edge_profile_settings(self, profile))
        settings_btn.resize(20, 20)
        settings_btn.move(UISettings.PROFILE_WIDTH - 24, UISettings.PROFILE_HEIGHT - 24)
        settings_btn.setStyleSheet(UISettings.PROFILE_SETTINGS_BUTTON_STYLE)

        return profile_frame

    def open_edge_profile_settings(self, profile):
        dialog = ProfileDialog(profile, self)
        dialog.exec_()

    def save_profile_settings(self, profile, name, avatar):
        # Save profile settings
        profile['name'] = name
        profile['avatar'] = avatar

        EdgeController.set_edge_profile_name(profile['folder'], name)

    def elide(self, label, text):
        metrix = QFontMetrics(label.font())
        width = label.width()
        label.setText(metrix.elidedText(text, Qt.ElideRight, width - 15))

    def round_image(self, image_path):
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(75, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        mask_path = 'images/circle_mask.png'
        mask = QPixmap(mask_path)

        mask = mask.scaled(pixmap.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        pixmap.setMask(mask.createMaskFromColor(Qt.transparent))

        return pixmap


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
