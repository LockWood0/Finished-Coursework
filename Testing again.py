
import numpy as np
import matplotlib.pyplot as plt

def plotGraph():
    categories = ['Memory', 'Executive Function', 'Attention', 'Language']
    categories = [*categories, categories[0]]

    assessments_1 = [4, 4, 5, 4] #Valeus for each different catagories
    assessments_2 = [5, 5, 4, 5]
    assessments_3 = [3, 2, 1, 5]
    assessments_1 = [*assessments_1, assessments_1[0]] #Links the last node to the first node
    assessments_2 = [*assessments_2, assessments_2[0]]
    assessments_3 = [*assessments_3, assessments_3[0]]

    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(assessments_1))

    plt.figure(figsize=(6, 6)) 
    plt.subplot(polar=True)
    plt.plot(label_loc, assessments_1, label='Assessments 1') #Plotting each graph 
    plt.plot(label_loc, assessments_2, label='Assessments 2')
    plt.plot(label_loc, assessments_3, label='Assessments 3')
    plt.title('Previous Domain Assessments', size=20, y=1.05) #Title of grpah
    lines, labels = plt.thetagrids(np.degrees(label_loc), labels=categories)
    plt.legend()
    plt.show()

plotGraph()