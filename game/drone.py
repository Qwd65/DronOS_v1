import pygame

class Drone:
    def __init__(self, index):
        self.index = index
        self.position = [100 * index, 100]  # Разные стартовые позиции
        self.selected = False
        self.target_position = None

    def update(self):
        if self.target_position:
            self.move()

    def move(self):
        # Простой алгоритм движения к цели
        x_diff = self.target_position[0] - self.position[0]
        y_diff = self.target_position[1] - self.position[1]
        step = min(5, (x_diff ** 2 + y_diff ** 2) ** 0.5)
        self.position[0] += step * (x_diff / max(abs(x_diff), 1))
        self.position[1] += step * (y_diff / max(abs(y_diff), 1))

    def move_to(self, position):
        self.target_position = position

    def is_clicked(self, position):
        # Проверка, кликает ли игрок по дрону
        return abs(self.position[0] - position[0]) < 20 and abs(self.position[1] - position[1]) < 20

    def check_collision(self, intruder):
        # Простой хитбокс: если дрон касается нарушителя
        return abs(self.position[0] - intruder.position[0]) < 20 and abs(self.position[1] - intruder.position[1]) < 20

