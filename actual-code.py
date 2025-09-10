import sys, pygame, os

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


def draw_start(screen, big, small, audio_loaded):
    screen.fill(BG)
    title = big.render("ShyRhythm", True, WHITE)
    hint = small.render("Press ENTER to start", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 40))
    screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 10))
    if audio_loaded: 
        msg = small.render("Press M to toggle music", True, WHITE)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 40))


def draw_play(screen, small, pulse_on, score, remaining_s):
    screen.fill(BG)
    cx, cy = WIDTH // 2, HEIGHT // 2
    radius = BIG_R if pulse_on else BASE_R
    pygame.draw.circle(screen, WHITE, (cx, cy), radius, width=2)
    score_text = small.render(f"Score: {score}", True, WHITE)
    time_text = small.render(f"Time: {remaining_s}s", True, WHITE)
    screen.blit(score_text, (16, 16))
    screen.blit(time_text, (16, 44))
    

def draw_end(screen, big, small, score):
    screen.fill(BG)
    result = big.render(f"Final score: {score}", True, WHITE)
    restart = small.render("Press R to restart", True, WHITE)
    screen.blit(result, (WIDTH//2 - result.get_width()//2, HEIGHT//2 - 30))
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 10))


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.display.set_caption("ShyRhythm (lite + music)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    small = pygame.font.SysFont(None, 28)
    big = pygame.font.SysFont(None, 48)

    audio_loaded = False
    try:
        if os.path.exists(LOOP_PATH):
            pygame.mixer.music.load(LOOP_PATH)
            audio_loaded = True
    except Exception:
        audio_loaded = False
    audio_on = False

    state = STATE_START
    t = 0.0
    pulse_timer = 0.0
    score = 0
    play_elapsed = 0.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

    elif event.type == pygame.KEYDOWN:
        if state == STATE_START and audio_loaded and event.key == pygame.K_m:
            audio_on = not audio_on
            if audio_on:
                pygame.mixer.music.play(loops=-1)
            else:
                pygame.mixer.music.stop()

        if state == STATE_START and event.key == pygame.K_RETURN:
            state = STATE_PLAY
            t = 0.0
            pulse_timer = 0.0
            score = 0
            play_elapsed = 0.0

        elif state == STATE_PLAY and event.key == pygame.K_SPACE:
            if pulse_timer > 0.0:
                score += 1

        elif state == STATE_END and event.key == pygame.K_r:
            state = STATE_START
