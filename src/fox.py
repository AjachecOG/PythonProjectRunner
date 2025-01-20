import pygame
from entity import Entity


class Fox(Entity):
    def __init__(self, x, y, width, height, animation=None, scale=None, debug=False):
        """
        Klasa reprezentująca lisa jako przeszkodę w grze.

        :param x: Pozycja X.
        :param y: Pozycja Y.
        :param width: Szerokość rect lisa.
        :param height: Wysokość rect lisa.
        :param animation: Obiekt animacji dla lisa.
        :param scale: Skalowanie obrazów lisa.
        :param debug: Flaga debugowania.
        """
        super().__init__(x, y, width, height, 'fox', damage=1, animation=animation, debug=debug)

        if scale:
            if self.animation:
                self.animation.frames = [pygame.transform.scale(frame, scale) for frame in self.animation.frames]
            self.rect = pygame.Rect(x, y, *scale)

    def update(self, speed):
        """Aktualizuje pozycję i animację lisa."""
        super().update(speed)

    def draw(self, screen):
        """Rysuje lisa na ekranie."""
        super().draw(screen)
