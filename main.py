import json
from tkinter import *
from tkinter import messagebox

DEBUG = None
JSONPATH = ".\\tloos.json"
json_count = None
read_line = 0

def logout(text) -> None:
    if DEBUG:
        import time
        print(f"[{time.strftime('%H:%M:%S', time.localtime())}] {text}")
        with open(".\\log.log", "a", encoding="UTF-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S', time.localtime())}] {text}\n")

def exit() -> None:
    import sys
    logout("exit")
    sys.exit()       

class READ:
    def __init__(self) -> None:
        self.read_root_line = read_line
        with open(JSONPATH, "r", encoding="UTF-8") as f:
            self.data = json.load(f)
            self.read_DEBUG()
            self.read_json_count()
            logout("read json ok")
            logout(self.data)
    
    def read_DEBUG(self) -> None:
        global DEBUG
        DEBUG = self.data["DEBUG"]
    
    def read_json_count(self) -> dict:
        return self.data["count"]

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

        # 显示 read_line
        global read_line
        self.win_text_read_line = Label(self.win)
        self.win_text_read_line.config(text=f"line : {read_line + 1}")
        self.win_text_read_line.place(x=180, y=15)
 
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
        self.win_text_read_line.config(text=f"line : {read_line + 1}")
    
    def win_button_down(self) -> None:
        global read_line
        logout("Down")
        if not read_line == len(self.read.data["root"])-1:
            read_line += 1
            logout(read_line)
        else:
            messagebox.showinfo("提示", "已经是最后一行了！")
            logout("not Down")
        self.win_text_read_line.config(text=f"line : {read_line + 1}")

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
        RUN().run()

    def win_loop(self) -> None:
        logout("loop...ok")
        self.win.mainloop()
        exit()
    
    def win_text(self, text:list) -> None:
        text_label = Label(self.win)
        text_label.config(text=text[1])
        text_label.place(x=10, y=50)
        name_label = Label(self.win)
        if text[0] in json_count:
            name_label.config(text=json_count[text[0]])
        else:
            name_label.config(text=text[0])
        name_label.place(x=10, y=70)
        logout(text)

    def win_run(self, run:dict) -> None:
        if "count" in run:
            for i, value in run["count"]:
                logout(value)
                if i in json_count:
                    json_count[i] = run["count"][i]
                    logout(f"count {i} = {run['count'][i]}")
                if value == "input":
                    json_count[i] = self.my_input
                    logout(f"count:{json_count[i]} = {self.my_input}")
        
        if "run" in run:
            self.win_run(run["run"])
        
        if "text" in run:
            self.win_text(run["text"].split(":"))

    def win_button_click(self, button:dict) -> None:
        if "run" in button:
            self.win_run(button["run"])
        self.my_button1.destroy()
        self.my_button2.destroy()
        self.my_button3.destroy()

    def win_button(self, button:dict) -> None:
        self.my_button1 = Button(self.win, text=button["text"][0], command=lambda: self.win_button_click(button))
        self.my_button2 = Button(self.win, text=button["text"][1], command=lambda: self.win_button_click(button))
        self.my_button3 = Button(self.win, text=button["text"][2], command=lambda: self.win_button_click(button))
        if button["num"] == 1:
            self.my_button1.pack(fill="x")
        if button["num"] == 2:
            self.my_button1.pack(fill="x")
            self.my_button2.pack(fill="x")
        if button["num"] == 3:
            self.my_button1.pack(fill="x")
            self.my_button2.pack(fill="x")
            self.my_button3.pack(fill="x")

    def win_input_click(self, input:Entry) -> None:
        logout(input.get())
        if "run" in input:
            self.win_run(input["run"])

    def win_input(self, input:dict) -> None:
        Label(self.win, text=input["text"]).pack(fill="x")
        self.my_input = Entry(self.win)
        self.my_input.pack(fill="x")
        self.my_button = Button(self.win, text="ok", command=lambda: self.win_input_click(input))
        

class RUN():
    def __init__(self) -> None:
        self.win = WIN()
    
    def run(self) -> None:
        self.win.win_loop()


if __name__ == "__main__":
    logout("start...")

    logout(str(DEBUG)+str(JSONPATH)+str(json_count)+str(read_line))

    app = RUN()
    app.run()
    
    exit()