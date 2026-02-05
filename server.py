import socket
import selectors
import threading
import time

import database
import game_timers_constants as constants
from view_dir import model as view_dir_model


class Server:
    def __init__(self, host, mygame, view_component, model):
        self.view_component = view_component
        self.model = model
        self.painting_size = view_dir_model.CANVAS_WIDTH * view_dir_model.CANVAS_HEIGHT

        self.mygame = mygame
        self.listen_thread = None
        self.start_button = False
        self.clients = {}
        self.host = host
        self.port = 6969
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, self.port))
        self.socket.listen(2)
        self.socket.setblocking(False)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.socket, selectors.EVENT_READ, self.accept)
        self.selector_thread = threading.Thread(target=self.selector_work)
        self.all_paintings = {}
        self.all_points = {}
        self.lock = threading.Lock()
        self.id = self.socket.fileno()

    def accept(self, sock, mask):
        conn, addr = self.socket.accept()
        conn.setblocking(False)
        self.clients[conn] = addr
        self.selector.register(conn, selectors.EVENT_READ, self.read)
        self.mygame.player_count = len(self.clients) + 1
        self.mygame.players_count_label.config(text=f'Liczba graczy: {self.mygame.player_count}')
        clients_len = str(int(len(self.clients) + 1))
        for all_conn in self.clients.keys():
            all_conn.send(clients_len.encode('UTF-8'))

    def read(self, conn, mask):
        try:
            data = conn.recv(self.painting_size + 1000)
            if data:
                if b'(painting)' in data:
                    while len(data) < 90000:
                        data += conn.recv(self.painting_size + 1000)
                    new_data = data.split(b'(painting)')
                    with self.lock:
                        self.all_paintings[conn.fileno()] = new_data[1]
                elif b'(rating)' in data:
                    new_data = data.split(b'(rating)')
                    with self.lock:
                        previous_point = self.all_points[int(new_data[0])]
                        self.all_points[int(new_data[0])] = int(new_data[1]) + previous_point
            else:
                self.close_client_connection(conn)
        except ConnectionResetError:
            self.close_client_connection(conn)

    def close_client_connection(self, conn):
        print('Connection closed')
        del self.clients[conn]
        self.selector.unregister(conn)
        conn.close()
        self.mygame.player_count = len(self.clients) + 1
        self.mygame.players_count_label.config(text=f'Liczba graczy: {self.mygame.player_count}')
        clients_len = str(int(len(self.clients) + 1))
        for all_conn in self.clients.keys():
            all_conn.send(clients_len.encode('UTF-8'))

    def selector_work(self):
        while True:
            select = self.selector.select(timeout=0.2)

            for key, mask in select:
                handler = key.data
                handler(key.fileobj, mask)

    def loop_serve(self):
        self.selector_thread.start()
        while not self.start_button:
            pass
            time.sleep(1)

        message = 'game_start'
        for conn in self.clients.keys():
            conn.send(message.encode('UTF-8'))

        rounds_message = str(int(constants.ROUND_AMOUNT))
        for conn in self.clients.keys():
            conn.send(rounds_message.encode('UTF-8'))

        # losuj temat do narysowania
        theme = database.random_topic()
        # roześlij temat po socketach
        for conn in self.clients.keys():
            conn.send(theme.encode('utf-8'))

        for conn in self.clients.keys():
            self.all_paintings[conn.fileno()] = None

        self.all_paintings[self.id] = None

        for conn in self.clients.keys():
            self.all_points[conn.fileno()] = 0

        self.all_points[self.id] = 0

        time.sleep(1)
        round = 0
        self.view_component.start_game()
        while round < constants.ROUND_AMOUNT:

            self.view_component.notify_of_draw_phase(theme, constants.TIME_TO_DRAW)

            time.sleep(constants.TIME_TO_DRAW)
            bytearray_model = self.model.array
            self.all_paintings[self.id] = bytearray_model

            time.sleep(2)
            # ======================================
            with self.lock:
                for conn in self.clients.keys():
                    conn.send(int.to_bytes(len(self.all_paintings),3,byteorder='big'))

            with self.lock:
                for conn_file_no in self.all_paintings.keys():
                    for conn in self.clients.keys():
                        conn.send(int.to_bytes(conn_file_no,3,byteorder='big'))
                time.sleep(1)
                with self.lock:
                    for conn in self.clients.keys():
                        conn.send(self.all_paintings[conn_file_no])

                self.model.set_bytearray(self.all_paintings[conn_file_no])
                self.view_component.notify_of_vote_phase(constants.RATING_RESULT_VIEW_TIME)

                time.sleep(constants.RATING_RESULT_VIEW_TIME)

                rating = self.view_component.get_rating()
                with self.lock:
                    previous_point = self.all_points[conn_file_no]
                    self.all_points[conn_file_no] = rating + previous_point

            # =========================================
            # self.view_component.notify_of_vote_results(rating, constants.RATING_RESULT_VIEW_TIME)
            #
            # time.sleep(constants.RATING_RESULT_VIEW_TIME)

            #================================
            self.model.reset()
            round += 1

        self.socket.shutdown(socket.SHUT_RDWR)

    def start_game(self):
        print(f'Server clients: {self.clients}')
