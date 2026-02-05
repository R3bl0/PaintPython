import pygame
from view_dir import canvas_view

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 760

BACKGROUND_COLOR = pygame.Color(123, 166, 234)

VERTICAL_CANVAS_OFFSET = 50
HORIZONTAL_CANVAS_OFFSET = 50

FPS = 60

class View:
    def __init__(self, canvas_view, palette_view, slider, timer, vote_buttons, theme_label):
        self.game_started_flag = False
        self.running = True

        self.background_image = pygame.image.load("graphics/background.jpg")

        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT

        self.vertical_offset = VERTICAL_CANVAS_OFFSET
        self.horizontal_offset = HORIZONTAL_CANVAS_OFFSET

        self.canvas_origin_x = None
        self.canvas_origin_y = None

        self.screen = None
        self.clock = pygame.time.Clock()

        self.canvas_view = canvas_view

        self.is_draw_phase = False
        self.is_vote_phase = False
        self.is_results_phase = False

        self.past_mouse_pos = None
        self.cursor_locked_to_canvas = False

        self.slider = slider
        self.palette_view = palette_view
        self.timer = timer
        self.vote_buttons = vote_buttons
        self.theme_label = theme_label

        self.brush_size = 3
        self.color_index = 1

        self.palette_x_start = None
        self.palette_y_start = None
        self.palette_x_end = None
        self.palette_y_end = None

        self.slider_x_start = None
        self.slider_y_start = None
        self.slider_x_end = None
        self.slider_y_end = None

        self.canvas_x_start = None
        self.canvas_y_start = None
        self.canvas_x_end = None
        self.canvas_y_end = None

    def game_has_started(self):
        return self.game_started_flag

    def start_game(self):
        self.game_started_flag = True

    def close(self):
        self.running = False

    def resize(self):
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        rect = self.background_image.get_rect(topleft=(0, 0))
        self.screen.blit(self.background_image, rect)

        canvas_zone_width = self.width - 2 * self.horizontal_offset
        canvas_zone_height = self.height - 2 * self.vertical_offset

        self.canvas_view.resize(canvas_zone_width, canvas_zone_height)

        free_width = self.width - self.canvas_view.canvas_width
        free_height = self.height - self.canvas_view.canvas_height

        self.canvas_origin_x = (free_width // 2)
        self.canvas_origin_y = (free_height // 2)

        self.palette_view.resize(self.canvas_view.canvas_width, self.canvas_view.canvas_height)
        self.slider.resize(self.canvas_view.canvas_width)
        self.timer.resize(self.canvas_view.canvas_width//4, self.canvas_origin_y)
        self.vote_buttons.resize(self.canvas_view.canvas_width)
        self.theme_label.resize(int(self.canvas_view.canvas_width * 3/4), self.canvas_origin_y)

        self.palette_x_start = self.canvas_origin_x
        self.palette_y_start = self.canvas_view.canvas_height + self.canvas_origin_y
        self.palette_x_end = self.width - self.canvas_origin_x
        self.palette_y_end = self.canvas_view.canvas_height + self.canvas_origin_y + self.palette_view.height

        self.slider_x_start = self.canvas_origin_x
        self.slider_y_start = self.canvas_view.canvas_height + self.canvas_origin_y + self.palette_view.height
        self.slider_x_end = self.width - self.canvas_origin_x
        self.slider_y_end = self.canvas_view.canvas_height + self.canvas_origin_y + self.palette_view.height + self.slider.height

        self.canvas_x_start = self.canvas_origin_x
        self.canvas_y_start = self.canvas_origin_y
        self.canvas_x_end = self.canvas_view.canvas_width + self.canvas_origin_x
        self.canvas_y_end = self.canvas_view.canvas_height + self.canvas_origin_y

    def handle_click_drawing_enabled(self):
        x, y = pygame.mouse.get_pos()

        if self.palette_x_start < x < self.palette_x_end and self.palette_y_start < y < self.palette_y_end:
            self.past_mouse_pos = None
            if not self.cursor_locked_to_canvas:
                new_index = self.palette_view.user_click(x, y)
                if new_index != -1:
                    self.color_index = new_index

        elif self.slider_x_start < x < self.slider_x_end and self.slider_y_start < y < self.slider_y_end:
            self.past_mouse_pos = None
            if not self.cursor_locked_to_canvas:
                self.brush_size = self.slider.user_click(x - self.canvas_origin_x)

        elif self.canvas_x_start < x < self.canvas_x_end and self.canvas_y_start < y < self.canvas_y_end:
            self.cursor_locked_to_canvas = True
            x -= self.canvas_origin_x
            y -= self.canvas_origin_y
            if self.past_mouse_pos is not None:
                if self.past_mouse_pos[0] != x or self.past_mouse_pos[1] != y:
                    for point in canvas_view.CanvasView.points_in_line(x, y, self.past_mouse_pos[0], self.past_mouse_pos[1], self.brush_size):
                        self.canvas_view.user_paint(point[0], point[1], self.brush_size, self.color_index)
            self.canvas_view.user_paint(x, y, self.brush_size, self.color_index)
            self.past_mouse_pos = (x, y)

        else:
            self.past_mouse_pos = None

    def start_view(self):
        pygame.init()
        self.resize()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.resize()
                if self.is_draw_phase:
                    if pygame.mouse.get_pressed(3)[0]:
                        self.handle_click_drawing_enabled()
                    else:
                        self.past_mouse_pos = None
                        self.cursor_locked_to_canvas = False

                if self.is_vote_phase:
                    if pygame.mouse.get_pressed(3)[0]:
                        x, y = pygame.mouse.get_pos()
                        self.vote_buttons.user_click(x, y)

            if self.is_draw_phase:
                self.palette_view.draw(self.screen, self.canvas_origin_x, self.canvas_y_end)
                self.slider.draw(self.screen, self.canvas_origin_x, self.palette_y_end)
                self.theme_label.draw(self.screen, self.canvas_x_start + self.timer.width, 0)
                self.timer.draw(self.screen, self.canvas_x_start, 0)
                self.canvas_view.draw(self.screen, self.canvas_origin_x, self.canvas_origin_y)
            if self.is_vote_phase:
                self.vote_buttons.draw(self.screen, self.canvas_origin_x, self.canvas_y_end)
                self.theme_label.draw(self.screen, self.canvas_x_start + self.timer.width, 0)
                self.timer.draw(self.screen, self.canvas_x_start, 0)
                self.canvas_view.draw(self.screen, self.canvas_origin_x, self.canvas_origin_y)
            if self.is_results_phase:
                self.theme_label.draw(self.screen, self.canvas_x_start + self.timer.width, 0)
                self.timer.draw(self.screen, self.canvas_x_start, 0)
                self.canvas_view.draw(self.screen, self.canvas_origin_x, self.canvas_origin_y)


            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


    #canvas bytearray musi być przekazywany do modelu płótna bezpośrednio
    def notify_of_draw_phase(self, theme, time_to_draw):
        self.is_vote_phase = False
        self.is_results_phase = False
        self.is_draw_phase = True

        self.theme_label.set_text(theme)

        rect = self.background_image.get_rect(topleft=(0, 0))
        self.screen.blit(self.background_image, rect)
        self.canvas_view.request_full_repaint()
        self.canvas_view.draw(self.screen, self.canvas_origin_x, self.canvas_origin_y)
        self.theme_label.request_repaint()

        self.timer.set_time_start_countdown(time_to_draw)

    def notify_of_vote_phase(self, time_to_vote):
        self.is_draw_phase = False
        self.is_results_phase = False
        self.is_vote_phase = True

        rect = self.background_image.get_rect(topleft=(0, 0))
        self.screen.blit(self.background_image, rect)
        self.canvas_view.request_full_repaint()
        self.palette_view.request_repaint()
        self.theme_label.request_repaint()
        self.vote_buttons.request_repaint()

        self.timer.set_time_start_countdown(time_to_vote)


    def notify_of_vote_results(self, score, time_delay):
        self.is_vote_phase = False
        self.is_draw_phase = False
        self.is_results_phase = True

        self.theme_label.set_text(("Otrzymana liczba gwiazdek: " + str(score)))

        rect = self.background_image.get_rect(topleft=(0, 0))
        self.screen.blit(self.background_image, rect)
        self.palette_view.request_repaint()
        self.theme_label.request_repaint()
        self.canvas_view.request_full_repaint()

        self.timer.set_time_start_countdown(time_delay)




    def get_rating(self):
        return self.vote_buttons.get_rating()

