#Imports for Radar Graoh 
from cgi import test
from email.errors import FirstHeaderLineIsContinuationDefect
import re
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from matplotlib.pyplot import show
import numpy as np

#Imports for tkinter 
import tkinter as tk
from tkinter.messagebox import showinfo
from xmlrpc.client import FastUnmarshaller
import customtkinter 
from PIL import Image, ImageTk

import pyodbc

from datetime import date

import AttentionTests
import MemoryTests
import ExecFunctionTests
import LangaugeTests

class MainMenu(object):
    def __init__(self, id):
        self.list_of_results = []
        self.id = id
        self.root = tk.Tk()
        self.root.title("Main Menu")

        #Defining the size of the window 
        self.root.geometry("996x664")
        self.root.resizable(False,False)

        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'

        #This makes the background picture
        self.Image = Image.open('mainScreen.jpg')
        self.background_image = ImageTk.PhotoImage(self.Image)
        self.background_image_label = tk.Label(image= self.background_image)

        self.background_image_label.image = self.Image
        self.background_image_label.place(x=0, y=0)

        #Canvas around everything
        self.canvas = tk.Canvas(self.root,
                                    width = 875, 
                                    height = 575, 
                                    bg =  '#FEFFFE')
        self.canvas.place(x = 55, y = 50)
        
        #Defines the sizes of the graph
        fig = Figure(figsize = (5, 5),
            dpi = 100) 

        #Updates the figure to have the graph, and plots the graph
        fig = self.plotGraph()

        #Canvas with graph on
        self.canvas = FigureCanvasTkAgg(fig, master = self.root)
        self.canvas.draw()
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().place(x=50, y=100)

         #Adding the title 
        self.title_label = tk.Label(self.root,
                                    text = "Suggestions:", 
                                    font = ("Century Gothic", 22), 
                                    fg = '#210124', 
                                    bg = '#FEFFFE')
        self.title_label.place(x = 660, y = 80)

        #Adding the word which chnages and the user has to recite
        self.changing_label = customtkinter.CTkLabel(self.root,
                                    text = "You have blank as your \n weakest area, to get\n stonger try: ",
                                    width=260,
                                    height=100,
                                    corner_radius=12,
                                    text_font= ("Century Gothic", 14),
                                    text_color= self.BLACK,
                                    fg_color=self.PASTEL_BLUE,
                                    bg_color = self.WHITE)
        self.changing_label.place(x = 615, y=160)
        
        #Button that begins the test
        self.most_suggested_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text_font = ("Century Gothic", 14),
                                    text="Most Suggested",
                                    command = self.mostSuggested, #Calls beginTest method
                                    border_width=5,
                                    corner_radius=10)
        self.most_suggested_button.place(x =665, y = 300)

        #Button that begins the test
        self.second_suggested_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text_font = ("Century Gothic", 14),
                                    text="2nd Suggested",
                                    command = self.secondMostSuggested, #Calls beginTest method
                                    border_width=5,
                                    corner_radius=10)
        self.second_suggested_button.place(x =670, y = 360)

        #Button that begins the test
        self.third_suggested_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text_font = ("Century Gothic", 14),
                                    text="3rd Suggested",
                                    command = self.thirdMostSuggested, #Calls beginTest method
                                    border_width=5,
                                    corner_radius=10)
        self.third_suggested_button.place(x =670, y = 420)

        self.changing_label.after(3000,self.personalDetailsCheck, id) #Calls the function

        self.root.mainloop()


    def plotGraph(self):
        #Defines the figure, fig size meaning in inches
        fig = Figure(figsize = (5, 5),
            dpi = 100)

        #Defines the catagories
        categories = ['Memory', 'Attention', 'Language', 'Executive Function']
        categories = [*categories, categories[0]] #This makes the a final entry which is the same as teh first so the graph joins back

        self.assessments_1 = [] #Pre defines the self variables
        self.assessments_2 =[]
        self.assessments_3 = []

        self.findResults(self.id) #Calls the query 

        graph1 = [
            self.assessments_1.memeMark, 
            self.assessments_1.atteMark, 
            self.assessments_1.langMark, 
            self.assessments_1.execMark] #Valeus for each different catagories
        
        #If they do not have a second assesment, the variable should not of updated, so
        #So if it is not empty it has a row
        if self.assessments_2 != []:
            graph2 = [
                self.assessments_2.memeMark, 
                self.assessments_2.atteMark, 
                self.assessments_2.langMark, 
                self.assessments_2.execMark]

        #If it doesnt we just make the graph nothing
        else:
            graph2 = [0, 0, 0, 0]

        if self.assessments_3 != []:
            graph3 = [
                self.assessments_3.memeMark, 
                self.assessments_3.atteMark, 
                self.assessments_3.langMark, 
                self.assessments_3.execMark]

        else:
            graph3 = [0, 0, 0, 0]

        graph1 = [*graph1, graph1[0]] #Links the last node to the first node
        graph2 = [*graph2, graph2[0]]
        graph3 = [*graph3, graph3[0]]

        plot1 = fig.add_subplot(polar=True)
        label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(graph1))

        #getting graph colours
        VIOLET = "#58508d"
        PINK = "#bc5090"
        YELLOW = "#ffa600"

        #Plotting graph 1, latest assesment 
        plot1.plot(label_loc, graph1, label='Latest Assessment', color = VIOLET)
        plot1.fill(label_loc, graph1, alpha = 0.25, color = VIOLET)

        #Plotting graph 2
        plot1.plot(label_loc, graph2, label='2nd Latest Assessment', color = PINK)
        plot1.fill(label_loc, graph2, alpha = 0.25, color = PINK)

        #Plotting graph 3
        plot1.plot(label_loc, graph3, label='3rd Latest Assessment', color = YELLOW)
        plot1.fill(label_loc, graph3, alpha = 0.25, color = YELLOW)

        #This plots the y axis and makes it always out of 5
        plot1.set_yticks([0, 1, 2, 3, 4, 5], color = "grey", size = 10)
        plot1.set_ylim(0,5)

        plot1.set_facecolor('#FEFFFE')

        plot1.set_title('Radar Graph of Assessments')
        lines, labels = plot1.set_thetagrids(np.degrees(label_loc), labels=categories)
        plot1.legend()

        return fig #Returns teh now completed graph


    def findResults(self,id):
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()


        sql = ("""
            SELECT AssementsTbl.memeMark, AssementsTbl.atteMark, AssementsTbl.langMark, AssementsTbl.execMark, AssementsTbl.dateCompleted, AssementsTbl.UserID
            FROM AssementsTbl
            WHERE (((AssementsTbl.UserID)=?))
            ORDER BY AssementsTbl.dateCompleted DESC;

        """)
        params = (id)
        cursor.execute(sql,params) #Finds asessments done by the user and organises by most recent

        x =0 

        for row in cursor.fetchall():
            if x == 0:
                self.assessments_1 = row #Updates the varibles so they each have one of the rows, we only need the three most recent
            elif x == 1:
                self.assessments_2 = row
            elif x ==2:
                self.assessments_3 = row

            x +=1 #Incrementing so we can deine the next row as an asessment


    def mostSuggested(self):
        most_suggested = self.list_of_results[0][0]
        mark = self.list_of_results[0][1]

        if most_suggested == "Attention":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                FIRST_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                FIRST_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "MEDIUM")
            else:
                FIRST_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "EASY")
            
            test_mark = FIRST_ADDDITIONAL_TEST.attention_mark
            total_mark = FIRST_ADDDITIONAL_TEST.total_attention

            FIRST_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window

        elif most_suggested == "Memory":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                FIRST_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                FIRST_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "MEDIUM")
            else:
                FIRST_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "EASY")
            
            test_mark = FIRST_ADDDITIONAL_TEST.memory_mark
            total_mark = FIRST_ADDDITIONAL_TEST.total_memory_mark

            FIRST_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window

        elif most_suggested == "Exec Function":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                FIRST_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                FIRST_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "MEDIUM")
            else:
                FIRST_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "EASY")
            
            test_mark = FIRST_ADDDITIONAL_TEST.exec_mark
            total_mark = FIRST_ADDDITIONAL_TEST.exec_total

            FIRST_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window
            
        elif most_suggested == "Language":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                FIRST_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                FIRST_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "MEDIUM")
            else:
                FIRST_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "EASY")
            
            test_mark = FIRST_ADDDITIONAL_TEST.language_mark
            total_mark = FIRST_ADDDITIONAL_TEST.language_total

            FIRST_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window
        
        else:
            showinfo("Window", "I'm sorry but an unecpected error has occured, please try again later")
    

    def secondMostSuggested(self):
        most_suggested = self.list_of_results[1][0]
        mark = self.list_of_results[1][1]
        if most_suggested == "Attention":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                SECOND_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                SECOND_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "MEDIUM")
            else:
                SECOND_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "EASY")
            
            test_mark = SECOND_ADDDITIONAL_TEST.attention_mark
            total_mark = SECOND_ADDDITIONAL_TEST.total_attention

            SECOND_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window

        elif most_suggested == "Memory":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                SECOND_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                SECOND_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "MEDIUM")
            else:
                SECOND_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "EASY")
            
            test_mark = SECOND_ADDDITIONAL_TEST.memory_mark
            total_mark = SECOND_ADDDITIONAL_TEST.total_memory_mark

            SECOND_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window

        elif most_suggested == "Exec Function":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                SECOND_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                SECOND_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "MEDIUM")
            else:
                SECOND_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "EASY")
            
            test_mark = SECOND_ADDDITIONAL_TEST.exec_mark
            total_mark = SECOND_ADDDITIONAL_TEST.exec_total

            SECOND_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window
        
        elif most_suggested == "Language":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                SECOND_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                SECOND_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "MEDIUM")
            else:
                SECOND_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "EASY")
            
            test_mark = SECOND_ADDDITIONAL_TEST.language_mark
            total_mark = SECOND_ADDDITIONAL_TEST.language_total

            SECOND_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window
        
        else:
            showinfo("Window", "I'm sorry but an unecpected error has occured, please try again later")


    def thirdMostSuggested(self):
        most_suggested = self.list_of_results[2][0]
        mark = self.list_of_results[2][1]
        if most_suggested == "Attention":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                THIRD_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                THIRD_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "MEDIUM")
            else:
                THIRD_ADDDITIONAL_TEST = AttentionTests.AttentionTest1(difficulty = "EASY")
            
            test_mark = THIRD_ADDDITIONAL_TEST.attention_mark
            total_mark = THIRD_ADDDITIONAL_TEST.total_attention

            THIRD_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window
            
        elif most_suggested == "Memory":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                THIRD_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                THIRD_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "MEDIUM")
            else:
                THIRD_ADDDITIONAL_TEST = MemoryTests.MemoryTest1(difficulty = "EASY")
            
            test_mark = THIRD_ADDDITIONAL_TEST.memory_mark
            total_mark = THIRD_ADDDITIONAL_TEST.total_memory_mark

            THIRD_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window

        elif most_suggested == "Exec Function":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                THIRD_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                THIRD_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "MEDIUM")
            else:
                THIRD_ADDDITIONAL_TEST = ExecFunctionTests.ExecutiveFunctionTest1(difficulty = "EASY")
            
            test_mark = THIRD_ADDDITIONAL_TEST.exec_mark
            total_mark = THIRD_ADDDITIONAL_TEST.exec_total

            THIRD_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window

        elif most_suggested == "Language":
            self.root.destroy() # Gets rid of the current main meu window
            if mark > 4: 
                THIRD_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "HARD") #Chekcs how difficult to make the additonal test
            elif mark >2:
                THIRD_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "MEDIUM")
            else:
                THIRD_ADDDITIONAL_TEST = LangaugeTests.LanguageTest1(difficulty = "EASY")
            
            test_mark = THIRD_ADDDITIONAL_TEST.language_mark
            total_mark = THIRD_ADDDITIONAL_TEST.language_total

            THIRD_ADDDITIONAL_TEST.logTest(test_mark, total_mark, self.id) #Logs the mark 
            WIN = MainMenu(self.id) #Re-calls the mainmenu window

        else:
            showinfo("Window", "I'm sorry but an unecpected error has occured, please try again later")
        

    def personalDetailsCheck(self,id):
        personal_record = self.queryForPersonalDetails(id) #Grabs the personal details from databse

        today = date.today() #Todays date
        date_of_birth_given = personal_record.DateofBirth.split("/") #Splits the value in the database by the "/"
        year_of_birth = date_of_birth_given[2] #Fins the one which correlates to year
        age = today.year - int(year_of_birth) #Makes the difference between the year they were born and now, e.g there age

        exercise_amounts_given = personal_record.AmountofExerciseDOne #Gets the radio buttom
        concussion_amounts_given = personal_record.Concussions #Gets the other radio button
        boolean_diabetes = personal_record.Diabetes
        boolean_heart_diabese = personal_record.HeartDisease
        heurisitc = self.heurisitcMaker(age, exercise_amounts_given, concussion_amounts_given, boolean_diabetes, boolean_heart_diabese)

        #Checks to see if they should see a doctor
        self.causeForCOncern(heurisitc, self.assessments_1)

        #Find worst area
        self.worstAreas(self.assessments_1)


    def worstAreas(self,recent_assessment):
        memory = recent_assessment.memeMark
        attention = recent_assessment.atteMark
        language = recent_assessment.langMark
        exec_function = recent_assessment.execMark

        #Making a list of results and sorting the,
        self.list_of_results = [
            ["Memory", memory],
            ["Attention", attention],
            ["Language", language],
            ["Exec Function", exec_function] ]
        self.list_of_results.sort(key= lambda x:x[1])
        
        print(self.list_of_results)


    def causeForCOncern(self,heuristic, latest_assessment):
        if (
            (heuristic > 4 and latest_assessment.memeMark == 0) or
            (heuristic > 4 and latest_assessment.atteMark == 0) or
            (heuristic > 4 and latest_assessment.langMark == 0) or
            (heuristic > 4 and latest_assessment.execMark == 0)
            ):
            showinfo("Window", "These results are a cause for concern please try and book an appointment with your doctor to discuss your memory")
            

    def heurisitcMaker(self, age, exercise_amounts_given, concussion_amounts_given, boolean_diabetes, boolean_heart_diabese):
        heuristic_modifier = 0

        #Decides how much your age will effect you cognitive preformance
        if age > 17:
            heuristic_modifier += 0
        elif age > 34:
            heuristic_modifier +=1
        elif age > 44:
            heuristic_modifier +=2
        elif age >54:
            heuristic_modifier +=2
        elif age > 64:
            heuristic_modifier += 3
        elif age >74:
            heuristic_modifier += 4
        elif age >84:
            heuristic_modifier += 5

        #Exercise amount given heurisitic decide 
        if exercise_amounts_given == 102:
            heurisitc_modifer += 1
        elif exercise_amounts_given == 103:
            heurisitc_modifer += 2
        elif exercise_amounts_given == 104:
            heurisitc_modifer += 3

        #Conussion Amount
        if concussion_amounts_given == 202:
            heuristic_modifier += 5
        elif concussion_amounts_given == 203:
            heuristic_modifier += 3

        if boolean_diabetes == 1:
            heuristic_modifier += 3

        if boolean_heart_diabese == 1:
            heuristic_modifier +=3

        return heuristic_modifier


    def queryForPersonalDetails(self,id):
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()


        sql = ("""
            SELECT HabitsTbl.DateofBirth, HabitsTbl.AmountofExerciseDOne, HabitsTbl.Concussions, HabitsTbl.Diabetes, HabitsTbl.HeartDisease
            FROM HabitsTbl
            WHERE (((HabitsTbl.UserID)=?));

        """) #IFnds the details if it is the same USer ID the user has


        params = (id)
        cursor.execute(sql,params) #Finds asessments done by the user and organises by most recent

        for row in cursor.fetchall():
            personal_record = row #Gets the row
        
        return (personal_record)
