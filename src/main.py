import pygame
from sys import exit
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from player import Player
from animation import Animation
from background import draw_background
import random
from fox import Fox
from bird import Bird

# --- Inicjalizacja gry ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Runner Game')

# --- Ładowanie grafik ---
ground_surface = pygame.image.load('ground.png').convert_alpha()
sky_surface = pygame.image.load('Sky.png').convert_alpha()
ground_width = ground_surface.get_width()
sky_width = sky_surface.get_width()

# --- Tworzenie obiektów gry ---
clock = pygame.time.Clock()
GameSpeed = 100
deltatime = 0
offset_x = 0
entities = []
game_active = True  # Zmienna określająca, czy gra jest aktywna

# --- Konfiguracja gracza ---
player_run_animation = Animation('Shinobi/Run.png', total_columns=8, total_rows=1)
player_jump_animation = Animation('Shinobi/Jump.png', total_columns=12, total_rows=1, frame_delay=1)
player_jump_animation.stop_at_last_frame = False

player1 = Player(100, 400, 20, 80)
player1.add_animation('run', player_run_animation)
player1.add_animation('jump', player_jump_animation)
player1.set_animation('run')
player1.debug = False

# --- Konfiguracja Sonic Speed ---
SONIC_MODE_DURATION = 5000  # 5 sekund Sonic Speed
COOLDOWN_DURATION = 10000   # 10 sekund cooldown
last_activation_time = -COOLDOWN_DURATION
is_sonic_active = False
SONIC_SPEED_EVENT = pygame.USEREVENT + 1

# --- Tworzenie przeszkód ---
def create_entities():
    """
    Tworzy losowo przeszkody (Bird lub Fox).
    """
    level_x = 600
    level_y_lis = 385  # Poziom lisa
    level_y_ptak = 310  # Poziom ptaka

    if random.choices(["bird", "fox"], weights=[33, 67])[0] == "bird":
        bird_animation = Animation('BlueBird.png', total_columns=10, total_rows=9, row=7, frame_delay=10, flip_horizontal=True)
        bird_animation.set_frame_range(1, 8)
        return Bird(level_x, level_y_ptak, 15, 15, animation=bird_animation, debug=False, scale=(25, 25))
    else:
        fox_animation_paths = [f"Fox/foxrun{i+1}.png" for i in range(8)]
        fox_animation = Animation(fox_animation_paths, frame_delay=8, flip_horizontal=True)
        return Fox(level_x, level_y_lis, 15, 15, animation=fox_animation, debug=False, scale=(35, 35))

# --- Funkcje gry ---
def handle_sonic_speed():
    """
    Obsługuje tryb Sonic Speed, zwiększając FPS na ograniczony czas.
    """
    global FPS, last_activation_time, is_sonic_active

    current_time = pygame.time.get_ticks()
    if is_sonic_active:
        print("Sonic Speed is already active!")
        return

    if current_time - last_activation_time >= COOLDOWN_DURATION:
        FPS = 120
        is_sonic_active = True
        last_activation_time = current_time
        print("Sonic Speed activated!")
        pygame.time.set_timer(SONIC_SPEED_EVENT, SONIC_MODE_DURATION)
    else:
        time_left = (last_activation_time + COOLDOWN_DURATION - current_time) // 1000
        print(f"Cooldown active. Wait {time_left} seconds.")

def handle_events():
    """
    Obsługuje zdarzenia użytkownika, takie jak skok lub aktywacja Sonic Speed.
    """
    global FPS, is_sonic_active, game_active

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == SONIC_SPEED_EVENT:
            FPS = 60
            is_sonic_active = False
            pygame.time.set_timer(SONIC_SPEED_EVENT, 0)
            print("Sonic Speed deactivated!")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player1.rect.collidepoint(event.pos):
                player1.start_jump(15)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and not player1.is_jumping:
        player1.start_jump(8.5)
    if keys[pygame.K_DOWN]:
        player1.move('down')
    if keys[pygame.K_SPACE]:
        handle_sonic_speed()
    if keys[pygame.K_1]:
        print(f"Player X: {player1.rect.x}, Player Y: {player1.rect.y}")

def update_game_state():
    """
    Aktualizuje stan gry, przesuwa gracza i przeszkody.
    """
    global deltatime, offset_x
    deltatime += clock.get_time()
    if deltatime >= GameSpeed:
        player1.update()
        deltatime = 0

    offset_x += player1.speed
    to_remove = []

    for entity in entities:
        entity.update(player1.speed)
        if entity.check_collision(player1):
            to_remove.append(entity)
            if entity.has_hit:
                gameover()
        if entity.has_left:
            to_remove.append(entity)

    for entity in to_remove:
        entities.remove(entity)

    if len(entities) < 1:
        entities.append(create_entities())

def render_game():
    """
    Rysuje tło, gracza oraz przeszkody.
    """
    screen.fill((255, 255, 255))
    draw_background(screen, sky_surface, ground_surface, offset_x, sky_width, ground_width)

    for entity in entities:
        entity.draw(screen)

    player1.draw(screen)
    pygame.display.update()

def gameover():
    global game_active
    game_active = False

def display_restart_message():
    font = pygame.font.Font(None, 50)
    restart_message = font.render("Press R to Restart", True, (255, 0, 0))
    message_rect = restart_message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(restart_message, message_rect)

def restart_game():
    global game_active, entities, deltatime, offset_x, last_activation_time, is_sonic_active

    game_active = True
    entities = []
    deltatime = 0
    offset_x = 0
    last_activation_time = -COOLDOWN_DURATION
    is_sonic_active = False

    # Dodaj początkową przeszkodę
    entities.append(create_entities())
# --- Pętla gry ---
while True:
    handle_events()

    if game_active:
        update_game_state()
        render_game()
    else:
        screen.fill((255, 255, 255))  # Biały ekran
        display_restart_message()  # Wyświetl komunikat restartu
        pygame.display.update()

        # Obsługa ponownego uruchomienia gry
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Naciśnięcie SPACJI
            restart_game()

    clock.tick(FPS)
