# 用 tkinter 写一个简单的字幕播放器
import tkinter as tk
root = tk.Tk()
root.title("字��播放器")
root.geometry("800x600")

label = tk.Label(root, text="Hello, World!")


label.pack()

def text():
    # 删除 label 中的文本
    label.config(text="")
    # 添加新的文本
    label.config(text="Button clicked!")

    print("Button clicked!")

button = tk.Button(root, text="Click Me", command=lambda: text())
button.pack(side="top")


root.mainloop()
