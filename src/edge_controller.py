import os
import subprocess

from selenium import webdriver
from selenium.webdriver.edge.options import Options

def open_edge_profile(profile_name):
    # Ruta de acceso al ejecutable del navegador Microsoft Edge
    edge_exe = os.path.join(os.environ["ProgramFiles(x86)"], "Microsoft", "Edge", "Application", "msedge.exe")
    cmd_options = f'--profile-directory="{profile_name}"'

    # Comando completo para abrir el navegador con las opciones especificadas
    cmd = f'"{edge_exe}" {cmd_options}'

    # Ejecutar el comando como un proceso de Windows
    subprocess.Popen(cmd, shell=True)