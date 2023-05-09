import random
import time

# list of city abbreviations in europe
cities = ["LON","AMS","BER","PAR","BRU","FRA","COL","LYO","MIL","ROM","MAD","BAR"]

distances = {
    ('AMS', 'BRU'): [48], 
    ('AMS', 'COL'): [40],    
    ('AMS', 'BER'): [235],  
    ('BAR', 'MAD'): [98],   
    ('BAR', 'PAR'): [400],    
    ('BAR', 'LYO'): [320],
    ('BER', 'FRA'): [125],
    ('BRU', 'PAR'): [80],
    ('COL','FRA'): [40],  
    ('FRA', 'PAR'): [34], 
    ('FRA', 'MIL'): [240],
    ('LON', 'PAR'): [98],
    ('LYO', 'PAR'): [185], 
    ('LYO', 'MIL'): [180], 
    ('MAD', 'PAR'): [380], 
    ('MIL', 'ROM'): [125]

}

# Set default value for missing edges
default_cost = 1000

for city1 in cities:
    for city2 in cities:
        if (city1, city2) not in distances:
            distances[(city1, city2)] = [default_cost]

# Define chromosome representation
def create_chromosome(cities):
    chromosome = random.choices(cities, len(cities))
    return chromosome

# Define fitness function
def calculate_fitness(chromosome, distances):
    total_distance = 0
    for i in range(len(chromosome) - 1):
        city1, city2 = chromosome[i], chromosome[i + 1]

        total_distance += distances[(city1, city2)][0]
        #print(total_distance)
    return total_distance if total_distance != 0 else float('inf')

# Define selection operator
def tournament_selection(population, k):
    tournament = random.sample(population, k)
    return max(tournament, key=lambda chromosome: chromosome['fitness'])

def order_crossover(parent1, parent2):
    size = len(parent1)
    a, b = random.sample(range(size), 2)
    if a > b:
        a, b = b, a
    mask = set(parent1[a:b+1])
    child = [-1] * size
    for i in range(a, b + 1):
        child[i] = parent1[i]
    j = 0
    for i in range(size):
        if parent2[i] not in mask:
            while child[j] != -1:
                if j+1 == size:
                    break
                j += 1
            child[j] = parent2[i]
    return child

# Define mutation operator
def swap_mutation(chromosome):
    size = len(chromosome)
    a, b = random.sample(range(size), 2)
    chromosome[a], chromosome[b] = chromosome[b], chromosome[a]
    return chromosome

# Initialize population
population_size = 1000
population = [{'chromosome': create_chromosome(cities)} for _ in range(population_size)]

# Run the genetic algorithm
num_generations = 10000
k = 4 # tournament size
crossover_rate = 0.5
mutation_rate = 0.5

for generation in range(num_generations):
    # Evaluate fitness
    for individual in population:
        individual['fitness'] = calculate_fitness(individual['chromosome'], distances)

    # Sort population by fitness
    population.sort(key=lambda individual: individual['fitness'], reverse=True)

    # Print best fitness in current generation
    best_fitness = population[0]['fitness']
    print(f"Generation {generation + 1}: best fitness = {best_fitness}")

    # Select parents and generate offspring
    offspring = []
    for i in range(int(population_size / 2)):
        parent1 = tournament_selection(population, k)['chromosome']
        parent2 = tournament_selection(population, k)['chromosome']
        if random.random() < crossover_rate:
            child1 = {'chromosome': order_crossover(parent1, parent2)}
            child2 = {'chromosome': order_crossover(parent2, parent1)}
        else:
            child1 = {'chromosome': parent1}
            child2 = {'chromosome': parent2}
        if random.random() < mutation_rate:
            child1['chromosome'] = swap_mutation(child1['chromosome'])
        if random.random() < mutation_rate:
            child2['chromosome'] = swap_mutation(child2['chromosome'])
        offspring.extend([child1, child2])

    # Evaluate offspring fitness
    for individual in offspring:
        individual['fitness'] = calculate_fitness(individual['chromosome'], distances)

    # Replace 80 least fit individuals with offspring
    population[-500:] = offspring[-500:]

# Print best solution
best_chromosome = population[0]['chromosome']
best_fitness = population[0]['fitness']
print(f"Best solution: {best_chromosome}, best fitness: {best_fitness}")