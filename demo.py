from tkinter import *

win = Tk()

# 做一个点击后关闭点击按钮的按钮
def button_click():
    global button, label
    button.destroy()
    label.config(text="Button clicked!")

label = Label(win, text="Click the button")
label.pack()
button = Button(win, text="Click me", command=button_click)
button.pack()

win.mainloop()
        

