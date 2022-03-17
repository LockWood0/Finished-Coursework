#GUI Module
import tkinter as tk
from tkinter.messagebox import showinfo
from turtle import update
from PIL import Image, ImageTk
import customtkinter 

class HomeScreenWindow(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Home Screen")
        
        #Defines the colours for the GUI
        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'
        self.LINK_BLUE = '#CAE4F1'

        #Defining the size of the window 
        self.root.geometry("1000x600")
        self.root.resizable(False,False)

        #This makes the background picture
        self.Image = Image.open('Test4.jpg')
        self.background_image = ImageTk.PhotoImage(self.Image)
        self.background_image_label = tk.Label(image= self.background_image)

        self.background_image_label.image = self.Image
        self.background_image_label.place(x=0, y=0)

        #Adding the canvas
        self.canvas = tk.Canvas(self.root,
                                    width = 900, 
                                    height = 500, 
                                    bg =  self.WHITE)
        self.canvas.place(x = 50, y = 60)

        self.root.mainloop()
 

home = HomeScreenWindow()