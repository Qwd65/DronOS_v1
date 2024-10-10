import pygame
import random

class Intruder:
    def __init__(self, x=None, y=None):
        # Если x и y не указаны, выбираем случайные значения
        if x is None or y is None:
            self.position = [random.randint(100, 700), random.randint(100, 500)]  # Стартовая позиция
        else:
            self.position = [x, y]  # Задаем начальную позицию
        self.speed = 3  # Скорость нарушителя
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]  # Направление движения

    def update(self):
        # Обновление позиции нарушителя
        self.position[0] += self.direction[0] * self.speed
        self.position[1] += self.direction[1] * self.speed

        # Если нарушитель достигает границ экрана, меняем направление
        if self.position[0] <= 0 or self.position[0] >= 800:
            self.direction[0] *= -1
        if self.position[1] <= 0 or self.position[1] >= 600:
            self.direction[1] *= -1

    def move_away_from_drones(self, drones):
        # Логика уклонения от дронов
        for drone in drones:
            dist_x = drone.position[0] - self.position[0]
            dist_y = drone.position[1] - self.position[1]

            if abs(dist_x) < 100 and abs(dist_y) < 100:  # Если дрон рядом, нарушитель убегает
                if dist_x > 0:
                    self.direction[0] = -1
                else:
                    self.direction[0] = 1

                if dist_y > 0:
                    self.direction[1] = -1
                else:
                    self.direction[1] = 1

    def check_boundaries(self):
        # Обеспечивает, что нарушители остаются в пределах карты
        if self.position[0] < 0:
            self.position[0] = 0
        elif self.position[0] > 800:
            self.position[0] = 800

        if self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] > 600:
            self.position[1] = 600

