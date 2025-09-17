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

        self.root.configure(background=self.config['background'])
        Style().configure("TFrame", background=self.config['background'])
        Style().configure("TLabel", background=self.config['background'])
        Style().configure("TLabel", foreground=self.config['font_color'])

        self.container = Frame(self.frame)
        if self.screen_info[self.config['screen']].height > self.screen_info[self.config['screen']].width:
            upper_border = 300
        else:
            upper_border = 0
        self.container.grid(sticky="WE", pady=(upper_border,0))

        self.logo = PhotoImage(file="assets/logo.png")
        self.logo_label = Label(self.container, image=self.logo)
        self.logo_label.grid(row=0, pady=40, sticky="S")

        self.font_set = ("Yu Gothic", 28, "bold")

        self.model = Label(self.container, text=self.config['model'], font=self.font_set)
        self.model.grid(row=1)

        self.step = Label(self.container, text="STEP", font=self.font_set, width=50, anchor='center')
        self.step.grid(row=2, pady=5)

        self.description_frame = Frame(self.container)
        self.description_frame.grid(row=3)

        load_pic = Image.open(f"assets/logomode_load.gif")
        self.loading_frames = [ImageTk.PhotoImage(frame.resize((45, 45))) for frame in ImageSequence.Iterator(load_pic)]

        self.description_load = Label(self.description_frame)
        self.description_load.grid(row=0, column=0, sticky="W")

        self.step_description = Label(self.description_frame, text="", font=self.font_set, anchor="nw")
        self.step_description.grid(row=0,column=1, sticky="W")

        self.error_occurred = False

        Thread(target=self.play_gif, args=(0,), daemon=True).start()

        Thread(target=self.step_sequence, args=(self.config['steps'],), daemon=True).start()
    
    def play_gif(self, index):
        while not self.error_occurred:
            self.description_load['image'] = self.loading_frames[index]
            index = (index + 1) % len(self.loading_frames)
            time.sleep(0.04)
        else:
            self.description_load['image'] = PhotoImage()
    
    def step_sequence(self, steps: dict):
        for step in steps:
            self.set_step(step)
            if self.error_occurred:
                return
            time.sleep(self.config['steps'][step]['duration'])
        self.root.quit()
    
    def set_step(self, step: str):
        self.step['text'] = f"STEP {step}"
        self.step_description['text'] = self.config['steps'][step]['description']
        if self.config['steps'][step]['action'] != "":
            try:
                exec(f"error = self.error\n"+self.config['steps'][step]['action'])
            except Exception:
                self.error('0')

    def error(self, code: str):
        self.error_occurred = True
        self.description_load['image'] = None
        self.step['text'] = f'ERROR {code}'
        self.step_description['text'] = self.config['errors'][code]
        Thread(target=self.text_color_change, daemon=True).start()

    def text_color_change(self):
        depth = 0
        increment = True
        while True:
            if increment:
                depth += 1 if depth < 8 else 0
            else:
                depth -= 1 if depth != 0 else 0
            if depth == 8:
                increment = False
            elif depth == 0:
                increment = True
            self.step['foreground'] = self.step_description['foreground'] = f'#F{depth:x}0'
            time.sleep(0.12)

if __name__ == "__main__":
    program = GUI(Tk())
    program.root.mainloop()
