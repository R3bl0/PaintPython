import pygame

class VoteButtons:
    def __init__(self):
        self.image_off = pygame.image.load("graphics/star_inactive.png")
        self.image_on = pygame.image.load("graphics/star_active.png")

        self.gap = None
        self.rect_side = None
        self.height = None
        self.model = [1, 0, 0, 0, 0]
        self.rects = []

        self.repaint_flag = True

    def get_rating(self):
        for i in range(len(self.model) - 1, 0, -1):
            if self.model[i] == 1:
                return i + 1
        return 1

    def draw(self, screen, origin_x, origin_y):
        if self.repaint_flag:
            self.rects = []
            x = origin_x + self.gap // 2
            y = origin_y + self.gap // 4
            for state in self.model:
                image = self.image_on if state == 1 else self.image_off
                rect = image.get_rect(topleft=(x, y))
                screen.blit(image, rect)
                self.rects.append(rect)
                x += self.rect_side + self.gap
            self.repaint_flag = False
    def resize(self, width):
        space_per_button = (width/5)
        self.rect_side = int(space_per_button / 2)
        self.gap = self.rect_side
        self.height = self.gap * 2 + self.rect_side
        self.repaint_flag = True

    def user_click(self, x, y):
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(x, y):
                if self.model[index] == 0:
                    for i in range(index + 1):
                        self.model[i] = 1
                else:
                    for i in range(index + 1, len(self.model)):
                        self.model[i] = 0
        self.repaint_flag = True

    def request_repaint(self):
        self.repaint_flag = True