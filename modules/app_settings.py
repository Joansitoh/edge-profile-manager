class UISettings:

    PROFILE_HEIGHT = 180
    PROFILE_WIDTH = 165

    UI_HEIGHT = 550
    UI_WIDTH = 900

    BUTTON_WIDTH = 40
    BUTTON_HEIGHT = 20

    PROFILE_FRAME_STYLE = '''
        QFrame {
            border: 1px solid #C3C3C3;
            border-radius: 5px;
            background-color: white;
        }

        QFrame:hover {
            border: 2px solid #C3C3C3;
            box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.75);
        }
        
        QFrame QLabel:hover {
            border: 0px;
        }
    '''

    PROFILE_TITLE_STYLE = '''
        QLabel {
            color: #7d7d7d;
            font-size: 18px;
            font-family: "Google Sans",Roboto,Arial,sans-serif;
            
            border: 0px;
            border-bottom: 1px solid #C3C3C3;
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
           border: 0px;
           border-radius: 0px;
       }
       QPushButton:hover {
           background-color: #C3C3C3;
           border-radius: 50%;
       }
    '''