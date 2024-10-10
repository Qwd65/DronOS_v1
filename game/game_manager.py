import pygame
from game.drone import Drone
from game.intruder import Intruder
from game.utils import draw_ui

class GameManager:
    def __init__(self, mode='player'):
        # Original map size likely here
        self.last_spawn_time = pygame.time.get_ticks()
        self.screen_width = 800  # New smaller width
        self.screen_height = 600  # New smaller height
        self.bg_color = (50, 50, 50)  # Gray background for contrast
        self.boundary_color = (255, 0, 0)  # Red boundary lines for clarity
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
            self.draw_boundary(self.screen)
            if pygame.time.get_ticks() - self.last_spawn_time > self.intruder_spawn_time:
                self.spawn_intruder()
                self.last_spawn_time = pygame.time.get_ticks()
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
                    
    def spawn_intruder(self):
        if len(self.intruders) < 6:  # Max 6 intruders
            new_intruder = Intruder(random.randint(0, self.screen_width), random.randint(0, self.screen_height))
            self.intruders.append(new_intruder)
            
    def draw_boundary(self, screen):
        pygame.draw.rect(screen, self.boundary_color, pygame.Rect(0, 0, self.screen_width, self.screen_height), 5)
