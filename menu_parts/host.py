import tkinter as tk
from tkinter import messagebox
from menu_parts import utils
from my_game import My_Game

global host_nick
def host_case(select_window, root, view_component, model):
    def handle_input():
        global host_nick
        host_nick = user_input_nick.get()

        if host_nick == "":
            messagebox.showerror("Error", "Podaj nick")
            return

        nick_window.destroy()
        My_Game(root, view_component, model, host_nick).lobby("server")

    select_window.destroy()
    nick_window = tk.Toplevel(root)
    nick_window.geometry("300x150")
    nick_window.configure(bg="#6B3E86")
    utils.center_window(root, nick_window, 300, 100)

    tk.Label(nick_window, text="Podaj nick:", font=("Impact", 14), bg="#6B3E86").pack()
    user_input_nick = tk.Entry(nick_window, width=30)
    user_input_nick.pack()

    ok_button = tk.Button(nick_window, text="Ok", command=handle_input, font=("Palatino", 10), bg="#7653A0",
                          fg="white", activebackground='#6B3E86', width=4)
    ok_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
