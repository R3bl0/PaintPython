import pygame
class ThemeLabel:
    def __init__(self):
        self.theme = 'temat do narysowania'
        self.width = None
        self.height = None
        self.repaint_flag = True

        font_path = 'PixelOperator.ttf'
        font_size = 33
        pygame.font.init()
        self.font = pygame.font.Font(font_path, font_size)
        pygame.font.init()

    def set_text(self, text):
        self.theme = text

    def draw(self, screen, origin_x, origin_y):
        if self.repaint_flag:
            text_surface = self.font.render(self.theme, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(origin_x + self.width // 2, origin_y + self.height // 2))
            pygame.draw.rect(screen, (123, 166, 234), (origin_x, origin_y, self.width, self.height))
            screen.blit(text_surface, text_rect)
            self.repaint_flag = False

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.repaint_flag = True

    def request_repaint(self):
        self.repaint_flag = True

