import PySimpleGUI as sg

import webbrowser
from PIL import Image


def PopupImage(imageChoice):
    layout = [
        [sg.Image(data=imageChoice,key="-IMAGE-")],
    ]
    window = sg.Window("ExamMaker - Visualizador", layout,icon=r'input/LogoIcon.ico')
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()