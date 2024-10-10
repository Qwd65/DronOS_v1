import torch
import torch.nn as nn
import torch.optim as optim

class DroneAI:
    def __init__(self):
        self.model = nn.Sequential(
            nn.Linear(10, 128),
            nn.ReLU(),
            nn.Linear(128, 5)  # 5 возможных дронов
        )
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()

    def control_drones(self, drones, intruders):
        # Обработка состояния и решение
        state = self.get_state(drones, intruders)
        action = self.model(torch.tensor(state, dtype=torch.float32))
        return action

    def get_state(self, drones, intruders):
        # Получение состояния дронов и нарушителей
        return [drone.position[0] for drone in drones] + [intruder.position[0] for intruder in intruders]

    def train_model(self, data):
        for epoch in range(100):
            for state, target in data:
                prediction = self.model(torch.tensor(state, dtype=torch.float32))
                loss = self.criterion(prediction, torch.tensor(target, dtype=torch.float32))
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            print(f"Epoch {epoch}: Loss = {loss.item()}")

