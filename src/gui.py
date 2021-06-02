import PySimpleGUIWeb as sg
import requests
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import os
from socket import gaierror
import random
import re

from db import SqlConnection, GetThings
from popups import PopupHelp, PopupThanks, PopupImage



def AnswerGui(cur, realAnswer, userAnswer, Sentence, justification):

    layout = [
        [sg.Text(Sentence, font=('Helvetica', 16,), text_color="Yellow", background_color="Blue")],
        [sg.Text(f"Elegiste {userAnswer} y la respuesta correcta es {realAnswer}",key="-CORRECT-")],
        [sg.Text("")],
        [sg.Multiline(default_text=GetThings(cur, justification, option="Justification"), size=(
            43, 5), key="-JUS-", disabled=True, enter_submits=False)],
        [sg.Button('OK')]
    ]

    window = sg.Window('ExamMaker - Answer', layout, web_port=2228, web_start_browser=False)

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
        [sg.Text(
            f"Has acertado {correctAnswers} de un total de {totalAnswers} preguntas posibles")],
        [sg.Text(
            f"Este hecho representa una tasa de acierto del {perCorrect}")],
        [sg.Text(f"RESULTADO FINAL = {checkPass}")],
        [sg.Button('OK')]
    ]

    window = sg.Window('ExamMaker - Answer', layout, web_port=2228, web_start_browser=False)
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
    InitialGui()
    window.close()
    


