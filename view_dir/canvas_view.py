import math

import pygame

class CanvasView:
    def __init__(self, model):
        self.model = model

        self.rect_side = 1
        self.canvas_width = self.rect_side * self.model.width
        self.canvas_height = self.rect_side * self.model.height

    def adjust_size(self, width, height):
        size_steps = [4, 3, 2, 1]
        self.rect_side = size_steps[-1]

        max_tile_size_width = width / self.model.width
        max_tile_size_height = height / self.model.height

        max_tile_size = min(max_tile_size_height, max_tile_size_width)

        for size in size_steps:
            if size <= max_tile_size:
                self.rect_side = size
                break
        self.canvas_width = self.rect_side * self.model.width
        self.canvas_height = self.rect_side * self.model.height

    def draw(self, screen, origin_x, origin_y):
        for color_index in self.model.repaint_dict:
            for tile_index in self.model.repaint_dict[color_index]:
                x = tile_index % self.model.width
                y = tile_index // self.model.width

                x = x * self.rect_side + origin_x
                y = y * self.rect_side + origin_y

                rect = pygame.Rect(x, y, self.rect_side, self.rect_side)

                color = self.model.color_list[color_index]
                pygame.draw.rect(screen, color, rect)
            self.model.repaint_dict[color_index] = []

    def resize(self, width, height):
        self.adjust_size(width, height)
        self.model.full_repaint()

    def request_full_repaint(self):
        self.model.full_repaint()

    def user_paint(self, x, y, brush_size, color_index):
        x //= self.rect_side
        y //= self.rect_side
        for x_offset in range(-brush_size, brush_size + 1):
            for y_offset in range(-brush_size, brush_size + 1):
                if x_offset ** 2 + y_offset ** 2 <= brush_size ** 2:
                    if 0 <= x + x_offset < self.model.width and 0 <= y + y_offset < self.model.height:
                        tile_index = (x + x_offset) + (y + y_offset) * self.model.width
                        if tile_index < len(self.model.array):
                            self.model.paint(tile_index, color_index)

    def points_in_line(x0, y0, x1, y1, brush_size):

        euclidean_distance = int(math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2))

        if brush_size > 1:
            quantity = math.ceil(euclidean_distance / brush_size)
        else:
            quantity = euclidean_distance ** 2

        points = []

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        interval = euclidean_distance // quantity

        count = -1

        while True:
            count += 1
            if count == interval:
                count = -1
                points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points



    def clear(self):
        self.model.reset()
