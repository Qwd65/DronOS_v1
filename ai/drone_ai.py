import torch
import torch.nn as nn
import torch.optim as optim

class DroneAI:
    def __init__(self):
        self.model = nn.Sequential(
            nn.Linear(20, 128),  # 10 координат (5 дронов) + 10 координат (5 нарушителей)
            nn.ReLU(),
            nn.Linear(128, 10)  # Выход для 5 дронов (каждый по X и Y координате)
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

    def get_state(self, drones, intruders):
        # Возвращаем состояния дронов и нарушителей в виде числового массива
        return [drone.position[0] for drone in drones] + [drone.position[1] for drone in drones] + \
               [intruder.position[0] for intruder in intruders] + [intruder.position[1] for intruder in intruders]

    def train_model(self, data):
        for epoch in range(100):
            for state, target in data:
                # Преобразуем кортеж состояния и действий в тензоры
                state_tensor = torch.tensor(state, dtype=torch.float32)
                target_tensor = torch.tensor(self.flatten_target(target), dtype=torch.float32)

                # Прогоняем через модель и вычисляем ошибку
                prediction = self.model(state_tensor)
                loss = self.criterion(prediction, target_tensor)

                # Обновляем веса модели
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            print(f"Epoch {epoch}: Loss = {loss.item()}")

    def flatten_target(self, target):
        # Преобразование целевых данных в массив чисел (убираем словари)
        return [value for action in target for value in action.values()]

    def save(self, path):
        torch.save(self.model.state_dict(), path)

