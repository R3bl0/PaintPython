import menu
from view_dir import canvas_view, palette_view, slider, timer, vote_buttons, theme_label, model
from view_dir import view
from menu_parts import handlers

import time
import threading


"""
#tu metody, funkcje menu

is_host = True #ta wartość z menu wychodzi


if is_host: #jak jest w trybie hosta, to dysponuje listą z socketami


else: #jak jest w trybie klienta to jest tylko jeden socket wejście
    #czekaj na temat
    theme = 'theme'

    #czekaj na czas na rysowanie
    time_to_draw = 90

#powiedz view, że
#view.draw_phase(theme, time_to_draw)

#czekaj na powrót z view (wywołanie metody nastąpi po upłynięciu ustalonego czasu)

#zawsze jest własny canvas
finished_canvas = bytearray()

if is_host:
    client_canvases = {}
    #czekaj i zbieraj bytearraye-rysunki przychodzące od klientów

    #po zebraniu, jest cykl:
    for canvas in client_canvases:
        #wysyłasz wybraną pracę do wszystkich klientów

        #dajesz widokowi pracę, uruchamiany jest interfejs do głosowania (jakiś czas jest ustalony)
        #view.rate(canvas, time_to_rate)
        #rate_phase()
else:
    #wyślij swój canvas hostowi
    
    #czekasz na bytearray od hosta
    #view.rate(canvas, time_to_rate)
    #rate_phase()


def rate_phase():
    #jeden rating jest zawsze z gracza-hosta albo gracza-klienta
    given_rating = 3
    
    if is_host:
        client_ratings = {}
        #trzeba czekać na wyniki przychodzące od klientów
        client_ratings = {"nick1": 3, "nick2": 0}
    else:
        #prześlij swój rating do hosta
    
        #należy czekać aż host odeśle wszystkie ratingi
        client_ratings = {"nick1": 3, "nick2": 0}
    
    #po zebraniu wszystkich ocen, trzeba przekazać je do widoku do wyświetlenia
    #view.show_ratings

"""

model = model.CanvasModel()
view_component = view.View(canvas_view.CanvasView(model), palette_view.PaletteView(model), slider.Slider(), timer.Timer(), vote_buttons.VoteButtons(), theme_label.ThemeLabel())
menu_component = menu.Menu(view_component, model)

thread = threading.Thread(target = menu_component.start_menu)
thread.start()

while view_component.running:
    if view_component.game_has_started():
        view_component.start_view()
    time.sleep(0.2)






# model = model.CanvasModel()
# view = view.View(canvas_view.CanvasView(model), palette_view.PaletteView(model), slider.Slider(), timer.Timer(), vote_buttons.VoteButtons(), theme_label.ThemeLabel())
#
# threading.Thread(target = view.start_view).start()
#
# time.sleep(1)
# while(True):
#     draw_time = 10
#     theme = 'gówno'
#
#     view.notify_of_draw_phase(theme, draw_time)
#
#     #bytearray można wziąć:
#     bytearray = model.array
#
#     time.sleep(draw_time)
#
#     vote_time = 10
#     view.notify_of_vote_phase(vote_time)
#
#     time.sleep(vote_time)
#
#     rating = view.get_rating()
#
#     time_delay = 5
#     view.notify_of_vote_results(rating, 5)
#
#     time.sleep(5)
#     model.reset()