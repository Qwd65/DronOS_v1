from ai.drone_ai import DroneAI
from game.game_manager import GameManager

def generate_training_data():
    # Генерация данных на основе простых симуляций игры
    data = []
    for _ in range(100):  # 100 эпох симуляции
        game = GameManager(mode='ai')
        state = game.get_state()  # Получаем состояния игры
        target = game.get_target_actions()  # Получаем действия
        data.append((state, target))  # Добавляем в виде кортежей (состояние, действие)
    return data

def train_model():
    model = DroneAI()
    data = generate_training_data()  # Генерация обучающих данных
    model.train_model(data)  # Тренировка модели
    model.save('models/drone_model.pth')  # Сохранение обученной модели

