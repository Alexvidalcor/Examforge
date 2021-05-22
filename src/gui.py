import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import ToolTip
import requests
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import os

from src.db import SqlConnection
from src.question import *
from src.popups import *

app_title = 'ExamMaker-V0.3'
sg.SetOptions(font='any 11', auto_size_buttons=True, progress_meter_border_depth=0, border_width=1)

menu_def = [['Archivo', ['Salir']],['Ayuda', ["Agradecimientos", 'Acerca de...']]]



def AnswerGui(cur, realAnswer, userAnswer):

    layout = [
        [sg.Text(f"Elegiste {userAnswer} y la respuesta correcta es {realAnswer[1]}", key="-CORRECT-")],
        [sg.Text(realAnswer[0], key="-ANSWER-", size=(80,30))],
        [sg.Button('OK')]
    ]

    window = sg.Window('ExamMaker - Answer', layout)
    while True:
        event, values = window.read()

        if event == "OK":
            break

        if event is None or event == 'Exit' or event == "Salir":
            break
            
    if os.path.exists("testDB.db"):
          os.remove("testDB.db")
    window.close()


def ConclusionGui(windowTest, windowInitial, totalAnswers, correctAnswers):

    perCorrect = correctAnswers/totalAnswers
    if perCorrect >= 0.7:
        checkPass = "APROBADO"
    else:
        checkPass = "SUSPENSO"

    layout = [
        [sg.Text(f"Has acertado {correctAnswers} de un total de {totalAnswers} preguntas posibles")],
        [sg.Text(f"Este hecho representa una tasa de acierto del {perCorrect}")],
        [sg.Text(f"RESULTADO FINAL = {checkPass}")],
        [sg.Button('OK')]
    ]

    window = sg.Window('ExamMaker - Answer', layout)
    while True:
        event, values = window.read()

        if event == "OK":
            break

        if event is None or event == 'Exit' or event == "Salir":
            break

    if os.path.exists("testDB.db"):
          os.remove("testDB.db")
    windowInitial.close()
    windowTest.close()
    window.close()





def TestGui(cur, numberQuest, questChoice, windowInitial):

    randomQuestions = random.sample(range(1,numberQuest+1), questChoice)
    n = 0
    correct = 0
    layout = [[sg.Text(GetThings(cur, randomQuestions[n]), size=(80,30), key="-QUESTION-")],
        [sg.InputText('Respuesta elegida: ', readonly=True, key='-IN-')],
        [sg.Text('Elige tu respuesta:', key='-OUT-')],
        [sg.Button('A'), sg.Button('B'), sg.Button('C')],
        [sg.Button('D'), sg.Button('E'), sg.Button('F')],
        [sg.Button('Enter')]
    ]

    window = sg.Window('Teams Exam', layout)

    while True:
        event, values = window.read()

        if event is None or event == 'Exit' or event == "Salir":
            break

        elif event in 'ABCDEF':
            answerFormatted = f'Respuesta elegida: {event}'
            window.Element("-IN-").Update(value=answerFormatted)
            userAnswer = event

        elif event == "Enter":
            realAnswer = GetThings(cur, randomQuestions[n], question=False)
            AnswerGui(cur,realAnswer,userAnswer)
            if realAnswer[1] == userAnswer:
                correct+=1
            
            if n != len(randomQuestions)-1:
                n +=1
                window.Element("-QUESTION-").Update(GetThings(cur, randomQuestions[n]))
            else:
                ConclusionGui(window, windowInitial,len(randomQuestions), correct)
                break

    if os.path.exists("testDB.db"):
          os.remove("testDB.db")
    windowInitial.close()
    window.close()



