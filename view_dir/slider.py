import pygame

class Slider:
    def __init__(self):
        self.states = [1, 4, 5, 7, 9, 11, 13, 15, 17, 19,  21, 23, 25, 27, 29, 31, 33, 35, 37, 39]
        self.state_index = 1
        self.width = None
        self.height = 40
        self.handle_width = 5
        self.handle_pos = None

        self.repaint_flag = True

    def draw(self, screen, origin_x, origin_y):
        if self.repaint_flag:
            pygame.draw.rect(screen, (200, 200, 200), (origin_x, origin_y, self.width + self.handle_width, self.height))

            handle_x = origin_x + (self.width / (len(self.states) - 1)) * self.state_index
            self.handle_pos = (handle_x, origin_y)

            pygame.draw.rect(screen, (25, 25, 25), (self.handle_pos[0], self.handle_pos[1], self.handle_width, self.height))

    def resize(self, width):
        self.width = width
        self.repaint_flag = True

    def user_click(self, x):
        self.state_index = int(x / self.width * len(self.states))
        self.repaint_flag = True
        return self.states[self.state_index]
