import PySimpleGUI as sg

from src.db import SqlConnection
from src.question import *

def AnswerGui(cur, realAnswer, userAnswer):

    layout = [
        [sg.Text(f"Elegiste {userAnswer} y la respuesta correcta es {realAnswer[1]}", key="-CORRECT-")],
        [sg.Text(realAnswer[0], key="-ANSWER-", size=(80,30))],
        [sg.Button('OK')]
    ]

    window = sg.Window('Teams Exam - Answer', layout)
    while True:
        event, values = window.read()

        if event == "OK":
            break

        elif event is None or event == 'Exit':
            break

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

    window = sg.Window('Teams Exam - Answer', layout)
    while True:
        event, values = window.read()

        if event == "OK":
            break

        elif event is None or event == 'Exit':
            break

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

        if event is None or event == 'Exit':
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

    windowInitial.close()
    window.close()



def InitialGui():

    commonParams = [(30, 1), (10, 1), ("Helvetica", 12), (20, 1), (38, 1)]

    layout = [[sg.Text('Introduce los siguientes datos para iniciar el examen:', size=(50, 2), font=commonParams[2])],
    [sg.Text("Selecciona la DB: "), sg.Input(key="-FILE-", change_submits=True), sg.FileBrowse(button_text = "Seleccionar", key="-FILEBROWSER-"), sg.Button("Aceptar", key = "-SUB-")],
    [sg.Text('No se ha introducido DB', size=commonParams[0], font=commonParams[2], key="-INF-")],
    [sg.Text("Selecciona el número de preguntas:"), sg.Listbox(size=commonParams[1], enable_events=True, default_values=[0],values=[0], disabled=True,  key="-LIST-")],
    [sg.Button('OK', key="-OK-", disabled=True)]]

    window = sg.Window('Teams Exam - Answer', layout)
    while True:
        event, values = window.read()
        if event == "-OK-":
            window.Hide()
            TestGui(cur, numberQuest, questChoice, window)

        elif event == "-SUB-":
            cur = SqlConnection(values["-FILEBROWSER-"])

            if cur == False:
                sg.Popup("Base de datos no válida")

            else:
                cur.execute("SELECT COUNT(*) FROM MainExam")
                numberQuest = cur.fetchall()[0][0]

                window.Element('-INF-').Update(f"Número de preguntas introducidas: {numberQuest}")
                window.Element('-LIST-').Update(values=list(range(1,numberQuest+1)), disabled=False)
        
        elif event =="-LIST-":
            questChoice = values["-LIST-"][0]
            window.Element("-OK-").Update(disabled=False)

        if event is None or event == 'Exit':
            break
        
    window.close()        














