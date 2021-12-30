
from tkinter import *
import random
#from tkinter.font import *

root = Tk()
root.geometry("600x300")


def repeat():
    global timer
    rand = random.randint(1, 100)
    # configuring the tag, to overcome over writing of text.
    cv.itemconfigure('rand', text="Number: "+str(rand))
    # asking to repeat it, you can change the interval.
    timer = root.after(1000, repeat)

def stop():
    root.after_cancel(timer)

cv = Canvas(root, width=200, height=200, bg="blue")
#styles = Font(family="calibri",size=30,weight="bold")
cv.create_text(100, 100, font=("calibri", 20, "bold"),
               fill="lightblue", tag='rand')  # added a tag
cv.pack()

b_start = Button(root, text='Start', command=repeat,width=10)
b_start.pack(pady=10)

b_stop = Button(root, text='Stop', command=stop,width=10)
b_stop.pack(padx=10)

root.mainloop()