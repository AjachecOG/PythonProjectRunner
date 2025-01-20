import pygame


class Animation:
    def __init__(self, image_path_or_list, total_columns: int = 1, total_rows: int = 1,
                 frame_delay: int = 1, row: int = 1, flip_horizontal: bool = False):
        """
        Zarządza animacjami z pojedynczego obrazu zbiorczego lub listy obrazów.

        :param image_path_or_list: Ścieżka do obrazu animacji lub lista ścieżek do obrazów.
        :param total_columns: Liczba kolumn w obrazie zbiorczym (jeśli używane).
        :param total_rows: Liczba wierszy w obrazie zbiorczym (jeśli używane).
        :param frame_delay: Liczba ticków między zmianami klatek.
        :param row: Wiersz (1-indeksowany), z którego wyświetlane są klatki (dla obrazu zbiorczego).
        :param flip_horizontal: Czy odbić obrazy w poziomie.
        """
        self.frame_delay = frame_delay
        self.frame_timer = 0
        self.current_frame = 0
        self.stop_at_last_frame = False


        # Obsługa listy obrazów
        if isinstance(image_path_or_list, list):
            self.frames = [pygame.image.load(path).convert_alpha() for path in image_path_or_list]
            if flip_horizontal:
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
            self.total_frames = len(self.frames)
        else:
            # Obsługa obrazu zbiorczego
            self.surface = pygame.image.load(image_path_or_list).convert_alpha()
            if flip_horizontal:
                self.surface = pygame.transform.flip(self.surface, True, False)
            self.total_columns = total_columns
            self.total_rows = total_rows
            self.frame_width = self.surface.get_width() / total_columns
            self.frame_height = self.surface.get_height() / total_rows
            self.row = row - 1
            self.total_frames = total_columns
            self.frames = None  # Tryb obrazu zbiorczego

        self.frame_range = (0, self.total_frames - 1)

    @property
    def debug(self):
        """Getter """
        return self._debug

    @debug.setter
    def debug(self, value):
        """Setter"""
        if isinstance(value, bool):
            self._debug = value
        else:
            raise ValueError("Debug musi być wartością logiczną (True lub False).")

    def update(self):
        """Aktualizuje animację, przełączając klatki w odpowiednim tempie."""
        if self.stop_at_last_frame and self.current_frame == self.frame_range[1]:
            return  # Zatrzymaj się na ostatniej klatce

        self.frame_timer += 1
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame > self.frame_range[1]:
                self.current_frame = self.frame_range[0]

    def get_frame(self):
        """Zwraca aktualną klatkę jako Surface."""
        if self.frames:
            return self.frames[self.current_frame]
        else:
            frame_rect = pygame.Rect(
                self.current_frame * self.frame_width,
                self.row * self.frame_height,
                self.frame_width,
                self.frame_height
            )
            return self.surface.subsurface(frame_rect)

    def set_frame_range(self, start: int, end: int, stop_at_last: bool = False):
        """Ustawia zakres klatek dla animacji."""
        self.frame_range = (start, end)
        self.current_frame = self.frame_range[0]
        self.stop_at_last_frame = stop_at_last
