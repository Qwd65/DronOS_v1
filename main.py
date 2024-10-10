from game.game_manager import GameManager
from ai.drone_ai import DroneAI
from ai.train import train_model

def main():
    mode = input("Выберите режим игры (player/ai/train): ")

    if mode == 'train':
        # Запуск обучения нейросети
        train_model()
    else:
        game = GameManager(mode=mode)
        game.run()

if __name__ == '__main__':
    main()

