from main import *
from . app_settings import UISettings


class EdgeController:

    @staticmethod
    def open_edge_profile(profile_name, open_func=None):
        # Ruta de acceso al ejecutable del navegador Microsoft Edge
        edge_exe = os.path.join(os.environ["ProgramFiles(x86)"], "Microsoft", "Edge", "Application", "msedge.exe")
        cmd_options = f'--profile-directory="{profile_name}"'

        # Comando completo para abrir el navegador con las opciones especificadas
        cmd = f'"{edge_exe}" {cmd_options}'

        # Ejecutar el comando como un proceso de Windows
        subprocess.Popen(cmd, shell=True)

        sleep(0.1)
        if open_func is not None:
            open_func()

    @staticmethod
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

    @staticmethod
    def set_edge_profile_name(profile_name, new_name):
        # Accedemos a la ruta de acceso de los perfiles de Microsoft Edge y dentro del apartado del profile
        # modificamos el campo "name" por el nuevo nombre
        local_app_data = os.environ['LOCALAPPDATA']
        edge_base_path = os.path.join(local_app_data, r'Microsoft\Edge\User Data')
        profile_list_path = os.path.join(edge_base_path, 'Local State')

        with open(profile_list_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data['profile']['info_cache'][profile_name]['name'] = new_name

        with open(profile_list_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def set_edge_profile_avatar(profile_name, avatar_path):
        # Accedemos a la ruta de acceso de los perfiles de Microsoft Edge y dentro del apartado del profile
        # modificamos el campo "name" por el nuevo nombre
        local_app_data = os.environ['LOCALAPPDATA']
        edge_base_path = os.path.join(local_app_data, r'Microsoft\Edge\User Data')
        profile_list_path = os.path.join(edge_base_path, 'Local State')

        with open(profile_list_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data['profile']['info_cache'][profile_name]['avatar'] = avatar_path

        with open(profile_list_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)


