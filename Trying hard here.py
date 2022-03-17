from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import numpy as np

# plot function is created for
# plotting the graph in
# tkinter window
def plot():

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                dpi = 100)

    # list of squares
    assessments_1 = [4, 4, 5, 4] #Valeus for each different catagories
    assessments_2 = [5, 5, 4, 5]
    assessments_3 = [3, 2, 1, 5]
    assessments_1 = [*assessments_1, assessments_1[0]] #Links the last node to the first node
    assessments_2 = [*assessments_2, assessments_2[0]]
    assessments_3 = [*assessments_3, assessments_3[0]]

    plot1 = fig.add_subplot(polar=True)
    label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(assessments_1))

    # plotting the graph
    plot1.plot(label_loc, assessments_1, label='Assessments 1')
    plot1.plot(label_loc, assessments_2, label='Assessments 2')
    plot1.plot(label_loc, assessments_3, label='Assessments 3')

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                            master = window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# the main Tkinter window
window = Tk()

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("500x500")

# button that displays the plot
plot_button = Button(master = window,
					command = plot,
					height = 2,
					width = 10,
					text = "Plot")

# place the button
# in main window
plot_button.pack()

# run the gui
window.mainloop()
