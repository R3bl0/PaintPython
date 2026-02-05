import socket
import threading
import time

import select

from view_dir import model as view_dir_model
import game_timers_constants as constants

import game_timers_constants


class Client:
    def __init__(self, my_game, view_component, model, ip_address):
        self.view_component = view_component
        self.model = model
        self.my_game = my_game
        self.painting_size = view_dir_model.CANVAS_WIDTH * view_dir_model.CANVAS_HEIGHT

        self.port = 6969
        self.ip_address = ip_address
        self.players = None
        self.socket = None

    def connect_to_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.ip_address, self.port))
            self.socket = s
        except socket.error:
            return False
        return True

    def start_client(self):
        data = None
        while data != 'game_start':
            data = self.socket.recv(1024).decode('utf-8')
            if data != 'game_start':
                self.my_game.player_count = int(data)
                self.my_game.players_count_label.config(text=f'Liczba graczy: {self.my_game.player_count}')

        rounds = int(self.socket.recv(1).decode('utf-8'))
        theme = self.socket.recv(1024).decode('utf-8')  #ponoć to się blokuje aż przyjdzie coś
        rating_view_time = constants.RATING_RESULT_VIEW_TIME

        round = 0

        self.view_component.start_game()
        time.sleep(1)
        while round < rounds:

            self.view_component.notify_of_draw_phase(theme, game_timers_constants.TIME_TO_DRAW)

            time.sleep(10)
            self.send_to_server(b'(painting)' + self.model.array)


            time.sleep(2)
            #===================================
            paintings_count = int.from_bytes(self.socket.recv(2))

            for i in range(paintings_count):
                painting_number = self.socket.recv(10)
                time.sleep(1)
                painting = self.socket.recv(self.painting_size)
                print(painting)
                self.model.set_bytearray(painting)
                self.view_component.notify_of_vote_phase(rating_view_time)

                time.sleep(rating_view_time)

                rating = self.view_component.get_rating()
                rating_to_send = bytearray()
                rating_to_send.extend(painting_number)
                rating_to_send.extend(b'(rating)')
                rating_to_send.extend(rating)
                self.send_to_server(rating_to_send)

            round += 1

    def send_to_server(self, data):
        self.socket.setblocking(False)
        data_len = len(data)
        total_sent = 0
        while total_sent < data_len:
            try:
                sent = self.socket.send(data)
                total_sent += sent
                data = data[sent:]
            except socket.error:
                select.select([], [self.socket], [])
        self.socket.setblocking(True)

