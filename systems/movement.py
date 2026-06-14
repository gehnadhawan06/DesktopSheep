import random
from PySide6.QtGui import QGuiApplication


class MovementSystem:
    def __init__(self, widget):
        self.widget = widget
        self.dx = -1
        self.dy = 1

    def move(self):
        if self.widget.frozen:
            return

        if self.widget.state != "walk":
            return

        screen_width, screen_height = self.get_screen_size()

        new_x = self.widget.x() + self.dx
        new_y = self.widget.y() + self.dy

        if (
            new_x <= 0
            or new_x + self.widget.width() >= screen_width
            or new_y <= 0
            or new_y + self.widget.height() >= screen_height
        ):
            self.choose_safe_direction(screen_width, screen_height)

        self.widget.move(
            self.widget.x() + self.dx,
            self.widget.y() + self.dy
        )


    def choose_safe_direction(self, screen_width, screen_height):
        directions = [
            (-1, 0),
            (-1, -1),
            (-1, 1),
            (1, 0),
            (1, -1),
            (1, 1),
        ]

        valid = []

        for dx, dy in directions:
            test_x = self.widget.x() + dx
            test_y = self.widget.y() + dy

            if (
                test_x >= 0
                and test_x + self.widget.width() <= screen_width
                and test_y >= 0
                and test_y + self.widget.height() <= screen_height
            ):
                valid.append((dx, dy))

        if valid:
            self.dx, self.dy = random.choice(valid)
            self.widget.update_facing()

    def choose_random_direction(self):
        straight = [(-1, 0), (1, 0)]
        diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if random.random() < 0.6:
            self.dx, self.dy = random.choice(straight)
        else:
            self.dx, self.dy = random.choice(diagonal)

        self.widget.update_facing()

    def get_screen_size(self):
        screen = QGuiApplication.primaryScreen()
        geo = screen.geometry()
        return geo.width(), geo.height()