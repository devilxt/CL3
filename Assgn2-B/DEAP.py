!pip install deap
import random
from deap import base, creator, tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)

# Structure initializers: Create an individual consisting of 100 random booleans
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)

# Create a population consisting of a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    """Fitness function: Returns the sum of the list (number of 1s)."""
    # DEAP requires fitness values to be returned as an iterable (tuple), hence the comma!
    return sum(individual),

# Register our evaluate function
toolbox.register("evaluate", evaluate)

# Register the genetic operators from DEAP's built-in tools
toolbox.register("mate", tools.cxTwoPoint)                            # Two-point crossover
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)              # Bit-flip mutation (5% chance per bit)
toolbox.register("select", tools.selTournament, tournsize=3)          # Tournament selection

def main():
    pop = toolbox.population(n=50)
    
    # CXPB  = probability with which two individuals are crossed
    # MUTPB = probability for mutating an individual
    # NGEN  = number of generations
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    
    print("Starting Evolution...")
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
        
    # Begin the generational loop
    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        
        offspring = list(map(toolbox.clone, offspring))
        
        # Apply Crossover
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values # Invalidate fitness since genes changed
                del child2.fitness.values
                
        # Apply Mutation
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values # Invalidate fitness since genes changed
                
        # Evaluate the individuals with an invalid (changed) fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        best_fit = max(fits)
        print(f"Generation {g:02d}: Best Fitness = {best_fit}/100")
        
        # Early stopping if we hit the perfect score
        if best_fit == 100:
            print("\nOptimal solution found early!")
            break

    print("\n-- End of evolution --")
    # Retrieve the best individual
    best_ind = tools.selBest(pop, 1)[0]
    print(f"Best individual fitness: {best_ind.fitness.values[0]}")

if __name__ == "__main__":
    main()
