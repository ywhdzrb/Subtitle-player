import json
from tkinter import *
from tkinter import messagebox

DEBUG = None
JSONPATH = ".\\tloos.json"
COUNTINI = ".\\count.ini"
json_count = None
read_line = 0

def logout(text) -> None:
    if DEBUG:
        import time
        print(f"[{time.strftime('%H:%M:%S', time.localtime())}] {text}")
        with open(".\\log.log", "a") as f:
            f.write(f"[{time.strftime('%H:%M:%S', time.localtime())}] {text}\n")

def exit() -> None:
    import sys
    with open(COUNTINI, "w", encoding="UTF-8") as f:
        f.write(str(DEBUG)+"\n")
        f.write(str(JSONPATH)+"\n")
        f.write(str(COUNTINI)+"\n")
        f.write(str(json_count)+"\n")
        f.write(str(read_line)+"\n")
    sys.exit()       

class READ:
    def __init__(self) -> None:
        self.read_root_line = read_line
        with open(JSONPATH, "r", encoding="UTF-8") as f:
            self.data = json.load(f)
            self.read_json_count_and_DEBUG()
            self.read_count()
            logout("read json ok")
            logout(self.data)
    
    def read_count(self) -> None:
        global DEBUG, JSONPATH, COUNTINI, json_count, read_line
        with open(COUNTINI, "r", encoding="UTF-8") as f:
            DEBUG = bool(f.readline())
            JSONPATH = str(f.readline())
            COUNTINI = str(f.readline())
            json_count = dict(f.readline())
            read_line = int(f.readline())
            logout("count...ok")
    
    def read_json_count_and_DEBUG(self) -> None:
        json_count = self.data["count"]
        with open(COUNTINI, "r", encoding="UTF-8") as f:
            JSONPATH = f.readline()
            COUNTINI = f.readline()
            read_line = f.readline()
        
        with open(JSONPATH, "r", encoding="UTF-8") as f:
            json_count = json.load(f)["count"]
            logout(json_count)
            DEBUG = json_count["DEBUG"]

        with open(COUNTINI, "w") as f:
            f.write(str(DEBUG)+"\n")
            f.write(str(JSONPATH)+"\n")
            f.write(str(COUNTINI)+"\n")
            f.write(str(json_count)+"\n")
            f.write(str(read_line)+"\n")
        logout(json_count, DEBUG)
    
    def read_text(self) -> str:
        if type(self.data["root"][self.read_root_line]) == str:
            return self.data["root"][self.read_root_line]
    
    def read_button(self) -> dict:
        if type(self.data["root"][self.read_root_line]) == dict and "buuton" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
    
    def read_input(self) -> dict:
        if type(self.data["root"][self.read_root_line]) == dict and "input" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]

    def read_run(self) -> dict:
        if type(self.data["root"][self.read_root_line]) == dict and "run" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
    
    def read_json_count(self) -> dict:
        if type(self.data["root"][self.read_root_line]) == dict and "count" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
    
    def read_bigtext(self) -> dict:
        if type(self.data["root"][self.read_root_line]) == dict and "bigtext" in self.data["root"][self.read_root_line]:
            return self.data["root"][self.read_root_line]
        
class RUN_READ:
    def __init__(self) -> None:
        self.read = READ()
        self.win = WIN()
    
    def run_text(self) -> None:
        self.win.win_text(self.read.read_text().split(":"))

class WIN:
    def __init__(self) -> None:
        self.win = Tk()
        self.win.title("subtitle player")
        self.win.geometry("350x200")
        self.win.resizable(False, False)
        
        self.button_up = Button(self.win, text="Up", command=lambda: self.win_button_up())
        self.button_up.place(x=310, y=10)

        self.button_down = Button(self.win, text="Down", command=lambda: self.win_button_down())
        self.button_down.place(x=250, y=10)

        self.button_home = Button(self.win, text="home", command= lambda: self.win_button_home())
        self.button_home.place(x=10, y=10)

        self.read = READ()

        logout("init...ok")
    
    def win_button_up(self) -> None:
        global read_line
        logout("Up")
        if not read_line == 0:
            read_line -= 1
            logout(read_line)
        else:
            messagebox.showinfo("提示", "已经是第一行了！")
            logout("not UP")
    
    def win_button_down(self) -> None:
        global read_line
        logout("Down")
        if not read_line == len(self.read.data["root"])-1:
            read_line += 1
            logout(read_line)
        else:
            messagebox.showinfo("提示", "已经是最后一行了！")
            logout("not Down")
    
    def win_button_home(self) -> None:
        logout("start home")
        home = Tk()
        home.title("subtitle player home")
        home.geometry("300x100")
        home.resizable(False, False)

        Label(home, text="json path").grid(row=0, column=0)

        json_path = Entry(home)
        json_path.insert(0, JSONPATH)
        json_path.grid(row=0, column=1)

        button_reboot = Button(home, text="reboot", command=lambda: self.win_button_reboot(json_path.get(), home))
        button_reboot.grid(row=0, column=2)

        button_exit = Button(home, text="exit", command=lambda: exit())
        button_exit.grid(row=1, column=0)

        home.mainloop()

    def win_button_reboot(self, json_path, home) -> None:
        logout("reboot...ok")
        home.destroy()
        self.win.destroy()
        global JSONPATH, read_line
        if not json_path == JSONPATH:
            read_line = 0
        JSONPATH = json_path
        with open(COUNTINI, "w", encoding="UTF-8") as f:
            f.write(str(DEBUG)+"\n")
            f.write(str(JSONPATH)+"\n")
            f.write(str(COUNTINI)+"\n")
            f.write(str(json_count)+"\n")
            f.write(str(read_line)+"\n")
        RUN().run()

    def win_loop(self) -> None:
        logout("loop...ok")
        self.win.mainloop()
        exit()
    
    def win_text(self, text:list) -> None:
        text_label = Label(self.win)
        text_label.config(text=text[0])
        text_label.place(x=10, y=50)
        name_label = Label(self.win)
        name_label.config(text=text[1]+":")
        name_label.place(x=10, y=70)
        logout(text)

    def win_run(self, run) -> None:
        if run in "count":
            pass
    
    def win_button(self, button) -> None:
        self.button_down.destroy()
        self.button_up.destroy()
        self.button_home.destroy()
        if button["num"] == 1:
            logout("button1")
            button1 = Button(self.win, text=button["text"][0], command=lambda:self.win_run(button["run"]))
            button1.pack(fill=X)
        if button["num"] == 2:
            logout("button2")
            button1 = Button(self.win, text=button["text"][0], command=lambda:self.win_run(button["run"]))
            button1.pack(fill=X)
            button2 = Button(self.win, text=button["text"][1], command=lambda:self.win_run(button["run"]))
            button2.pack(fill=X)

class RUN():
    def __init__(self) -> None:
        self.read = READ()
        self.win = WIN()
    
    def run(self) -> None:
        self.win.win_loop()


if __name__ == "__main__":
    logout("start...")

    logout(str(DEBUG)+str(JSONPATH)+str(COUNTINI)+str(json_count)+str(read_line))

    app = RUN()
    app.run()
    
    exit()