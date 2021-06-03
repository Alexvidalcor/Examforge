import PySimpleGUIWeb as sg

from PIL import Image

def PopupImage(imageChoice):
    layout = [
        [sg.Image(data=imageChoice,key="-IMAGE-")],
        [sg.Button("Salir")]
    ]
    window = sg.Window("ExamMaker - Visualizador", layout)
    while True:
        event, values = window.read()
        if event == "Salir" or event == sg.WIN_CLOSED:
            break
    window.close()
