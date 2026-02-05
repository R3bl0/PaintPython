import tkinter as tk
from PIL import ImageTk, Image

from menu_parts import handlers as hand


class Menu:
    def __init__(self, view_component, model):
        self.root = None
        self.view_component = view_component
        self.model = model

    def start_menu(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        bg = Image.open('./graphics/background.jpg')
        bg = bg.resize((600, 400), Image.Resampling.LANCZOS)
        bg = ImageTk.PhotoImage(bg)

        canvas = tk.Canvas(self.root, width=600, height=400)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg, anchor="nw")

        canvas.create_text(300, 50, text="RYSOWANKO", font=("Impact", 30, "bold"))
        start_button = tk.Button(self.root, text="Start",
                                 command=lambda: hand.start_button_click(self.root, self.view_component, self.model), width=20,
                                 height=2,
                                 font=("Palatino", 12, "bold"), bg="#7BA6EA", fg="white", activebackground="#215CC0")
        ranking_button = tk.Button(self.root, text="Ranking", command=lambda: hand.ranking_button_click(self.root),
                                   width=20, height=2,
                                   font=("Palatino", 12, "bold"), bg="#7BA6EA", fg="white", activebackground="#215CC0")
        exit_button = tk.Button(self.root, text="Exit", command = hand.exit_button_click, width=20, height=2,
                                font=("Palatino", 12, "bold"), bg="#7BA6EA", fg="white", activebackground="#215CC0")

        start_button.place(relx=0.5, rely=0.35, anchor='center')
        ranking_button.place(relx=0.5, rely=0.5, anchor='center')
        exit_button.place(relx=0.5, rely=0.65, anchor='center')

        self.root.mainloop()

    def end_menu(self):
        print(
            f'Rozjebałeś się kurwo jak najgorsza chujoza\nNa Twym gardle obroża niech Cię skarci dłoń Boża\nJednak zanim to zrobi ostrza ludzi poznasz\nKiedy na ulicy ciężkiego urazu doznasz\n')
        self.root.destroy()
        self.view_component.close()
