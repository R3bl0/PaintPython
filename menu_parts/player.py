import tkinter as tk
from tkinter import messagebox
from menu_parts import utils
from my_game import My_Game

global player_nick

def player_case(select_window, root, view_component, model):
    def handle_input():
        ip_server = user_input_ip.get()
        global player_nick
        player_nick = user_input_nick.get()

        if ip_server == "error":
            messagebox.showerror("Error", "Błędne ip")
            return
        if player_nick == "":
            messagebox.showerror("Error", "Podaj nick")
            return

        ip_window.destroy()
        My_Game(root, view_component, model, player_nick, ip_server).lobby("player")

    select_window.destroy()
    ip_window = tk.Toplevel(root)
    ip_window.geometry("300x150")
    ip_window.configure(bg="#6B3E86")
    utils.center_window(root, ip_window, 300, 150)

    tk.Label(ip_window, text="Podaj ip:", font=("Impact", 14), bg="#6B3E86").pack()
    user_input_ip = tk.Entry(ip_window, width=30)
    user_input_ip.pack()

    tk.Label(ip_window, text="Podaj nick:", font=("Impact", 14), bg="#6B3E86").pack()
    user_input_nick = tk.Entry(ip_window, width=30)
    user_input_nick.pack()

    ok_button = tk.Button(ip_window, text="Ok", command=handle_input, font=("Palatino", 10), bg="#7653A0",
                          fg="white", activebackground='#6B3E86', width=4)
    ok_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
