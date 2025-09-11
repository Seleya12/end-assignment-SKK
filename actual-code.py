import sys, pygame, os

WIDTH, HEIGHT = 800, 600
BG = (15, 15, 30)
WHITE = (240, 240, 255)

STATE_START = 0
STATE_PLAY = 1
STATE_END = 2

BPM = 192
INTERVAL = 60.0 / BPM
PULSE_TIME = 0.12
BASE_R = 22
BIG_R = 38

PLAY_TIME = 20.0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOOP_PATH = os.path.join(BASE_DIR, "media", "loop.ogg")


def draw_start(screen, big, small, audio_loaded):
    screen.fill(BG)
    title = big.render("Roads Untraveled Rythm-Game", True, WHITE)
    hint = small.render("Press ENTER to start", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 10))
    if audio_loaded:
        msg = small.render("Press M to toggle music", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 + 40))
    else:
        msg = small.render("No music file found", True, WHITE)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 + 40))


def draw_play(screen, small, pulse_on, score, remaining_s):
    screen.fill(BG)
    cx, cy = WIDTH // 2, HEIGHT // 2
    radius = BIG_R if pulse_on else BASE_R
    pygame.draw.circle(screen, WHITE, (cx, cy), radius, width=2)
    score_text = small.render(f"Score: {score}", True, WHITE)
    time_text = small.render(f"Time: {remaining_s}s", True, WHITE)
    screen.blit(score_text, (16, 16))
    screen.blit(time_text, (16, 44))


def draw_end(screen: pygame.Surface, big: pygame.font.Font, small: pygame.font.Font, score: int):
    screen.fill(BG)
    result = big.render(f"Final score: {score}", True, WHITE)
    restart = small.render("Press R to restart", True, WHITE)
    screen.blit(result, (WIDTH//2 - result.get_width()//2, HEIGHT//2 - 30))
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 10))


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    pygame.display.set_caption("Roads Untraveled Rythm-Game (lite + music)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    small = pygame.font.SysFont(None, 28)
    big = pygame.font.SysFont(None, 48)

    audio_loaded = False
    try:
        if os.path.exists(LOOP_PATH):
            pygame.mixer.music.load(LOOP_PATH)
            pygame.mixer.music.set_volume(0.8)
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
                if audio_loaded and event.key == pygame.K_m:
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
                    if audio_loaded:
                        pygame.mixer.music.play(loops=-1)

                elif state == STATE_PLAY and event.key == pygame.K_SPACE:
                    if pulse_timer > 0.0:
                        score += 1

                elif state == STATE_END and event.key == pygame.K_r:
                    state = STATE_START

        if state == STATE_START:
            draw_start(screen, big, small, audio_loaded)

        elif state == STATE_PLAY:
            play_elapsed += dt
            beat_triggered = False

            if audio_loaded and audio_on and pygame.mixer.music.get_pos() >= 0:
                pos_s = pygame.mixer.music.get_pos() / 1000.0
                if (pos_s % INTERVAL) < dt:
                    beat_triggered = True
            else:
                t += dt
                if (t % INTERVAL) < dt:
                    beat_triggered = True

            if beat_triggered:
                pulse_timer = PULSE_TIME

            if pulse_timer > 0.0:
                pulse_timer = max(0.0, pulse_timer - dt)
            remaining = max(0, int(PLAY_TIME - play_elapsed))
            draw_play(screen, small, pulse_timer > 0.0, score, remaining)
            if play_elapsed >= PLAY_TIME:
                state = STATE_END
                if audio_loaded:
                    pygame.mixer.music.stop()

        else:
            draw_end(screen, big, small, score)

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
