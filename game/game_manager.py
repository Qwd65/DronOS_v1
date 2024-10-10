import pygame
import random  # Добавлен импорт
from game.drone import Drone
from game.intruder import Intruder
from game.utils import draw_ui

class GameManager:
    def __init__(self, mode='player'):
        self.last_spawn_time = pygame.time.get_ticks()
        self.intruder_spawn_time = 3000  # Время между спавнами нарушителей
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (50, 50, 50)
        self.boundary_color = (255, 0, 0)
        self.mode = mode
        self.drones = [Drone(i) for i in range(5)]
        self.intruders = []
        self.selected_drone = None
        self.score = 0
        self.time_left = 60

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        while self.time_left > 0:
            self.handle_events()
            self.update_game_state()
            self.draw_boundary(self.screen)
            if pygame.time.get_ticks() - self.last_spawn_time > self.intruder_spawn_time:
                self.spawn_intruder()
                self.last_spawn_time = pygame.time.get_ticks()
            draw_ui(self.screen, self.drones, self.intruders, self.score, self.time_left)
            pygame.display.flip()
            clock.tick(60)
            self.time_left -= 1 / 60

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
        for drone in self.drones:
            drone.update()
        for intruder in self.intruders:
            intruder.update()

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
                    
    def spawn_intruder(self):
        if len(self.intruders) < 6:  # Max 6 intruders
            new_intruder = Intruder(random.randint(0, self.screen_width), random.randint(0, self.screen_height))
            self.intruders.append(new_intruder)
            
    def draw_boundary(self, screen):
        pygame.draw.rect(screen, self.boundary_color, pygame.Rect(0, 0, self.screen_width, self.screen_height), 5)
    
    def get_state(self):
        # Собираем состояние игры
        drone_positions = [drone.position for drone in self.drones]
        intruder_positions = [intruder.position for intruder in self.intruders]
        score = self.score
        time_left = self.time_left

        # Возвращаем состояние как словарь или кортеж
        return {
            'drone_positions': drone_positions,
            'intruder_positions': intruder_positions,
            'score': score,
            'time_left': time_left
        }
        
    def get_target_actions(self):
        # Логика для определения целевых действий для дронов
        actions = []
        for drone in self.drones:
            # Определите, какое действие должен предпринять дрон
            # Например, перемещение к ближайшему нарушителю
            nearest_intruder = self.get_nearest_intruder(drone)
            if nearest_intruder:
                actions.append({'drone_id': drone.index, 'target_position': nearest_intruder.position})
            else:
                actions.append({'drone_id': drone.index, 'target_position': drone.position})  # Остается на месте

        return actions

    def get_nearest_intruder(self, drone):
        # Поиск ближайшего нарушителя
        nearest_intruder = None
        min_distance = float('inf')
        for intruder in self.intruders:
            distance = self.calculate_distance(drone.position, intruder.position)
            if distance < min_distance:
                min_distance = distance
                nearest_intruder = intruder
        return nearest_intruder

    def calculate_distance(self, pos1, pos2):
        # Вычисление расстояния между двумя позициями
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

