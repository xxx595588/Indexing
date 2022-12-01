import tkinter as tk
from search import search

frame = tk.Tk()
frame.title("CS 121 Search Engine")
frame.geometry('600x300')


def printResults():
    inp = inputtxt.get(1.0, "end-1c")
    retString = search(inp)
    lbl.config(text = retString)


def handler(e):
    inp = inputtxt.get(1.0, "end-1c")
    retString = search(inp)
    lbl.config(text = retString)

# Query Input
inputtxt = tk.Text(frame,
                   height = 1,
                   width = 50)

inputtxt.pack(side = tk.BOTTOM)

inputtxt.place(x = 100, y = 10)

# Search Button
printButton = tk.Button(frame,
                        text = "Search",
                        command = printResults)
printButton.pack(side = tk.BOTTOM)

printButton.place(x = 275, y = 40)

frame.bind('<Return>', handler)


# Results Label
lbl = tk.Label(frame, text = "", wraplength=500)
lbl.pack(side = tk.BOTTOM, ipady = 30)

frame.resizable(False,False) # prevent resizing of window
frame.mainloop()
