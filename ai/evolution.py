import numpy as np
import random
from ai.drone_ai import DroneAI

class Evolution:
    def __init__(self, population_size=20, mutation_rate=0.01):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [DroneAI() for _ in range(population_size)]

    def evolve(self, generations, training_data):
        for generation in range(generations):
            print(f"Generation {generation+1}/{generations}")
            fitness_scores = self.evaluate_population(training_data)
            self.population = self.selection(fitness_scores)
            self.mutate_population()

    def evaluate_population(self, training_data):
        # Оценка популяции: запуск тренировки и получение результата
        fitness_scores = []
        for individual in self.population:
            score = individual.train_model(training_data)
            fitness_scores.append(score)
        return fitness_scores

    def selection(self, fitness_scores):
        # Отбор лучших особей
        selected_population = []
        sorted_population = [x for _, x in sorted(zip(fitness_scores, self.population), key=lambda pair: pair[0], reverse=True)]
        
        # Отбираем лучших 50% для размножения
        num_selected = len(sorted_population) // 2
        selected_population.extend(sorted_population[:num_selected])
        
        # Дублируем лучших особей
        selected_population.extend(random.choices(selected_population, k=self.population_size - num_selected))
        return selected_population

    def mutate_population(self):
        # Мутация: случайным образом изменяем параметры моделей
        for individual in self.population:
            if random.random() < self.mutation_rate:
                individual.mutate()


