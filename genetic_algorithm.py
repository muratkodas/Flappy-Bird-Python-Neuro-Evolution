import numpy as np
from bird import Bird


class Genetic_Algorithm:
    def __init__(self, simulation, neurons, population_lenght):
        self.simulation = simulation
        self.settings = self.simulation.settings
        
        # Parameters of the GE algorithm
        self.total_ratio = 1
        self.mutation_rate = 0.2
        
        self.population = []
        self.neurons = neurons #exp: np.matrix([[6], [10], [10], [3]])
        self.population_lenght_start = population_lenght
        self.population_lenght = self.population_lenght_start
        self.poputaliton_creation(self.population_lenght, self.neurons)
        
        
    def poputaliton_creation(self, population_lenght, neurons):
        for i in range(population_lenght):
            self.population.append(Bird(self.simulation, self.neurons))
    
    def Pool_Selection(self, fitness, score_mean):
        self.fitness = fitness
        self.score_mean = score_mean
        self.population_lenght_start = self.population_lenght
        
        # Creating new population by mating
        new_population = []
        self.parents_population = []
        self.population_copy = self.population_copier()

        for i in range(self.population_lenght):
            if self.population_lenght >= 1:
                parent_A = self.Parent_Selection() 
                parent_B = self.Parent_Selection()
                if parent_A and parent_B:
                    child = Bird(self.simulation, self.neurons)
                    child = self.Crossover(parent_A, parent_B, child)
                    child = self.Mutation(child, self.mutation_rate)
                    new_population.append(child)
            else:
                break

        # Checks if population has enough member. Adds with copied birds and new birds
        population_lack = self.population_lenght_start - len(new_population)
        if population_lack > 0:
            population_lack_random = np.random.randint(population_lack)
            for i in range(population_lack_random):
                new_population.append(self.population_copy[np.random.randint(self.population_lenght_start)])
            for i in range(population_lack-population_lack_random):
                new_population.append(Bird(self.simulation, self.neurons))
        # Updates the population with new population
        self.population = new_population
        self.population_lenght = self.population_lenght_start
        return self.population
    
    def population_copier(self):
        #Parent's population with initial game settings with same brain.
        population_copy  = []
        layers_lenght = len(self.population[0].brain.layers)
        for i in range(self.population_lenght):
            population_copy.append(Bird(self.simulation, self.neurons))
            for j in range(layers_lenght):
                population_copy[i].brain.layers[j].weights = self.population[i].brain.layers[j].weights
                population_copy[i].brain.layers[j].bias = self.population[i].brain.layers[j].bias
            
        return population_copy
    
    def Parent_Selection(self):
        #Select the parent by chance or by fitness
        if len(self.population) > 0:
            #select the parent bird by chance.
            chance = 0.4
            selection_chance = np.random.uniform(low=0, high=1)
            if selection_chance > chance:
                #select randomly if selection chance is bigger
                population_pos = np.random.randint(self.population_lenght)
            else:
                #if chance is not big, select the best one from the remeaning birds.
                population_pos = np.argmax(self.fitness)
                
            parent = self.population[population_pos]
            self.Incest_Blocker(population_pos)
            return parent
        
        else:
            return []
    
    def Incest_Blocker(self, population_pos):
        #incest blocker, delete the parent to prevent same agent mating
        self.parents_population.append(self.population[population_pos])
        self.population = np.delete(self.population, population_pos, 0 )
        self.fitness = np.delete(self.fitness, population_pos, 0 )
        self.population_lenght = len(self.population) # Update the number of the population after deleting
    
    def Crossover(self, parent_A, parent_B, child):
        # Combine parents' genetic info to the child
        layers_lenght = len(parent_A.brain.layers)
        for j in range(layers_lenght):
            selection_chance = np.random.uniform(low=0, high=1)
            if selection_chance > 0.5:
                child.brain.layers[j].weights = parent_A.brain.layers[j].weights
                child.brain.layers[j].bias = parent_A.brain.layers[j].bias
            else:
                child.brain.layers[j].weights = parent_B.brain.layers[j].weights
                child.brain.layers[j].bias = parent_B.brain.layers[j].bias   
        return child
    
    def Mutation(self,child, mutation_rate):
        # Apply mutation on the genetic material randomly
        self.mutation_rate = mutation_rate
        mutation_guess = np.random.rand(1)

        if mutation_guess <= self.mutation_rate:
            layer_weight_guess = np.random.randint(len(child.brain.layers))
            weight_guess_i = np.random.randint(np.shape(child.brain.layers[layer_weight_guess].weights)[0])
            weight_guess_j = np.random.randint(np.shape(child.brain.layers[layer_weight_guess].weights)[1])
            child.brain.layers[layer_weight_guess].weights[weight_guess_i, weight_guess_j] = np.random.uniform(low=0, high=1)
            
            layer_bias_guess = np.random.randint(len(child.brain.layers))
            bias_guess = np.random.randint(np.shape(child.brain.layers[layer_bias_guess].bias)[0])
            child.brain.layers[layer_bias_guess].weights[bias_guess, 0] = np.random.uniform(low=0, high=1)
            
        else:
            pass

        return child
