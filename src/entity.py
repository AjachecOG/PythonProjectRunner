import pygame


class Entity:
    def __init__(self, x, y, width, height, entity_type, damage=0, animation=None, debug=False):
        """
        Klasa bazowa dla przeszkód w grze.

        :param x: Pozycja X.
        :param y: Pozycja Y.
        :param width: Szerokość.
        :param height: Wysokość.
        :param entity_type: Typ obiektu (np. "bird", "fox").
        :param damage: Obrażenia zadawane przez obiekt.
        :param animation: Obiekt animacji.
        :param debug: Flaga debugowania (wyświetlanie prostokąta zamiast tekstury).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.type = entity_type
        self.damage = damage
        self.animation = animation
        self.has_hit = False
        self.cooldown = 0
        self.has_left = False
        self.debug = debug

    def left(self):
        """Oznacza, że obiekt opuścił ekran."""
        self.has_left = True

    def update(self, speed):
        """Aktualizuje pozycję i animację obiektu."""
        self.rect.x -= speed * 2
        if self.animation and not self.debug:
            self.animation.update()
        if self.rect.right < 0:
            self.left()
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self, screen):
        """Rysuje obiekt na ekranie."""
        if self.debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        elif self.animation:
            frame = self.animation.get_frame()
            screen.blit(frame, frame.get_rect(center=self.rect.center))
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def check_collision(self, player):
        """Sprawdza kolizję z graczem."""
        if self.rect.colliderect(player.rect):
            if self.rect.collidepoint(player.rect.centerx, player.rect.centery):
                return 0
            if self.cooldown > 0:
                return 0
            self.has_hit = True
            return self.damage
        else:
            self.has_hit = False
        return 0
