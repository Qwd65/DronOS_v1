from ai.drone_ai import DroneAI
from game.game_manager import GameManager

def generate_training_data():
    # Генерация данных на основе простых симуляций игры
    data = []
    for _ in range(100):  # Эпохи симуляции
        game = GameManager(mode='ai')
        # Собирать данные о состоянии игры и целевых действиях
        state = game.get_state()
        target = game.get_target_actions()
        data.append((state, target))
    return data

def train_model():
    model = DroneAI()
    data = generate_training_data()
    model.train_model(data)
    model.save('models/drone_model.pth')

