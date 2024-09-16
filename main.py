import json
from tkinter import *

DEBUG = None
JSONPATH = ".\\tloos.json"
COUNTINI = ".\\count.ini"
count = None
read_line = 0

def logout(text):
    import time
    print(f"[{time.strftime('%H:%M:%S', time.localtime())}] {text}")

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
            return ["text", self.data["root"][self.read_root_line]]
    
    def read_button(self):
        if type(self.data["root"][self.read_root_line]) == dict and "buuton" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
    
    def read_input(self):
        if type(self.data["root"][self.read_root_line]) == dict and "input" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
        
    
    def read_run(self):
        if type(self.data["root"][self.read_root_line]) == dict and "run" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line] 
    
    


class WIN:
    def __init__(self) -> None:
        self.win = Tk()
        self.win.title("subtitle player")
        self.win.geometry("700x500")
        self.win.resizable(False, False)
        logout("init...ok")
        self.read = READ()
    
    def win_loop(self):
        self.win.mainloop()
        logout("loop...ok")
    
    def win_text(self):
        pass

if __name__ == "__main__":
    logout("start...")

    read = READ()
    read.read_count()
    logout(str(DEBUG)+str(JSONPATH)+str(COUNTINI)+str(count)+str(read_line))

    win = WIN()
    win.win_loop()


    logout("end...")
    exit()