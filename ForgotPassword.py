#GUI Module
import tkinter as tk
from tkinter.messagebox import showinfo
from turtle import update
from PIL import Image, ImageTk
import customtkinter 

#Databse Module
import pyodbc

#Hash Module
from hashlib import sha256

#Module for changing date of last login
from datetime import date

import random
import string

import SendEmail

import re

class ForgotPassowrdWindow(object):
    def __init__(self, id):
        #Gets user ID
        self.user_id= id
        self.code = ""

        self.root = tk.Tk()
        self.root.title("Forgot Password")

        self.canvas = tk.Canvas(self.root, width = 500, height = 500)
        
        #Defines the colours for the GUI
        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'
        self.LINK_BLUE = '#CAE4F1'

        #Defining the size of the window 
        self.root.geometry("800x500")
        self.root.resizable(False,False)

        #This makes the background picture
        self.Image = Image.open('backgroundPic.jpg')
        self.background_image = ImageTk.PhotoImage(self.Image)
        self.background_image_label = tk.Label(image= self.background_image)

        self.background_image_label.image = self.Image
        self.background_image_label.place(x=0, y=0)
 
        #Adding the canvas
        self.canvas = tk.Canvas(self.root,
                                    width = 400, 
                                    height = 400, 
                                    bg =  self.WHITE)
        self.canvas.place(x = 200, y = 60)

        #Adding the labels
        self.username_label = tk.Label(self.root,
                                    text = "Forgot my Password", 
                                    font = ("Century Gothic", 30), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.username_label.place(x = 205, y = 80)

        self.email_label = tk.Label(self.root,
                                    text = "Email:", 
                                    font = ("Century Gothic", 10), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.email_label.place(x = 280, y = 160)

        #Adding username entry with custom tkinter thingy
        self.email_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.email_entry.place(x = 280, y = 180)

        #CLear button
        self.send_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Send verification code",
                                    command= self.checkAndSendCode,
                                    border_width=5,
                                    corner_radius=10)
        self.send_button.place(x = 300, y = 220)

        self.verify_label = tk.Label(self.root,
                                    text = "Verification Code:", 
                                    font = ("Century Gothic", 10), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.verify_label.place(x = 280, y = 260)

        #Adding username entry with custom tkinter thingy
        self.verify_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.verify_entry.place(x = 280, y = 280)

        self.change_password_label = tk.Label(self.root,
                                    text = "Change Password to: ", 
                                    font = ("Century Gothic", 10), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.change_password_label.place(x = 280, y = 320)

        self.change_password_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.change_password_entry.place(x = 280, y = 340)

        #confirm_button using custom
        self.confirm_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Confirm",
                                    command = self.validateGiven, #Calls login function
                                    border_width=5,
                                    corner_radius=10)
        self.confirm_button.place(x =340, y = 380)

        self.root.mainloop()

    def checkAndSendCode(self):
        email_var = self.email_entry.get()
        valid = self.checkEmailValid(email_var)
        if valid == False:
            showinfo("Window", "Email is not valid")
            return None

        showinfo("Window", "Email found and verification code sent")
        self.code = self.makeVerificationCode()
        #SendEmail.sendEmail(self.code, email_var)

        #Get rid of later 
        print(self.code)


    def checkEmailValid(self,email):
        special_characters = "@"
        if any(c in special_characters for c in email): #Check for if password has symbols
            pass
        else:
            #Failed symbol check
            return(False)
        return(True)


    def makeVerificationCode(self):
        # get random password pf length 8 with letters, digits, and symbols
        characters = string.ascii_letters + string.digits + string.punctuation
        verification_code = ''.join(random.choice(characters) for i in range(8))
        return verification_code

    
    def validateGiven(self):
        given_code = self.verify_entry.get()
        new_password = self.change_password_entry.get()
        if self.code != given_code:
            showinfo("Window", "Verification code not the same")
            return None
        
        valid = self.entryValidation(new_password)
        if valid == True:
            hashed_password = self.hashPassword(new_password)
            self.updatePassword(self.id, hashed_password)

        else:
            return None


    def entryValidation(self, password_to_check):
        valid = True
        reason = None
        if password_to_check == "": #Pressence check
            #Failed pressence check
            valid = False
            showinfo("Window", "Please remember to write in the test boxes before submitting.") #Creates alert box

        has_number = re.findall("[0-9]",password_to_check) #Check to see if password has a number
        if has_number:
            pass
        else:
            #Failed number check
            valid = False
            reason = "characters_in_password"
        

        special_characters = "!@#$%^&*()-+?_=,<>/"
        if any(c in special_characters for c in password_to_check): #Check for if password has symbols
            pass
        else:
            #Failed symbol check
            valid = False
            reason = "characters_in_password"

        has_number = re.findall("[A-Z]",password_to_check) #Check for one capital letter
        if has_number:
            pass
        else:
            #Failed capital check
            valid = False
            reason = "characters_in_password"


        if reason == None: #To see if the reason was to do with type check
            pass
        elif reason == "characters_in_password":
            showinfo("Window", "A password must contain at least: 1 Number, 1 Lowercase letter, 1 Uppercase letter and 1 symbol")


        return valid

       
    def updatePassword(self,username_given,password):
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
            UPDATE UsersTbl
            SET Password = ? 
            WHERE Username= ?
        """)
        params = (password, username_given)
        conn.execute(sql,params) #Finds the password of user
        conn.commit()

    def hashPassword(self,password_to_hash):
        h = sha256()
        password_to_hash = password_to_hash.encode('UTF-8')
        h.update(password_to_hash)
        hash = h.hexdigest()

        return hash
