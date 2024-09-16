import json
from tkinter import *
from tkinter import messagebox

DEBUG = None
JSONPATH = ".\\tloos.json"
COUNTINI = ".\\count.ini"
count = None
read_line = 0

def logout(text):
    import time
    print(f"[{time.strftime('%H:%M:%S', time.localtime())}] {text}")
    with open(".\\log.log", "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S', time.localtime())}] {text}\n")

def exit():
    import sys
    with open(COUNTINI, "w", encoding="UTF-8") as f:
        f.write(str(DEBUG)+"\n")
        f.write(str(JSONPATH)+"\n")
        f.write(str(COUNTINI)+"\n")
        f.write(str(count)+"\n")
        f.write(str(read_line)+"\n")
    sys.exit()       

class READ:
    def __init__(self) -> None:
        self.read_root_line = read_line
        with open(JSONPATH, "r", encoding="UTF-8") as f:
            self.data = json.load(f)
            self.read_debug()
            self.read_count()
            logout("read json ok")
            logout(self.data)
    
    def read_count(self):
        global DEBUG, JSONPATH, COUNTINI, count, read_line
        with open(COUNTINI, "r", encoding="UTF-8") as f:
            DEBUG = bool(f.readline())
            JSONPATH = str(f.readline())
            COUNTINI = str(f.readline())
            count = dict(f.readline())
            read_line = int(f.readline())
            logout("count...ok")
    
    def read_count(self):
        global count
        count = self.data["count"]
        logout(count)

    def read_debug(self):
        global DEBUG
        DEBUG = self.data["count"]["DEBUG"]
        logout(DEBUG)
    
    def read_text(self):
        if type(self.data["root"][self.read_root_line]) == str:
            return self.data["root"][self.read_root_line]
    
    def read_button(self):
        if type(self.data["root"][self.read_root_line]) == dict and "buuton" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
    
    def read_input(self):
        if type(self.data["root"][self.read_root_line]) == dict and "input" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]

    def read_run(self):
        if type(self.data["root"][self.read_root_line]) == dict and "run" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
    
    def read_count(self):
        if type(self.data["root"][self.read_root_line]) == dict and "count" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
        
class RUN_READ:
    def __init__(self) -> None:
        self.read = READ()
        self.win = WIN()
    
    def run_text(self):
        global read_line
        self.win.win_text(self.read.read_text())
        logout(self.read.read_text())
    

class WIN:
    def __init__(self) -> None:
        self.win = Tk()
        self.win.title("subtitle player")
        self.win.geometry("350x200")
        self.win.resizable(False, False)
        
        self.button_up = Button(self.win, text="Up", command=lambda: self.win_button_up())
        # 大小
        self.button_up.pack(padx=10, pady=10, anchor="n")

        self.button_down = Button(self.win, text="Down", command=lambda: self.win_button_down())
        self.button_down.pack(padx=10, pady=10, anchor="sw")

        self.data = READ().data

        logout("init...ok")
    
    def win_button_up(self):
        global read_line
        logout("Up")
        if not read_line == 0:
            read_line -= 1
            logout(read_line)
        else:
            messagebox.showinfo("提示", "已经是第一行了！")
            logout("not UP")
    
    def win_button_down(self):
        global read_line
        logout("Down")
        if not read_line == len(self.data["root"])-1:
            read_line += 1
            logout(read_line)
        else:
            messagebox.showinfo("提示", "已经是最后一行了！")
            logout("not Down")

    def win_loop(self):
        logout("loop...ok")
        self.win.mainloop()
    
    def win_text(self, text):
        text_label = Label(self.win)
        text_label.config(text=text)
        text_label.pack()

class RUN():
    def __init__(self) -> None:
        self.read = READ()
        self.win = WIN()
    
    def run(self):
        self.win.win_loop()


if __name__ == "__main__":
    logout("start...")

    logout(str(DEBUG)+str(JSONPATH)+str(COUNTINI)+str(count)+str(read_line))

    app = RUN()
    app.run()
    
    exit()