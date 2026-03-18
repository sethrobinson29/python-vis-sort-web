# GUI for Sorter object as defined in sorter.py
# By Seth Robinson https://github.com/sethrobinson29 
from sorter import *
from math import *

root = Tk()
root.config(background="#297373")
root.geometry("1100x850")
root.title("vis-sort")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

titleFrame = Frame(root, background="#297373")
titleFrame.grid(row=0)
title = Label(titleFrame, text="Sorting Algorithm Visualizer", fg="#be97c6", font=("Helvetica bold", 40), background="#2e294e", padx=20)
title.config(highlightbackground="#000034", highlightthickness=4, relief="raised")
title.grid(row=0, pady=10)
# credit = Label(titleFrame, text="By Seth Robinson", fg="#be97c6", font=("Helvetica bold", 15), background="#2e294e", padx=10)
# credit.config(highlightbackground="#000034", highlightthickness=4, relief="raised")
# credit.grid(row=1, pady=10)

canFrame = Frame(root,highlightbackground="#2e294e", highlightthickness=2, relief="raised")
canFrame.grid(row=1, pady=5)
can = Sorter(canFrame)
can.canvas.pack()

# frame for bottom row of main window
lowFrame = Frame(root, background="#297373", pady=5, padx=20)
lowFrame.grid(row=2)

# comparisons output
compFrame = Frame(lowFrame, background="#000034", highlightbackground="#2e294e", highlightthickness=4, relief="ridge", pady=5, padx=20)
compFrame.grid(row=0, column=0)
compsLabel = Label(compFrame, text="Comparisons: ", background="#000034", fg="#be97c6", font="Helvetica 10")
compsLabel.grid(row=0, column=0)
compsDisplay = Label(compFrame, text="0", background="#000034", fg="#be97c6", font="Helvetica 10")
compsDisplay.grid(row=0, column=1)

# frame spacing
lowFrameSpace1 = Label(lowFrame, background="#297373", padx=10, text=" ")
lowFrameSpace1.grid(row=0, column=1)
lowFrameSpace2 = lowFrameSpace1 = Label(lowFrame, background="#297373", padx=10, text=" ")
lowFrameSpace1.grid(row=0, column=3)

# frame for buttons
bFrame = Frame(lowFrame, background="#000034", highlightbackground="#2e294e", highlightthickness=4, relief="ridge", pady=5, padx=20)
bFrame.grid(row=0, column=2)

# frame for sorting buttons
sortFrame = Frame(bFrame, pady=5, background="#000034")
sortFrame.grid(row=0)

# sorting buttons
bubble = Button(sortFrame, bg="#be97c6", text="Bubble", command=lambda:(buttonClicked("bubble")), font="Helvetica 12")
bubble.grid(row=0, column=0, padx=5)
selection = Button(sortFrame, bg="#be97c6", text="Selection", command=lambda:(buttonClicked("selection")) , font="Helvetica 12")
selection.grid(row=0, column=1, padx=5)
mergeButton = Button(sortFrame, bg="#be97c6", text="Merge", command=lambda:(buttonClicked("merge")) , font="Helvetica 12")
mergeButton.grid(row=0, column=2, padx=5)
quickButton = Button(sortFrame, bg="#be97c6", text="Quick", command=lambda:(buttonClicked("quick")) , font="Helvetica 12")
quickButton.grid(row=0, column=3, padx=5)
radix = Button(sortFrame,bg="#be97c6", text="Radix", command=lambda: (buttonClicked("radix")) , font="Helvetica 12")
radix.grid(row=0, column=4, padx=5)

# frame for utility buttons
utilFrame = Frame(bFrame, pady=5, background="#000034")
utilFrame.grid(row=1)

# utility buttons
backwards = Button(utilFrame, bg="#be97c6", text="Reverse", command=lambda: (buttonClicked("reverse")), font="Helvetica 12")
backwards.grid(row=0, column=1, padx=5)
# p = Button(midFrame, bg="#be97c6", text="print", command=lambda: (print(vals)))               # print sorter.vals to console
# p.grid(row=0, column=1, padx=5)
genNums = Button(utilFrame, bg="#be97c6", text="Create New Array", command=lambda:(buttonClicked("new")), font="Helvetica 12")
genNums.grid(row=0, column=0, padx=5)
closeProgram = Button(utilFrame, bg="#be97c6", fg="#f31227", text="Quit", command=lambda: (buttonClicked("quit")), font="Helvetica 12 bold")
closeProgram.grid(row=0,  column=2, padx=5)

# change length of array based on scale
def scaleChange(event):
    if can.numBars != barScale.get():
        tmp = barScale.get()
        barScaleDisplay.config(text=tmp)
        can.makeNewVals(tmp)
        compsDisplay.config(text=0)

# scale frame
scaleFrame = Frame(lowFrame, background="#000034", highlightbackground="#2e294e", highlightthickness=4, relief="ridge", pady=5, padx=20)
scaleFrame.grid(row=0, column=4)

# scale for setting length of array to be sorted
barScale = Scale(scaleFrame,from_=100, to=500, orient=HORIZONTAL, resolution=5, bg="#000034", fg="#be97c6", highlightbackground="#2e294e", highlightthickness=4, troughcolor="#be97c6", activebackground="#2e294e", font="Helvetica 10")
barScale.bind("<ButtonRelease-1>", scaleChange)
barScale.grid(row=2, columnspan=2)

# scale label and display 
barLabelFrame = Frame(scaleFrame, background="#000034", highlightbackground="#2e294e", highlightthickness=4, relief="ridge", pady=5, padx=20) 
barLabelFrame.grid(row=0, columnspan=2)
barScaleLabel = Label(barLabelFrame, text="Size of Array ", background="#000034", fg="#be97c6", font="Helvetica 10")
barScaleLabel.grid(row=0, column=0)
barScaleDisplay = Label(barLabelFrame, text=barScale.get(), background="#000034", fg="#be97c6", font="Helvetica 10")
barScaleDisplay.grid(row=0, column=1)
scaleFrameSpace1 = Label(scaleFrame, background="#000034",  text=" ")
scaleFrameSpace1.grid(row=1, columnspan=2)

# initialize sorting 
can.makeNewVals(barScale.get())

# wrapper for button handling
def buttonClicked(buttonName):
    # sort 
    if buttonName == "bubble":
        can.bubbleSort()
    elif buttonName == "selection":
        can.selectionSort()
    elif buttonName == "merge":
        can.mergeSortWrap()
    elif buttonName == "quick":
        can.quickSortWrap()
    elif buttonName == "radix":
        can.radixSort()
    elif buttonName == "reverse":
        can.reverse()
    elif buttonName == "new":
        can.makeNewVals(barScale.get())
    elif buttonName == "quit":
        root.destroy()
    
    # update comparison display
    compsDisplay.config(text=can.comps)

if __name__ == "__main__":
    root.mainloop()