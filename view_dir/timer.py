import pygame

class Timer:
    def __init__(self):
        self.time = None
        self.width = None
        self.height = None

        font_path = 'PixelOperator.ttf'
        font_size = 48
        pygame.font.init()
        self.font = pygame.font.Font(font_path, font_size)
        self.start_ticks = None

    def draw(self, screen, origin_x, origin_y):
        if self.start_ticks is not None:
            remaining_time = self.get_remaining_time()
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            time_str = f"{minutes%60}:{seconds%60}"
        else:
            time_str = "00:00"

        text_surface = self.font.render(time_str, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(origin_x + self.width // 2, origin_y + self.height // 2))

        pygame.draw.rect(screen, (147, 112, 219), (origin_x, origin_y, self.width, self.height))
        screen.blit(text_surface, text_rect)

    def get_remaining_time(self):
        seconds_passed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        remaining_time = self.time - seconds_passed
        if remaining_time > 0:
            return remaining_time
        return 0

    def resize(self, width, height):
        self.width = width
        self.height = height

    def set_time_start_countdown(self, time):
        self.time = time
        self.start_ticks = pygame.time.get_ticks()