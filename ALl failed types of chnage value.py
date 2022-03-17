import random
def changeValue(self):
    easy_word_list = ["Face", "Velvet", "Church", "Daisy", "Red"]
    values_back = self.chooseRandomWord(easy_word_list) #Picks the random word

    word_chosen = values_back[0]
    easy_word_list = values_back[1]
    finished = values_back[2]
    
    if finished is True:
        self.changing_label.after(2000, "Please now enter the words")
    else:
        self.changing_label.config(text = word_chosen)
        self.changing_label.after(2000, self.changeValue2)
    
def changeValue2(self):
    easy_word_list = ["Face", "Velvet", "Church", "Daisy", "Red"]
    index = random.randint(0,len(easy_word_list)-1)
    while easy_word_list != []:
        word_chosen = easy_word_list[index]
        self.changing_label.config(text = word_chosen)
        self.changing_label.after(2000,None)
        print(word_chosen)
        easy_word_list.pop(index)
        if easy_word_list != []:
            index = random.randint(0,len(easy_word_list)-1) #FInding a new word
        
        self.root.mainloop()

        #self.changing_label.after(2000, self.changeValue)

def changeValue3(self,word_chose,list,Finished):
    #Choose word from list
    if Finished is True:
        self.changing_label.after(2000, "Done")

    else:
        self.changing_label.after(2000,word_chose)
        self.pickAWord(list)

def pickAWord(self,list):
    easy_word_list = ["Face", "Velvet", "Church", "Daisy", "Red"]
    if list == None:
        index = random.randint(0,len(easy_word_list)-1)
        word_chosen = easy_word_list.pop(index)
        self.changeValue3(word_chosen, easy_word_list, False)
    
    elif list == []:
        self.changeValue3(None, None, True)
    
    else:
        index = random.randint(0,len(list)-1)
        word_chosen = list.pop(index)
        self.changeValue3(word_chosen, list, False)
        
    #Pop that word from list
    #Display that word
    #Repeat until list is empty 



def chooseRandomWord(self,easy_word_list):
    if len(easy_word_list) <1:
        return None,None, True

    chosen_word = random.choices(easy_word_list)
    value = self.linearsearch(easy_word_list,chosen_word[0]) #FInds the word's position in list
    easy_word_list.pop(value) #Pop it from the list

    return chosen_word[0],easy_word_list,False

def linearsearch(self,arr, desired_word):
    for i in range(len(arr)):
        if arr[i] == desired_word:
            return i
    return -1
