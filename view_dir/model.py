# 256 różnych kolorów możliwych na płótnie ( zakres 0-255)
# płótno rozmiar w sumie dowolny
import pygame


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 225

COLORS = [
    pygame.Color(255, 255, 255),  # White
    pygame.Color(0, 0, 0),        # Black
    pygame.Color(255, 0, 0),      # Red
    pygame.Color(0, 255, 0),      # Green
    pygame.Color(0, 0, 255),      # Blue
    pygame.Color(100, 100, 100),  # Gray
    pygame.Color(255, 255, 0),    # Yellow
    pygame.Color(139, 69, 19),    # Brown
    pygame.Color(255, 165, 0),    # Orange
    pygame.Color(128, 0, 128),    # Purple
    pygame.Color(173, 216, 230),  # Light Blue
    pygame.Color(255, 192, 203),  # Pink
    pygame.Color(139, 0, 0),      # Dark Red
    pygame.Color(0, 100, 0),      # Dark Green
    pygame.Color(0, 0, 139),      # Dark Blue
    pygame.Color(144, 238, 144),  # Light Green
    pygame.Color(255, 255, 224),  # Light Yellow
    pygame.Color(211, 211, 211),  # Light Gray
    pygame.Color(169, 169, 169),  # Dark Gray
    pygame.Color(0, 255, 255),    # Cyan
    pygame.Color(255, 0, 255),    # Magenta
    pygame.Color(128, 128, 0),    # Olive
    pygame.Color(0, 128, 128),    # Teal
    pygame.Color(0, 0, 128),      # Navy
    pygame.Color(128, 0, 0),      # Maroon
    pygame.Color(0, 255, 0),      # Lime
    pygame.Color(255, 127, 80),   # Coral
    pygame.Color(0, 255, 255),    # Aqua
    pygame.Color(75, 0, 130),     # Indigo
    pygame.Color(255, 215, 0),    # Gold
    pygame.Color(192, 192, 192),  # Silver
    pygame.Color(255, 218, 185),  # Peach
    pygame.Color(230, 230, 250),  # Lavender
    pygame.Color(245, 245, 220),  # Beige
    pygame.Color(189, 252, 201)   # Mint
]

class CanvasModel:
    def __init__(self):
        self.width = CANVAS_WIDTH
        self.height = CANVAS_HEIGHT
        self.array = bytearray(CANVAS_WIDTH * CANVAS_HEIGHT)
        self.color_list = COLORS
        self.repaint_dict = {0: list(range(len(self.array)))}
        for i in range(1, len(COLORS)):
            self.repaint_dict[i] = []

        self.client_socket = None

        self.drawing_enabled = True

    def reset(self):
        for i in range(len(self.array)):
            self.array[i] = 0

    def full_repaint(self):
        for i in range(len(self.array)):
            self.repaint_dict[self.array[i]].append(i)

    def paint(self, index, color_index):
        if self.array[index] != color_index:
            self.array[index] = color_index
            self.repaint_dict[color_index].append(index)

    def set_bytearray(self, new_bytearray):
        self.array = new_bytearray
        self.full_repaint()
