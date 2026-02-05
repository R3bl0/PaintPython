import pygame

class PaletteView:
    def __init__(self, model):
        self.model = model

        self.gap = None
        self.rect_side = None
        self.height = None
        self.rects = []

        self.repaint_flag = True


    def draw(self, screen, origin_x, origin_y):
        if self.repaint_flag:
            self.rects = []
            x = self.gap + origin_x
            y = self.gap + origin_y
            for color in self.model.color_list:
                offset = self.rect_side//10
                rect = pygame.Rect(x - 2*offset, y - 2*offset, self.rect_side + 4*offset, self.rect_side + 4*offset)
                pygame.draw.rect(screen, pygame.Color(75, 75, 75), rect)

                rect = pygame.Rect(x - offset, y - offset, self.rect_side + int(2.5*offset), self.rect_side + int(2.5*offset))
                pygame.draw.rect(screen, pygame.Color(0, 0, 0), rect)

                rect = pygame.Rect(x, y, self.rect_side, self.rect_side)
                pygame.draw.rect(screen, color, rect)
                self.rects.append(rect)
                x += self.rect_side + self.gap
            self.repaint_flag = False

    def user_click(self, x, y):
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(x, y):
                return index
        return -1

    def resize(self, width, height):
        colors_amount = len(self.model.color_list)
        space_per_color = (width/colors_amount)
        self.rect_side = int(space_per_color / 2)
        self.gap = self.rect_side
        self.height = self.gap * 2 + self.rect_side
        self.repaint_flag = True

    def request_repaint(self):
        self.repaint_flag = True


