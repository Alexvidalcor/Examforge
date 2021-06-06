import PySimpleGUI as sg

import webbrowser
from PIL import Image


def PopupImage(imageChoice):
    layout = [
        [sg.Image(data=imageChoice,key="-IMAGE-")],
        [sg.Column([[sg.Button("Pulsa aquí para salir del visualizador y desbloquear la ventana de respuestas",key="-Exit-")]], vertical_alignment='center', justification='center')]
    ]

    window = sg.Window("ExamMaker - Visualizador", layout,icon=r'input/LogoIcon.ico', resizable=True)
    while True:
        event, values = window.read()
        if event == "-Exit-" or event == sg.WIN_CLOSED:
            break
    window.close()




def PopupHelp():
    commonParams = ["#ffff80", ("Helvetica", 15)]
    easterEgg=0
    
    layoutPrep = [
                [sg.Text('Versión de ExamMaker:', text_color=commonParams[0], font=commonParams[1]),
                 sg.Text('0.3.1', enable_events=True,key = "-VERSION-", tooltip="Click para ver novedades", text_color="#ffafad",font=commonParams[1])],
                
                [sg.Text('Autor:', text_color=commonParams[0], font=commonParams[1]),
                 sg.Text('Alexvidalcor', enable_events=True,key = "-AUTHOR-", text_color="#ffafad",font=commonParams[1])],
                
                [sg.Text("", size=(1,1))],
                
                [sg.Button('Código fuente', key="-URL-"),
                 sg.Button('Actualizaciones',key = "-CHECK-", disabled=True, tooltip="Función no implementada")],
            ]


    layoutMain = [[sg.Column(layoutPrep, element_justification='center')]]
    
    window = sg.Window('Detalles', layoutMain,icon=r'input/LogoIcon.ico')

    while True:           
        event, values = window.read()
        if event == "-URL-":
            webbrowser.open_new("https://github.com/Alexvidalcor/ExamMaker")
        elif event == "-VERSION-":
            webbrowser.open_new("https://github.com/Alexvidalcor/ExamMaker/releases/tag/v0.3")
        elif event == "-AUTHOR-":
            if easterEgg==0:
                window.Element("-AUTHOR-").update(text_color="#ffff80")
                easterEgg=1
            elif easterEgg==1:
                window.Element("-AUTHOR-").update(text_color="#ffafad")
                easterEgg=0
            
            
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
    window.close()
    
    

def PopupThanks():
    commonParams = ["#ffff80", ("Helvetica", 15)]
    easterEgg=0
    
    layoutPrep = [
                [sg.Text('Agradecimientos', text_color=commonParams[0], font=commonParams[1])],
                [sg.Text('Gracias a los alumnos de Azure Madrid', text_color="#ffafad",font=commonParams[1])],
                [sg.Text('Gracias a Francisco Luque', text_color="#ffafad",font=commonParams[1])],
            ]


    layoutMain = [[sg.Column(layoutPrep, element_justification='center')]]
    
    window = sg.Window(':)', layoutMain, icon=r'input/LogoIcon.png')

    while True:           
        event, values = window.read()
 
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
    window.close()
    
