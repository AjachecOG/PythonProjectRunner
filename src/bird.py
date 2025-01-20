import pygame
from entity import Entity

class Bird(Entity):
    def __init__(self, x, y, width, height, animation=None, scale=None,debug = False):
        """
        Klasa reprezentująca ptaka jako przeszkodę w grze.
        :param x: Pozycja X.
        :param y: Pozycja Y.
        :param width: Szerokość obiektu.
        :param height: Wysokość obiektu.
        :param animation: Animacja ptaka (instancja Animation).
        :param scale: Krotka (szerokość, wysokość) dla skalowania.
        """
        super().__init__(x, y, width, height, "bird", damage=1, animation=animation,debug=debug)

        # Skalowanie animacji, jeśli przekazano argument
        if scale and self.animation:
            self.scale_animation(scale)

    def scale_animation(self, scale):
        """
        Skaluje animację ptaka do podanego rozmiaru.
        :param scale: Krotka (szerokość, wysokość) do skalowania klatek animacji.
        """
        if self.animation and self.animation.frames:
            self.animation.frames = [
                pygame.transform.scale(frame, scale) for frame in self.animation.frames
            ]

    def update(self, speed):
        """
        Aktualizuje pozycję i animację ptaka.
        :param speed: Prędkość przesuwania obiektu.
        """
        super().update(speed)
