import random 




def GetThings(cur, idQuestion, question=True):

    if question == True:
        cur.execute(f"SELECT ID,Question FROM MainExam WHERE ID ={idQuestion}")
        questionExtract = cur.fetchall()[0][1]
        return questionExtract

    elif question == False:
        cur.execute(f"SELECT ID,Answers FROM MainExam WHERE ID ={idQuestion}")
        answerExtract = cur.fetchall()[0][1]

        cur.execute(f"SELECT ID,Correct FROM MainExam WHERE ID ={idQuestion}")
        correctExtract = cur.fetchall()[0][1]

        return answerExtract, correctExtract