def InitialGui():

    ParamsH1 = [(45, 1), ("Helvetica", 18)]
    ParamsH2 = [(45, 1), ("Helvetica", 15)]
    ParamsH3 = [(20, 1), ("Helvetica", 12)]
    ParamsEmpty=[(1,1),("any 1")]
 

    OfflineLayout = [
            [sg.Menu(menu_def, tearoff=True)],
            [sg.Text("", size=ParamsEmpty[0])],

            [sg.Frame('Insertar Base de datos offline', layout=[
            [sg.Text("", font=ParamsEmpty[1])],
            [sg.Text("Selecciona la DB: ", size=ParamsH3[0], font=ParamsH3[1]), 
            sg.Input(key="-FILE1-",size=ParamsH3[0], font=ParamsH3[1], enable_events=True), 
                sg.FileBrowse(button_text = "Seleccionar", key="-SUB1-", change_submits=True, enable_events=True, tooltip="Selecciona la base de datos")],
            [sg.Text('No se ha introducido DB', size=ParamsH2[0], font=ParamsH3[1],text_color="#ffafad", key="-INF1-")],
            ])],

            [sg.Text("", font=ParamsEmpty[1])],

            [sg.Text("Número de preguntas:", size=ParamsH3[0], font=ParamsH3[1]), 

            sg.Listbox(size=(10,1), enable_events=True, tooltip="Desactivado. Selecciona DB antes", default_values=[0],values=[0], disabled=True,  key="-LIST1-")],

            [sg.Text("", size=ParamsEmpty[0])]
    ]


    OnlineLayout = [
            [sg.Menu(menu_def, tearoff=True)],
            [sg.Text("", size=ParamsEmpty[0])],

            [sg.Frame('Insertar Base de datos online', layout=[
            [sg.Text("", font=ParamsEmpty[1])],
            [sg.Text("Selecciona la DB: ", size=ParamsH3[0], font=ParamsH3[1]), 
            sg.Combo(values=[],tooltip="Pulsa'Refrescar'",key="-FILE2-",size=ParamsH3[0], font=ParamsH3[1], enable_events=True), 
                sg.Button("Refrescar", key="-SUB2-", change_submits=True, enable_events=True)],
            [sg.Text('No se ha introducido DB', size=ParamsH2[0], font=ParamsH3[1],text_color="#ffafad", key="-INF2-")],
            ])],

            [sg.Text("", font=ParamsEmpty[1])],

            [sg.Text("Número de preguntas:", size=ParamsH3[0], font=ParamsH3[1]), 

            sg.Listbox(size=(10,1),auto_size_text=False, enable_events=True, default_values=[0],values=[0], disabled=True,  key="-LIST2-")],

            [sg.Text("", size=ParamsEmpty[0])]
    
    ]

    layout = [[sg.TabGroup(
        [[sg.Tab('BBDD Offline', OfflineLayout), sg.Tab('BBDD Online', OnlineLayout)]], enable_events=True,key='-TABS-')],
        [sg.Button('OK', size=ParamsH3[0], font=ParamsH3[1], key="-OK-", disabled=True, tooltip="Desactivado. Se necesita insertar número de preguntas y database válida")],
    ]
    
    checkTab= 2
    window = sg.Window('ExamMaker - Pantalla inicial', layout)
    while True:
        event, values = window.read()
        
        if event == "-TABS-":
            if checkTab ==1:
                checkTab=2
            else:
                checkTab=1
                
        if event == "-OK-":
            window.Hide()
            TestGui(cur, numberQuest, questChoice, window)

        elif event == f"-FILE{checkTab}-":
            try:
                if event == "-FILE2-":
                    dbSelected = requests.get(f"https://raw.githubusercontent.com/Alexvidalcor/ExamMaker/master/databases/{values['-FILE2-']}")
                    password = sg.popup_get_text("Introduce aquí la contraseña:", title="ExamMaker - Contraseña",
                                             keep_on_top=True,
                                             password_char="*",
                                             grab_anywhere=False)
                    if password == None:
                        window.Element(f"-INF{checkTab}-").Update("DB no desencriptada")
                        continue
                    with ZipFile(BytesIO(dbSelected.content)) as zf:
                        zf.extractall(pwd=bytes(password,'utf-8'))
                        cur = SqlConnection("testDB.db")
                        
                else:
                    password = sg.popup_get_text("Introduce aquí la contraseña:", title="ExamMaker - Contraseña",
                                             keep_on_top=True,
                                             password_char="*",
                                             grab_anywhere=False)
                    if password == None:
                        window.Element(f"-INF{checkTab}-").Update("DB no desencriptada")
                        continue
                    with ZipFile(values[f"-SUB{checkTab}-"]) as zf:
                        zf.extractall(pwd=bytes(password,'utf-8'))
                        cur = SqlConnection("testDB.db")
            except BadZipFile:
                window.Element(f"-INF{checkTab}-").Update("ZIP no válido")
                continue
                
                
    
            if cur == False:
                window.Element(f"-INF{checkTab}-").Update("DB no válida")

            else:
                cur.execute("SELECT COUNT(*) FROM MainTest")
                numberQuest = cur.fetchall()[0][0]
                    
                window.Element(f'-INF{checkTab}-').Update(f"Número de preguntas introducidas: {numberQuest}", text_color="#ffff80")
                window.Element(f'-LIST{checkTab}-').Update(values=list(range(1,numberQuest+1)), disabled=False)
                window.Element(f"-LIST{checkTab}-").set_tooltip("Haz click encima para seleccionar")
                
                
        elif event == f"-SUB2-":
            dbRequest = requests.get("https://api.github.com/repos/Alexvidalcor/ExamMaker/contents/databases?ref=master")
            namesDB = [element["name"] for element in dbRequest.json()]
            window.Element(f"-FILE{checkTab}-").Update(values=namesDB, size=(20,1))
            
        elif event ==f"-LIST{checkTab}-":
            questChoice = values[f"-LIST{checkTab}-"][0]
            window.Element("-OK-").Update(disabled=False)
            window.Element("-OK-").set_tooltip("¡Ánimo y suerte!")
        
        elif event == "Acerca de...":
            PopupHelp()

        if event is None or event == 'Exit' or event == "Salir":
            break
    
    if os.path.exists("testDB.db"):
          os.remove("testDB.db")
    window.close()        


