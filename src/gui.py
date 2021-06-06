import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import ToolTip
import requests
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import os
from socket import gaierror
import random
import re

from src.db import SqlConnection, GetThings
from src.popups import PopupHelp, PopupThanks, PopupImage

app_title = 'ExamMaker-V0.3'
sg.SetOptions(font='any 11', auto_size_buttons=True, progress_meter_border_depth=0, border_width=1)
sg.set_global_icon('input/LogoIcon.ico')

menu_def = [['Archivo', ['Salir']],['Ayuda', ["Agradecimientos", 'Acerca de...']]]

#Thanks MikeTheWatchGuy
def place(elem):
    return sg.Column([[elem]], pad=(0,0))

def AnswerGui(cur, realAnswer, userAnswer, Sentence, justification):

    layout = [
        
        [sg.Column([[sg.Text(Sentence,font=('Helvetica', 16,), text_color="Yellow", background_color="Blue")],], vertical_alignment='center', justification='center')],
        [sg.Column([[sg.Text(f"Elegiste {userAnswer} y la respuesta correcta es {realAnswer}", key="-CORRECT-")]], vertical_alignment='center', justification='center')],
        [sg.Text("")],
        [sg.Multiline(default_text= GetThings(cur, justification, option="Justification"),size=(43,5), key="-JUS-", disabled=True, enter_submits=False)],
        [sg.Column([[sg.Button('OK')]], vertical_alignment='center', justification='center')]
        
    ]

    window = sg.Window('ExamMaker - Answer', layout, icon='input/LogoIcon.ico')
    while True:
        event, values = window.read()

        if event == "OK":
            break

        if event is None or event == 'Exit' or event == "Salir":
            break
            
    window.close()


def ConclusionGui(con, windowTest, windowInitial, totalAnswers, correctAnswers):

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

    window = sg.Window('ExamMaker - Answer', layout, icon='input/LogoIcon.ico')
    while True:
        event, values = window.read()

        if event == "OK":
            break

        if event is None or event == 'Exit' or event == "Salir":
            break

    if os.path.exists("TestDB.db"):
        con.close()
        os.remove("TestDB.db")
    windowInitial.close()
    windowTest.close()
    window.close()


