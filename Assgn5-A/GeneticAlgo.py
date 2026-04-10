import random

POPULATION_SIZE = 10
GENOME_LENGTH = 12
GENERATIONS = 50
MUTATION_RATE = 0.1

TARGET_GENOME = [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1]

def create_individual():
    """Initialization: Generates a random sequence of 0s and 1s."""
    return [random.randint(0, 1) for _ in range(GENOME_LENGTH)]

def calculate_fitness(individual):
    """Evaluation: Calculates how close the individual is to the target."""
    fitness = 0
    for i in range(GENOME_LENGTH):
        if individual[i] == TARGET_GENOME[i]:
            fitness += 1
    return fitness

def select_parents(population, fitnesses):
    """Selection: Chooses parents based on higher fitness (Tournament Selection)."""
    # Pick 3 random individuals and return the one with the best fitness
    tournament = random.sample(list(zip(population, fitnesses)), 3)
    best_parent = max(tournament, key=lambda item: item[1])[0]
    return best_parent

def crossover(parent1, parent2):
    """Crossover: Single-Point Crossover exchanging tails of chromosomes."""
    # The mating chromosomes are cut once at corresponding points and exchanged 
    point = random.randint(1, GENOME_LENGTH - 1)
    
    head1, tail1 = parent1[:point], parent1[point:]
    head2, tail2 = parent2[:point], parent2[point:]
    
    offspring1 = head1 + tail2
    offspring2 = head2 + tail1
    
    return offspring1, offspring2

def mutate(individual):
    """Mutation: Randomly flips bits to maintain diversity."""
    # Mutation of a bit involves flipping a bit, changing 0 to 1 and vice-versa 
    for i in range(GENOME_LENGTH):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 if individual[i] == 0 else 0
    return individual

# ==========================================
# MAIN GA LOOP
# ==========================================
def run_genetic_algorithm():
    print(f"TARGET TO FIND: {TARGET_GENOME}\n")
    
    # 1. Initialization [cite: 506]
    population = [create_individual() for _ in range(POPULATION_SIZE)]
    
    for generation in range(GENERATIONS):
        # 2. Evaluation [cite: 507]
        fitnesses = [calculate_fitness(ind) for ind in population]
        
        # Check if we found the perfect solution early
        best_fitness = max(fitnesses)
        best_individual = population[fitnesses.index(best_fitness)]
        
        print(f"Gen {generation:02d} | Best Fitness: {best_fitness}/{GENOME_LENGTH} | Best Genome: {best_individual}")
        
        if best_fitness == GENOME_LENGTH:
            print("\nOptimal solution found! Stopping criteria met.")
            break
            
        new_population = []
        
        # Create the next generation
        for _ in range(POPULATION_SIZE // 2):
            # 3. Selection [cite: 510]
            parent1 = select_parents(population, fitnesses)
            parent2 = select_parents(population, fitnesses)
            
            # 4. Crossover [cite: 512]
            child1, child2 = crossover(parent1, parent2)
            
            # 5. Mutation [cite: 515]
            child1 = mutate(child1)
            child2 = mutate(child2)
            
            # 6. Replacement [cite: 511]
            new_population.extend([child1, child2])
            
        population = new_population

if __name__ == "__main__":
    run_genetic_algorithm()