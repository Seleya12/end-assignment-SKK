import sys, pygame 

WIDTH, HEIGHT = 800, 600
BG = (15, 15, 30)
WHITE = (240, 240, 255)

STATE_START = 0
STATE_PLAY = 1
STATE_END = 2

INTERVAL = 0.6
PULSE_TIME = 0.12
BASE_R = 22
BIG_R = 38

PLAY_TIME = 20.0

LOOP_PATH = os.path.join("media", "loop.ogg") #path for the possible sound


def draw_start(screen, big, small): 
    screen.fill(BG)
    title = big.render("ShyRhythm", True, WHITE)
    hint = small.render("Press ENTER to start", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 40))
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 10))
    if audio_loaded: 
        msg = small.render("Press M to toggle music", True, WHITE)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 40)
