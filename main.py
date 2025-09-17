from threading import Thread
import time
import screeninfo
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk, ImageSequence
from pynput.mouse import Controller
import json

class GUI:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Amusement Linkage Live System")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.configure(background='white')
        self.root.bind('<Escape>', lambda _: self.root.destroy())

        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.screen_info = screeninfo.get_monitors()
        for i, s in enumerate(self.screen_info):
            if i == self.config['screen']:
                self.root.geometry("{}x{}+{}+{}".format(s.width, s.height, s.x, s.y))
                mouse = Controller()
                mouse.position = (s.width, s.height)
                del mouse
                self.root.state('zoomed')
                break

        self.frame = Frame(self.root)
        self.frame.pack(expand=YES)

        Style().configure("TFrame", background='white')

        self.container = Frame(self.frame)
        if self.screen_info[self.config['screen']].height > self.screen_info[self.config['screen']].width:
            upper_border = 320
        else:
            upper_border = 20
        self.container.grid(sticky="WE", pady=(upper_border,0))

        self.logo = PhotoImage(file="assets/logo.png")
        self.logo_label = Label(self.container, image=self.logo, background='white', padding=10)
        self.logo_label.grid(row=0, pady=40, sticky="S")

        self.font_set = ("Yu Gothic", 28, "bold")

        self.model = Label(self.container, text=self.config['model'], font=self.font_set, background='white')
        self.model.grid(row=1)

        self.step = Label(self.container, text="STEP", font=self.font_set, background='white')
        self.step.grid(row=2, pady=30)

        self.description_frame = Frame(self.container)
        self.description_frame.grid(row=3)

        load_pic = Image.open(f"assets/logomode_load.gif")
        self.loading_frames = [ImageTk.PhotoImage(frame.resize((45, 45))) for frame in ImageSequence.Iterator(load_pic)]

        self.description_load = Label(self.description_frame, background='white', image=self.loading_frames[0])
        self.description_load.grid(row=0, column=0, sticky="W")

        self.step_description = Label(self.description_frame, text="", font=self.font_set, anchor="nw", background='white')
        self.step_description.grid(row=0,column=1, sticky="W", padx=10)

        Thread(target=self.play_gif, args=(0,), daemon=True).start()

        Thread(target=self.step_sequence, args=(self.config['steps'],), daemon=True).start()
    
    def play_gif(self, index):
        while True:
            self.description_load['image'] = self.loading_frames[index]
            index = (index + 1) % len(self.loading_frames)
            time.sleep(0.04)
    
    def step_sequence(self, steps: dict):
        for step in steps:
            self.set_step(step)
            time.sleep(self.config['steps'][step]['duration'])
        self.root.quit()
    
    def set_step(self, step: str):
        self.step['text'] = f"STEP {step}"
        self.step_description['text'] = self.config['steps'][step]['description']
        if self.config['steps'][step]['action'] != "":
            exec(self.config['steps'][step]['action'])

if __name__ == "__main__":
    program = GUI(Tk())

    program.root.mainloop()
