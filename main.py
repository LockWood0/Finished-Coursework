from calendar import month
from re import M
from tkinter.messagebox import showinfo

import Registration as Rg
import Login as Lg

import Personal_Info as Pi
import MainMenu as Ma

import pyodbc
from datetime import date

def main():
    REG_WINDOW = Rg.RegWindow()
    if REG_WINDOW.new_user_added == True: #Personal Dteail window only made if new user was made
        PI_WINDOW =  Pi.PersonalInfoWindow()

        #Gettign variables from test
        exercisise_var = PI_WINDOW.exercisise_var
        concussions_var = PI_WINDOW.concussions_var
        cal_var = PI_WINDOW.cal_var

        #Checkbox
        has_diabetes = PI_WINDOW.has_diabetes
        has_heart_disease = PI_WINDOW.has_heart_disease
    

    LOG_IN_WINDOW = Lg.LogInWindow()
    #Going to make a branch if last login was greater than two months

    id = LOG_IN_WINDOW.user_id #Gets the id of the user:

    if REG_WINDOW.new_user_added == True: #This means the results are only added if a new user was added
        PI_WINDOW.addDetails(
                    id,
                    cal_var,
                    exercisise_var,
                    concussions_var,
                    has_diabetes,
                    has_heart_disease,)

    d2 = databaseQuery(id)
    diff = months_between(d2)

    if REG_WINDOW.new_user_added == True or diff >2:
        initialAssessment(id) #I put it all in one function to make main simpiler

    MAIN_WINDOW = Ma.MainMenu(id)



def initialAssessment(id):
    import InitialTest 
    MEMORY_TEST = InitialTest.MemoryTestInitial() #Makes LieRamemory test window

    memory_mark = MEMORY_TEST.memory_mark
    total_memory_mark = MEMORY_TEST.total_memory_mark
    if id  == '': #Just in case they put nothing in the login we wont add an assessment with nothing
        print("Error leave go and re-do your login")
        main()

    MEMORY_TEST.logMark(memory_mark, total_memory_mark, id)

    ATTENTION_TEST = InitialTest.AttentionTestInital() #Makes attention test window

    attention_mark = ATTENTION_TEST.attention_mark
    total_attention_mark = ATTENTION_TEST.total_attention
    ATTENTION_TEST.logAttentionMarks(attention_mark,total_attention_mark,id)

    LANGUAGE_TEST = InitialTest.LanguageTestInitial()

    language_mark = LANGUAGE_TEST.language_mark
    language_total = LANGUAGE_TEST.language_total
    LANGUAGE_TEST.logLanguageMarks(language_mark,language_total,id)

    EXECUTIVE_TEST = InitialTest.ExecutiveFunctionInital()

    exec_mark = EXECUTIVE_TEST.exec_mark
    exec_total = EXECUTIVE_TEST.exec_total
    EXECUTIVE_TEST.logExecutiveFunctionMarks(exec_mark,exec_total,id)


def databaseQuery(id):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
    cursor = conn.cursor()


    sql = ("""
        SELECT UsersTbl.DateofLastLogin
        FROM UsersTbl
        WHERE (((UsersTbl.UserID)=?));
    """) #IFnds the details if it is the same USer ID the user has


    params = (id)
    cursor.execute(sql,params) #Finds asessments done by the user and organises by most recent

    for row in cursor.fetchall():
        personal_record = row #Gets the row
    
    return (personal_record.DateofLastLogin)

def months_between(d2):
    total_months = d2.year*12 + d2.month

    today = date.today()
    total_month_today = today.year*12 + today.month

    diff = total_month_today - total_months #Makes the difference between the year they were born and now, e.g there age
    return diff

if __name__ == '__main__': 
    main()
