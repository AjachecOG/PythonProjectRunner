from settings import WINDOW_HEIGHT, GRAVITY
import pygame

class Player:
    def __init__(self, x, y,xwidth,ywidth,debug = False):
        self.rect = pygame.Rect(x, y - 70,xwidth, ywidth)
        self.animations = {}
        self.current_animation = None
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_peak_reached = False
        self.jump_start_y = 0
        self.speed = 3 # odpowiedzialne za szybkocsc(ofsetx) podloza
        self.debug = debug

    def add_animation(self, name, animation_object):
        self.animations[name] = animation_object
        if self.current_animation is None:
            self.current_animation = name

    def set_animation(self, name):
        if name in self.animations:
            self.current_animation = name

    def update(self):
        self.animations[self.current_animation].update()
        self.handle_jump()

    def handle_jump(self):
        if self.is_jumping:
            self.rect.y += self.velocity_y

            # Osiągnięcie szczytu
            if self.velocity_y > 0 and not self.jump_peak_reached:
                self.jump_peak_reached = True
                self.animations[self.current_animation].set_frame_range(6, 11, stop_at_last=True)  # Animacja opadania

            # Dodanie grawitacji
            self.velocity_y += GRAVITY * 6 # bo zwiekszamy jump_force

            # Powrót na ziemię
            if self.rect.y >= self.jump_start_y:
                self.rect.y = self.jump_start_y
                self.is_jumping = False
                self.jump_peak_reached = False
                self.velocity_y = 0
                self.set_animation('run')

    def start_jump(self, jump_force):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_peak_reached = False
            self.jump_start_y = self.rect.y
            self.velocity_y = -jump_force * 2# 4 razy szybszy skok w gore
            self.set_animation('jump')  # Przełącz na animację* 2oku
            self.animations[self.current_animation].set_frame_range(0, 5, stop_at_last=True)  # Wzlot
            self.animations[self.current_animation].current_frame = 0
            self.animations[self.current_animation].frame_delay = 1  # Animacja wzlotu działa szybciej

    def draw(self, screen):
        if self.debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.current_animation:
            frame = self.animations[self.current_animation].get_frame()
            screen.blit(frame, frame.get_rect(midbottom=self.rect.midbottom))

    def move(self, direction):
        if direction == 'up' and self.rect.y > 0:
            self.rect.y -= 2
        elif direction == 'down' and self.rect.y < (WINDOW_HEIGHT - self.rect.height):
            self.rect.y += 2
