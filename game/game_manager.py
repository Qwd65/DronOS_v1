import pygame
from game.drone import Drone
from game.intruder import Intruder
from game.utils import draw_ui

class GameManager:
    def __init__(self, mode='player'):
        self.mode = mode
        self.drones = [Drone(i) for i in range(5)]
        self.intruders = []
        self.selected_drone = None
        self.score = 0
        self.time_left = 60  # Время игры в секундах

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        while self.time_left > 0:
            self.handle_events()
            self.update_game_state()
            draw_ui(screen, self.drones, self.intruders, self.score, self.time_left)
            pygame.display.flip()
            clock.tick(60)
            self.time_left -= 1 / 60  # Обновляем таймер

        print(f"Игра окончена! Вы набрали {self.score} очков.")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка — выбор дрона
                    self.select_drone(event.pos)
                elif event.button == 3:  # Правая кнопка — перемещение выбранного дрона
                    if self.selected_drone:
                        self.selected_drone.move_to(event.pos)

    def update_game_state(self):
        # Обновляем состояние дронов и нарушителей
        for drone in self.drones:
            drone.update()
        for intruder in self.intruders:
            intruder.update()

        # Проверяем столкновения и начисляем очки
        self.check_collisions()

    def select_drone(self, position):
        for drone in self.drones:
            if drone.is_clicked(position):
                self.selected_drone = drone
                break

    def check_collisions(self):
        for drone in self.drones:
            for intruder in self.intruders:
                if drone.check_collision(intruder):
                    self.intruders.remove(intruder)
                    self.score += 1

