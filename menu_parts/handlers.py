import sys
import tkinter as tk

from database import get_players
from menu_parts import utils
from menu_parts import host
from menu_parts import player


def start_button_click(root, view_component, model):
    select_window = tk.Toplevel(root)
    select_window.geometry("300x100")
    select_window.resizable(False, False)
    select_window.configure(bg="#6B3E86")
    utils.center_window(root, select_window, 300, 100)
    tk.Label(select_window, text="WHO ARE YOU?", font=("Impact", 14), bg="#6B3E86").pack(pady=5)

    tk.Button(select_window, text="Host", command=lambda: host.host_case(select_window, root, view_component, model), width=10,
              font=("Palatino", 10), bg="#7653A0", fg="white",
              activebackground='#6B3E86').pack()
    tk.Button(select_window, text="Player", command=lambda: player.player_case(select_window, root, view_component, model), width=10,
              font=("Palatino", 10), bg="#7653A0",
              fg="white", activebackground='#6B3E86').pack()


def ranking_button_click(root):
    ranking_window = tk.Toplevel(root)
    ranking_window.geometry("300x400")
    ranking_window.resizable(False, False)
    ranking_window.configure(bg="#6B3E86")
    utils.center_window(root, ranking_window, 300, 400)

    tk.Label(ranking_window, text="RANKING", font=("Impact", 20), pady=10, bg="#6B3E86", fg="black").pack()

    frame = tk.Frame(ranking_window, bg="#6B3E86")
    frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame, bg="#6B3E86")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    inner_frame = tk.Frame(canvas, bg="#6B3E86")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    players = get_players()

    (tk.Label(inner_frame, text="Nick", font=("Arial", 10, "bold"), bg="#6B3E86", fg="black")
     .grid(row=0, column=0, padx=50, pady=5, sticky="nsew"))
    (tk.Label(inner_frame, text="Score", font=("Arial", 10, "bold"), bg="#6B3E86", fg="black")
     .grid(row=0, column=1, padx=50, pady=5, sticky="nsew"))

    for row_num, (nick, score) in enumerate(players, start=1):
        (tk.Label(inner_frame, text=nick, font=("Arial", 10), bg="#6B3E86", fg="black")
         .grid(row=row_num, column=0, padx=50, pady=5, sticky="nsew"))
        (tk.Label(inner_frame, text=score, font=("Arial", 10), bg="#6B3E86", fg="black")
         .grid(row=row_num, column=1, padx=50, pady=5, sticky="nsew"))

    for col_num in range(2):
        inner_frame.grid_columnconfigure(col_num, weight=1)

    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def exit_button_click():
    sys.exit()
