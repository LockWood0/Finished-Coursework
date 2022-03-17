from cProfile import label
from cmath import polar
from math import degrees
from tracemalloc import stop
from turtle import width
from matplotlib import lines
import matplotlib.pyplot as plt 
import numpy as np 
import pygal 

#data
catagories = ['Memory', 'Executive Function', 'Attention', 'Language']

person1 = [2,3,5,4]
person1 = np.concatenate((person1,[person1[0]])) #This means that the graph links together

person2 = [4,4,2,1]
person2 = np.concatenate((person2,[person2[0]]))

person3 = [0,1,2,3]
person3 = np.concatenate((person3,[person3[0]]))

#calculates evenly-spaced co-ordinates
#Use radians for polar plot 
label_placement = np.linspace(start = 0, stop = 2*np.pi, num = len(person1))

print(2*np.pi, 'radians = ', np.degrees(2*np.pi), 'degrees')

print('radians', label_placement)
print('degrees', np.degrees(label_placement))

plt.figure(figsize= (5,5))
plt.subplot(polar = True)
plt.plot(label_placement, person1)
plt.plot(label_placement, person2)
plt.plot(label_placement, person3)

lines, labels = plt.thetagrids(np.degrees(label_placement), labels = catagories)

plt.title('Compare People', y = 1.1, fontdict = {'fontsize': 18})
plt.legend(labels = ['Person 1', 'Person 2', 'Person 3'], loc = (0.95,0.8));

radar_chart = pygal.Radar(width=500, height = 400)
radar_chart.title = 'Compare People'
radar_chart.x_labels = ['Memory', 'Executive Function', 'Attention', 'Language']
radar_chart.add('Person 1', [2,3,5,4])
radar_chart.add('Person 2', [4,4,2,1])
radar_chart.add('Person 3', [0,1,2,3])
radar_chart