def TestGui(con, cur, numberQuest, questChoice, windowInitial):

    randomQuestions = random.sample(range(1,numberQuest+1), questChoice)
    n = 0
    correct = 0
    layout = [
        [sg.Text(GetThings(cur, randomQuestions[n], option="Category"), font=('Helvetica', 16), justification='left', key='-CAT-'),
            sg.Text(font=('Helvetica', 16),size =(12,1), justification='right', key='-TIME-'),
            sg.Text(f'{n+1} de {questChoice}', size =(10,1), key="-COUNTER-",justification="right", font=("Helvetica", 16))],
        [sg.Text('')],
        [sg.Frame("Pregunta", layout=[[sg.Multiline
               (default_text= GetThings(cur, randomQuestions[n]),
                size=(42,5), key="-QUESTION-", disabled=True, enter_submits=False)]])],
        [sg.pin(sg.Column([[sg.Text('')],[sg.Button('VER IMAGEN ADJUNTA A LA PREGUNTA', key="-IMAGE-",enable_events=True, visible=True)]], 
                    key = "-COLIMAGE-",visible=False, vertical_alignment='center', justification='center', element_justification='center',expand_x=True, expand_y=True),expand_x=True, vertical_alignment='center',expand_y=True)],
        [sg.Text('')],
        [sg.Frame("Posibles Respuestas", layout=[[sg.Multiline
               (default_text= GetThings(cur, randomQuestions[n], option="Answer"),
                size=(42,5), key="-ANSWER-", disabled=True, enter_submits=False)]])],
        [sg.Text('')],
        [sg.InputText('Respuesta elegida: ', size=(39,1), readonly=True, key='-IN-'), 
            sg.Button(image_filename="input/DeleteAnswer.png", key="-DELETE-", enable_events=True,image_size=(40,30), image_subsample=13)],
        [sg.Text('')],
        [sg.Button('A',size=(12,1),visible=True), sg.Button('B',size=(12,1),visible=True), sg.pin(sg.Button('C',size=(12,1),visible=False))],
        [sg.pin(sg.Button('D',size=(12,1),visible=False)), sg.pin(sg.Button('E',size=(12,1),visible=False)), sg.pin(sg.Button('F',size=(12,1),visible=False))],
        [sg.Text('')],
        [sg.Column([[sg.Button('Confirmar Respuesta', key="-ENTER-", enable_events=True)]], vertical_alignment='center', justification='center')]
    ]

    window = sg.Window('ExamMaker', layout,icon='input/LogoIcon.ico')

    timeRunning, counter = True, 0
    answerNeeds = True
    answerMulti, answerCount = True, 0
    answerImage =True
    
    while True:
        event, values = window.read(timeout=10)
        if answerMulti == True:
            correctManager = GetThings(cur, randomQuestions[n], option="Correct")
            correctCounter = len(correctManager.split(","))
            if correctCounter >=2:
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas:'
            else:
                answerFormatted = f'Respuesta elegida:'
            window.Element("-IN-").Update(value=answerFormatted)
            answerMulti=False

        if answerImage==True:
            imageManager = GetThings(cur, randomQuestions[n], option="Image")
            if imageManager!=None:
                window.Element("-COLIMAGE-").update(visible=True)
            elif imageManager==None:
                window.Element("-COLIMAGE-").update(visible=False)
            answerImage=False

        if answerNeeds == True:
            answerManager = GetThings(cur, randomQuestions[n], option="answer")
            answerCounter = len(re.findall("[A-Z][.]", answerManager))
            if answerCounter ==2:
                window.Element("C").update(visible=False)
                window.Element("D").update(visible=False)
                window.Element("E").update(visible=False)
                window.Element("F").update(visible=False)
            elif answerCounter ==3:
                window.Element("C").update(visible=True)
                window.Element("D").update(visible=False)
                window.Element("E").update(visible=False)
                window.Element("F").update(visible=False)
            elif answerCounter ==4:
                window.Element("C").update(visible=True)
                window.Element("D").update(visible=True)
                window.Element("E").update(visible=False)
                window.Element("F").update(visible=False)
            elif answerCounter ==5:
                window.Element("C").update(visible=True)
                window.Element("D").update(visible=True)
                window.Element("E").update(visible=True)
                window.Element("F").update(visible=False)
            elif answerCounter ==6:
                window.Element("C").update(visible=True)
                window.Element("D").update(visible=True)
                window.Element("E").update(visible=True)
                window.Element("F").update(visible=True)
            answerNeeds = False
            

        if timeRunning == True:
            window.Element('-TIME-').update('{:02d}:{:02d}:{:02d}'.format((counter // 100)//3600,(counter // 100) // 60, (counter // 100) % 60))
            counter += 1
        
        if event is None or event == 'Exit' or event == "Salir":
            break

        if event == "-IMAGE-":
            imageManager = GetThings(cur, randomQuestions[n], option="Image")
            PopupImage(imageManager)

        if event =="-DELETE-":
            answerFormatted = f'Respuesta elegida:'
            if correctCounter >=2:
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas:'
                answerCount = 0
            else:
                answerFormatted = f'Respuesta elegida:'
                answerCount = 0
            window.Element("-IN-").Update(value=answerFormatted)

        if event in 'ABCDEF':
    
            if answerCount ==0:
                answerChoice = event
                if correctCounter >=2:
                    answerChoice1 = event
                    answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}'
                    window.Element("-IN-").Update(value=answerFormatted)
                    userAnswer = answerChoice1
                    answerCount += 1
                else:
                    answerFormatted = f'Respuesta elegida: {answerChoice}'
                    window.Element("-IN-").Update(value=answerFormatted)
                    userAnswer = answerChoice
            elif answerCount ==1 and correctCounter >=2:
                answerChoice2 = event
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}, {answerChoice2}'
                window.Element("-IN-").Update(value=answerFormatted)
                userAnswer = f"{answerChoice1},{answerChoice2}"
                answerCount +=1
            elif answerCount ==2 and correctCounter >=3:
                answerChoice3 = event
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}, {answerChoice2}, {answerChoice3}'
                window.Element("-IN-").Update(value=answerFormatted)
                userAnswer = f"{answerChoice1},{answerChoice2},{answerChoice3}"
                answerCount +=1
            elif answerCount ==3 and correctCounter ==4:
                answerChoice4 = event
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}, {answerChoice2}, {answerChoice3}, {answerChoice4}'
                window.Element("-IN-").Update(value=answerFormatted)
                userAnswer = f"{answerChoice1},{answerChoice2},{answerChoice3},{answerChoice4}"
                answerCount +=1
        

        if event == "-ENTER-":
            try:
                realAnswer = GetThings(cur, randomQuestions[n], option="Correct").split(",")
                userAnswer = userAnswer.split(",")
                realAnswer.sort()
                userAnswer.sort()
                if realAnswer == userAnswer:
                    correct+=1
                    AnswerGui(cur,realAnswer,userAnswer, "BIEN", randomQuestions[n])
                else:
                    AnswerGui(cur,realAnswer,userAnswer, "MAL", randomQuestions[n])


                if n != len(randomQuestions)-1:
                    n +=1
                    window.Element("-QUESTION-").Update(GetThings(cur, randomQuestions[n]))
                    window.Element("-ANSWER-").Update(GetThings(cur, randomQuestions[n], option="Answer"))
                    window.Element("-COUNTER-").Update(f'{n+1} de {questChoice}')
                    answerCount=0
                    answerImage=True
                    answerMulti = True
                    answerNeeds = True
                    
                else:
                    ConclusionGui(con, window, windowInitial,len(randomQuestions), correct)
                    break

            except AttributeError:
                sg.Popup("No has introducido respuesta",icon='input/LogoIcon.ico')
                continue

            except UnboundLocalError:
                sg.Popup("No has introducido respuesta",icon='input/LogoIcon.ico')
                continue

    if os.path.exists("TestDB.db"):
        con.close()
        os.remove("TestDB.db")
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
                sg.FileBrowse(button_text = "Seleccionar", file_types = [('Archivos zip', '*.zip')], key="-SUB1-", change_submits=True, enable_events=True, tooltip="Selecciona la base de datos")],
            [sg.Text('No se ha introducido DB', size=ParamsH2[0], font=ParamsH3[1],text_color="#ffafad", key="-INF1-")],
            ])],

            [sg.Text("", font=ParamsEmpty[1])],

            [sg.Text("Preguntas para examen:", size=ParamsH3[0], font=ParamsH3[1]), 

            sg.Combo(size=(10,5), auto_size_text=False, readonly=True, enable_events=True, tooltip="Desactivado. Selecciona DB antes", default_value=[0],values=[0], disabled=True,  key="-LIST1-")],

            [sg.Text("", size=ParamsEmpty[0])]
    ]


    OnlineLayout = [
            [sg.Menu(menu_def, tearoff=True)],
            [sg.Text("", size=ParamsEmpty[0])],

            [sg.Frame('Insertar Base de datos online', layout=[
            [sg.Text("", font=ParamsEmpty[1])],
            [sg.Text("Selecciona la DB: ", size=ParamsH3[0], font=ParamsH3[1]), 
            sg.Combo(values=[], readonly=True, tooltip="Pulsa'Refrescar'",key="-FILE2-",size=ParamsH3[0], font=ParamsH3[1], enable_events=True), 
                sg.Button("Refrescar", key="-SUB2-", change_submits=True, enable_events=True)],
            [sg.Text('No se ha introducido DB', size=ParamsH2[0], font=ParamsH3[1],text_color="#ffafad", key="-INF2-")],
            ])],

            [sg.Text("", font=ParamsEmpty[1])],

            [sg.Text("Preguntas para examen:", size=ParamsH3[0], font=ParamsH3[1]), 

            sg.Combo(size=(10,5),auto_size_text=False, readonly=True, enable_events=True, default_value=[0],values=[0], disabled=True,  key="-LIST2-")],

            [sg.Text("", size=ParamsEmpty[0])]
    
    ]

    layout = [[sg.TabGroup(
        [[sg.Tab('BBDD Offline', OfflineLayout), sg.Tab('BBDD Online', OnlineLayout)]], enable_events=True,key='-TABS-')],
        [sg.Button('OK', size=ParamsH3[0], font=ParamsH3[1], key="-OK-", disabled=True, tooltip="Desactivado. Se necesita insertar número de preguntas y database válida")],
    ]
    
    checkTab= 2
    window = sg.Window('ExamMaker - Pantalla inicial', layout, icon='input/LogoIcon.ico')
    while True:
        event, values = window.read()
        
        if event == "-TABS-":
            if checkTab ==1:
                checkTab=2
            else:
                checkTab=1
                
        if event == "-OK-":
            window.Hide()
            TestGui(con, cur, numberQuest, questChoice, window)

        elif event == f"-FILE{checkTab}-":
            try:
                if event == "-FILE2-":
                    dbSelected = requests.get(f"https://raw.githubusercontent.com/Alexvidalcor/ExamMaker/master/databases/{values['-FILE2-']}")
                    password = sg.popup_get_text("Introduce aquí la contraseña:", title="ExamMaker - Contraseña",
                                             keep_on_top=True,
                                             password_char="*",
                                             grab_anywhere=False,
                                             icon='input/LogoIcon.ico')
                    if password == None:
                        window.Element(f"-INF{checkTab}-").Update("DB no desencriptada")
                        continue
                    with ZipFile(BytesIO(dbSelected.content)) as zf:
                        zf.extractall(pwd=bytes(password,'utf-8'))
                        con, cur = SqlConnection("TestDB.db")
                        
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
                        con, cur = SqlConnection("TestDB.db")
            except BadZipFile:
                window.Element(f"-INF{checkTab}-").Update("ZIP no válido")
                continue
            except RuntimeError:
                window.Element(f"-INF{checkTab}-").Update("Contraseña no válida")
                continue
            except FileNotFoundError:
                window.Element(f"-INF{checkTab}-").Update("Error raro")
                continue
            
            if cur == False:
                window.Element(f"-INF{checkTab}-").Update("DB no válida")

            else:
                cur.execute("SELECT COUNT(*) FROM MainTest")
                numberQuest = cur.fetchall()[0][0]
                    
                window.Element(f'-INF{checkTab}-').Update(f"Número de preguntas introducidas: {numberQuest}", text_color="#ffff80")
                window.Element(f'-LIST{checkTab}-').Update(values=list(range(1,numberQuest+1)), disabled=False, readonly = True)
                window.Element(f"-LIST{checkTab}-").set_tooltip("Selecciona número de preguntas que tendrá el examen")
                
                
        elif event == f"-SUB2-":
            try:
                dbRequest = requests.get("https://api.github.com/repos/Alexvidalcor/ExamMaker/contents/databases?ref=master")
                window.Element(f"-INF{checkTab}-").Update("Conectado a internet")
                namesDB = [element["name"] for element in dbRequest.json()]
                window.Element(f"-FILE{checkTab}-").Update(values=namesDB, size=(20,1))
            except Exception:
                window.Element(f"-INF{checkTab}-").Update("Sin conexión a internet")
                continue
                
        elif event ==f"-LIST{checkTab}-":
            questChoice = values[f"-LIST{checkTab}-"]
            window.Element("-OK-").Update(disabled=False)
            window.Element("-OK-").set_tooltip("¡Ánimo y suerte!")
        
        elif event == "Acerca de...":
            PopupHelp()
        elif event == "Agradecimientos":
            PopupThanks()

        if event is None or event == 'Exit' or event == "Salir":
            break
    
    if os.path.exists("TestDB.db"):
        con.close()
        os.remove("TestDB.db")
    window.close()        


