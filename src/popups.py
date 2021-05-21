import PySimpleGUI as sg

import webbrowser

def PopupHelp():
    commonParams = ["#ffff80", ("Helvetica", 15)]
    easterEgg=0
    
    layout = [
                [sg.Text('Versión de ExamMaker:', text_color=commonParams[0], font=commonParams[1]),
                 sg.Text('0.3', enable_events=True,key = "-VERSION-", tooltip="Click para ver novedades", text_color="#ffafad",font=commonParams[1])],
                
                [sg.Text('Autor:', text_color=commonParams[0], font=commonParams[1]),
                 sg.Text('Alexvidalcor', enable_events=True,key = "-AUTHOR-", text_color="#ffafad",font=commonParams[1])],
                
                [sg.Text("", size=(1,1))],
                
                [sg.Button('Código fuente', key="-URL-"),
                 sg.Button('Actualizaciones',key = "-CHECK-", disabled=True, tooltip="Función no implementada")],
            ]


    layout = [[sg.Column(layout, element_justification='center')]]
    
    window = sg.Window('Detalles', layout)

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