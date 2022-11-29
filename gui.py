import tkinter as tk
from search import search

frame = tk.Tk()
frame.title("Search Engine")
frame.geometry('600x300')

  
def printResults():
    inp = inputtxt.get(1.0, "end-1c")
    retString = search(inp)
    lbl.config(text = retString)

 
# Query Input 
inputtxt = tk.Text(frame,
                   height = 1,
                   width = 50)
  
inputtxt.pack()
  
# Search Button 
printButton = tk.Button(frame,
                        text = "Search", 
                        command = printResults)
printButton.pack()



# Results Label
lbl = tk.Label(frame, text = "", wraplength=500)
lbl.pack()
frame.resizable(False,False) # prevent resizing of window 
frame.mainloop()