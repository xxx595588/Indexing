import tkinter as tk
from search import search

frame = tk.Tk()
frame.title("CS 121 Search Engine")
frame.geometry('600x300')


def printResults():
    inp = inputtxt.get(1.0, "end-1c")
    retString = search(inp)
    resultsText.delete("1.0","end")
    resultsText.insert("1.0",retString)
    inputtxt.delete("1.0","end")



def handler(e):
    inp = inputtxt.get(1.0, "end-1c")
    retString = search(inp)
    resultsText.delete("1.0","end")
    resultsText.insert("1.0",retString)
    inputtxt.delete("1.0","end")



# Query Input
inputtxt = tk.Text(frame, height = 1, width = 50, relief="ridge")

inputtxt.pack(side = tk.TOP)

inputtxt.place(x = 100, y = 10)

# Search Button
printButton = tk.Button(frame, text = "Search", command = printResults)
printButton.pack(side = tk.BOTTOM)

printButton.place(x = 275, y = 40)

frame.bind('<Return>', handler)


# Results Text Box

scroll=tk.Scrollbar(frame, orient='vertical')

resultsText = tk.Text(frame, width=500,height = 14, yscrollcommand=scroll.set)
scroll.pack(side="right", fill='y')



resultsText.pack(side = tk.BOTTOM)
scroll.config(command=resultsText.yview)

frame.resizable(False,False) # prevent resizing of window
frame.mainloop()
