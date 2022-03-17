import tkinter as tk
from tkinter.messagebox import showinfo
from xmlrpc.client import FastUnmarshaller
import customtkinter 
from PIL import Image, ImageTk

class MemoryTestInitial(object):
    def __init__(self):
        #Initalising of variables
        self.total_memory_mark = 0
        self.memory_mark = 0

        number_of_words_shown = 0 #Initialisng the number of words shown to user
        list_of_words_shown = [] #Intialising the list of words that will be shown variable
        self.times_submit_pressed = 0
        self.finished = False

        #This creates the Tkinter window
        self.root = tk.Tk()
        self.root.title("Memory Test")

        self.canvas = tk.Canvas(self.root, width = 630, height = 630)
        
        #Defines the colours for the GUI
        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'

        #Defining the size of the window 
        self.root.geometry("996x664")
        self.root.resizable(False,False)

        #This makes the background picture
        self.Image = Image.open('mainScreen.jpg')
        self.background_image = ImageTk.PhotoImage(self.Image)
        self.background_image_label = tk.Label(image= self.background_image)

        self.background_image_label.image = self.Image
        self.background_image_label.place(x=0, y=0)

        self.canvas = tk.Canvas(self.root,
                                    width = 480, 
                                    height = 480, 
                                    bg =  '#FEFFFE')
        self.canvas.place(x = 75, y = 50)

        self.root.mainloop()

win = MainMenu()