def TestGui(con, cur, numberQuest, questChoice, windowInitial):
    randomQuestions = random.sample(range(1, numberQuest+1), questChoice)
    n = 0
    correct = 0
    layout = [
        [sg.Text(GetThings(cur, randomQuestions[n], option="Category"), font=('Helvetica', 16), justification='left', key='-CAT-'),
            sg.Text(font=('Helvetica', 16), size=(12, 1), justification='right', key='-TIME-'),
            sg.Text(f'{n+1} de {questChoice}', size=(11, 1), key="-COUNTER-", justification="right", font=("Helvetica", 16))],

        [sg.Text('')],

        [sg.Multiline(default_text=GetThings(cur, randomQuestions[n]),size=(43, 5), key="-QUESTION-", disabled=True, enter_submits=False)],

        [sg.Text('', key="-SPACE1-", visible=False)],

        [sg.Button('VER IMAGEN ADJUNTA A LA PREGUNTA', key="-IMAGE-", enable_events=True, visible=False)],

        [sg.Text('')],

        [sg.Multiline(default_text=GetThings(cur, randomQuestions[n], option="Answer"),size=(43, 5), key="-ANSWER-", disabled=True, enter_submits=False)],

        [sg.Text('')],

        [sg.Text('Respuesta elegida: ', size=(40, 1), key='-IN-'), sg.Button("Borrar", key="-DELETE-", enable_events=True)],

        [sg.Text('')], 

        [sg.Button('A', size=(11, 1), visible=True), 
        sg.Button('B', size=(11, 1), visible=True), 
        sg.Button('C', size=(11, 1))],

        [sg.Button('D', size=(11, 1)), 
        sg.Button('E', size=(11, 1)), 
        sg.Button('F', size=(11, 1))],

        [sg.Text('')],
        [sg.Button('Confirmar Respuesta', key="-ENTER-", enable_events=True)]]

    window = sg.Window('ExamMaker', layout, web_port=2228, web_start_browser=False)

    timeRunning, counter = True, 0
    answerNeeds = True
    answerMulti, answerCount = True, 0
    answerImage = True

    while True:
        event, values = window.read(timeout=10)
        if answerMulti == True:
            correctManager = GetThings(
                cur, randomQuestions[n], option="Correct")
            correctCounter = len(correctManager.split(","))
            if correctCounter >= 2:
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas:'
            else:
                answerFormatted = f'Respuesta elegida:'
            window.Element("-IN-").Update(value=answerFormatted)
            answerMulti = False

        if answerImage == True:
            imageManager = GetThings(cur, randomQuestions[n], option="Image")
            if imageManager != None:
                window.Element("-IMAGE-").update(visible=True)
                window.Element("-SPACE1-").update(visible=True)
            elif imageManager == None:
                window.Element("-SPACE1-").update(visible=False)
                window.Element("-IMAGE-").update(visible=False)
            answerImage = False

        if answerNeeds == True:
            answerManager = GetThings(cur, randomQuestions[n], option="answer")
            answerCounter = len(re.findall("[A-Z][.]", answerManager))

        if timeRunning == True:
            window.Element('-TIME-').update('{:02d}:{:02d}:{:02d}'.format(
                (counter // 100)//3600, (counter // 100) // 60, (counter // 100) % 60))
            counter += 1

        if event is None or event == 'Exit' or event == "Salir":
            break

        if event == "-IMAGE-":
            imageManager = GetThings(cur, randomQuestions[n], option="Image")
            PopupImage(imageManager)

        if event == "-DELETE-":
            answerFormatted = f'Respuesta elegida:'
            if correctCounter >= 2:
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas:'
                answerCount = 0
            else:
                answerFormatted = f'Respuesta elegida:'
                answerCount = 0
            window.Element("-IN-").Update(value=answerFormatted)

        if event in 'ABCDEF':

            if answerCount == 0:
                answerChoice = event
                if correctCounter >= 2:
                    answerChoice1 = event
                    answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}'
                    window.Element("-IN-").Update(value=answerFormatted)
                    userAnswer = answerChoice1
                    answerCount += 1
                else:
                    answerFormatted = f'Respuesta elegida: {answerChoice}'
                    window.Element("-IN-").Update(value=answerFormatted)
                    userAnswer = answerChoice
            elif answerChoice1 in 'ABCDEF':
                answerChoice2 = event
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}, {answerChoice2}'
                window.Element("-IN-").Update(value=answerFormatted)
                userAnswer = f"{answerChoice1},{answerChoice2}"
                answerCount += 1
            elif answerChoice2 in 'ABCDEF':
                answerChoice3 = event
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}, {answerChoice2}, {answerChoice3}'
                window.Element("-IN-").Update(value=answerFormatted)
                userAnswer = f"{answerChoice1},{answerChoice2},{answerChoice3}"
                answerCount += 1
            elif answerChoice3 in 'ABCDEF':
                answerChoice4 = event
                answerFormatted = f'(MULTI-{correctCounter}) Respuestas elegidas: {answerChoice1}, {answerChoice2}, {answerChoice3}, {answerChoice4}'
                window.Element("-IN-").Update(value=answerFormatted)
                userAnswer = f"{answerChoice1},{answerChoice2},{answerChoice3},{answerChoice4}"
                answerCount += 1

        if event == "-ENTER-":
            try:
                realAnswer = GetThings(
                    cur, randomQuestions[n], option="Correct").split(",")
                userAnswer = userAnswer.split(",")
                realAnswer.sort()
                userAnswer.sort()
                if realAnswer == userAnswer:
                    correct += 1
                    AnswerGui(cur, realAnswer, userAnswer,
                              "BIEN", randomQuestions[n])
                else:
                    AnswerGui(cur, realAnswer, userAnswer,
                              "MAL", randomQuestions[n])

                if n != len(randomQuestions)-1:
                    n += 1
                    window.Element(
                        "-QUESTION-").Update(GetThings(cur, randomQuestions[n]))
                    window.Element(
                        "-ANSWER-").Update(GetThings(cur, randomQuestions[n], option="Answer"))
                    window.Element(
                        "-COUNTER-").Update(f'{n+1} de {questChoice}')
                    answerCount = 0
                    answerImage = True
                    answerMulti = True
                    answerNeeds = True

                else:
                    ConclusionGui(con, window, windowInitial,
                                  len(randomQuestions), correct)
                    break

            except AttributeError:
                sg.Popup("No has introducido respuesta",
                         icon=r'input/LogoIcon.png')
                continue

            except UnboundLocalError:
                sg.Popup("No has introducido respuesta",
                         icon=r'input/LogoIcon.png')
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
    ParamsEmpty = [(1, 1), ("any 1")]

    layout = [
            [sg.Text("A ver que tal", font=ParamsH3[1])],
        
            [sg.Input(key='-IN-', password_char = "*"), sg.Button('Go')],

            [sg.Text('No se ha introducido DB', size=ParamsH2[0],
                     font=ParamsH3[1], text_color="#ffafad", key="-INF-")],

            [sg.Text("Número de preguntas:", size=ParamsH3[0], font=ParamsH3[1]), sg.Combo(values=list(range(1,3)), key="-LIST-")],
            
            [sg.Button('OK')]]




    window = sg.Window('ExamMaker - Web', layout, web_port=2228, web_start_browser=True)
    while True:
        event, values = window.read()
        print(event)

        if event == "OK":
            window.Hide()
            questChoice = int(values["-LIST-"][0])
            TestGui(con, cur, numberQuest, questChoice, window)

        elif event == "Go":
            try:

                dbSelected = requests.get(f"https://raw.githubusercontent.com/Alexvidalcor/ExamMaker/master/databases/AzureV1.zip")
                password = values['-IN-']
                if password == None:
                    window.Element("-INF-").Update("DB no desencriptada")
                    continue
                with ZipFile(BytesIO(dbSelected.content)) as zf:
                    zf.extractall(pwd =bytes(password,'utf-8'))
                    con, cur= SqlConnection("TestDB.db")


            except BadZipFile:
                window.Element("-INF{-").Update("ZIP no válido")
                continue
            except RuntimeError:
                window.Element("-INF-").Update("Contraseña no válida")
                continue
            except FileNotFoundError:
                window.Element("-INF-").Update("Error raro")
                continue

            if cur == False:
                window.Element("-INF-").Update("DB no válida")

            else:
                cur.execute("SELECT COUNT(*) FROM MainTest")
                numberQuest= cur.fetchall()[0][0]

                window.Element('-INF-').Update(f"Número de preguntas introducidas: {numberQuest}", text_color ="#ffff80")
            

        if event is None or event == 'Exit' or event == "Salir":
            break

    if os.path.exists("TestDB.db"):
        con.close()
        os.remove("TestDB.db")
    window.close()



