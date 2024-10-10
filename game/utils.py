import pygame
import math

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def draw_ui(screen, drones, intruders, score, time_left):
    screen.fill(WHITE)  # Очистка экрана

    # Отрисовка дронов и выделение выбранного дрона
    for drone in drones:
        draw_drone(screen, drone)

    # Отрисовка нарушителей
    for intruder in intruders:
        draw_intruder(screen, intruder)

    # Отображение таймера и очков
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f"Time left: {int(time_left)}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    
    screen.blit(timer_text, (10, 10))  # Время отображается в левом верхнем углу
    screen.blit(score_text, (10, 50))  # Очки отображаются под временем

def draw_drone(screen, drone):
    color = RED if drone.selected else BLUE  # Подсветка выбранного дрона красным
    pygame.draw.circle(screen, color, (int(drone.position[0]), int(drone.position[1])), 20)
    if drone.selected:
        pygame.draw.circle(screen, GREEN, (int(drone.position[0]), int(drone.position[1])), 25, 2)

def draw_intruder(screen, intruder):
    pygame.draw.circle(screen, BLACK, (int(intruder.position[0]), int(intruder.position[1])), 15)

def distance(pos1, pos2):
    return math.hypot(pos2[0] - pos1[0], pos2[1] - pos1[1])

