import socket
import threading
import tkinter as tk
from PIL import ImageTk, Image

import client
from menu_parts import utils
import server


class My_Game:
    def __init__(self, root, view_component, model, nick, ip_address = None):
        self.nick = nick
        self.model = model
        self.root = root
        self.players_count = 1
        self.client_or_server = None
        self.client_or_server_thread = None
        self.lobby_window = None
        self.players_count_label = None
        self.view_component = view_component
        self.ip_address = ip_address

    def lobby(self, lobby_type):
        def swap_button_status():
            self.client_or_server.start_button = True

            #self.client_or_server_thread.interrupt()
            self.lobby_window.destroy()
            self.client_or_server = None

        def copy_ip():
            self.lobby_window.clipboard_clear()
            self.lobby_window.clipboard_append(ip)
            self.lobby_window.update()


        if lobby_type == "server":
            self.lobby_window = tk.Toplevel(self.root)
            self.lobby_window.title("Lobby")
            self.lobby_window.geometry("400x300")
            self.lobby_window.resizable(False, False)
            self.lobby_window.configure(bg="#6B3E86")
            utils.center_window(self.root, self.lobby_window, 400, 300)
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            self.client_or_server = server.Server(ip, self, self.view_component, self.model)
            ip_frame = tk.Frame(self.lobby_window, bg="#6B3E86")
            ip_frame.pack(pady=5)
            tk.Label(ip_frame, text=f"Twoje ip: {ip}", font=("Impact", 14), bg="#6B3E86").pack(
                side="left", padx=5)

            copy_icon_image = Image.open("./graphics/copy_icon.jpg")
            copy_icon_image = copy_icon_image.resize((20, 20))
            copy_icon = ImageTk.PhotoImage(copy_icon_image)

            copy_button = tk.Button(ip_frame, image=copy_icon, command=copy_ip, bg="#7653A0",
                                    activebackground='#6B3E86',
                                    relief='flat')
            copy_button.image = copy_icon
            copy_button.pack(side="left", padx=5)

            self.players_count_label = tk.Label(self.lobby_window, text=f"Liczba graczy: {self.players_count}",font=("Impact", 14), bg="#6B3E86")

            self.players_count_label.pack(pady=5)

            tk.Button(self.lobby_window, text="Start", command=swap_button_status, bg="#7653A0", fg="white",
                      activebackground='#6B3E86',
                      width=10, font=("Palatino", 10)).pack()
            self.client_or_server_thread = threading.Thread(target=self.client_or_server.loop_serve)
            self.client_or_server_thread.start()
        else:
            self.client_or_server = client.Client(self, self.view_component, self.model,self.ip_address)
            result = self.client_or_server.connect_to_server()
            if result:
                self.lobby_window = tk.Toplevel(self.root)
                self.lobby_window.title("Lobby")
                self.lobby_window.geometry("400x300")
                self.lobby_window.resizable(False, False)
                self.lobby_window.configure(bg="#6B3E86")
                utils.center_window(self.root, self.lobby_window, 400, 300)
                self.players_count_label = tk.Label(self.lobby_window, text=f"Liczba graczy: {self.players_count}", font=("Impact", 14), bg="#6B3E86")
                self.players_count_label.pack(pady=5)
                self.client_or_server_thread = threading.Thread(target=self.client_or_server.start_client)
                self.client_or_server_thread.start()
            else:
                self.client_or_server = None

