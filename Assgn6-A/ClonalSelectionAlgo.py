import random

POPULATION_SIZE = 20
GENOME_LENGTH = 15      # Length of our antibody (target is all 1s)
GENERATIONS = 50
SELECTION_SIZE = 5      # How many top antibodies to select for cloning
CLONES_PER_ANTIBODY = 4 # How many clones each selected antibody gets

def create_antibody():
    """Initialization: Generates a random sequence of 0s and 1s."""
    return [random.randint(0, 1) for _ in range(GENOME_LENGTH)]

def calculate_affinity(antibody):
    """Affinity Function: Counts the number of 1s (closer to all 1s = higher affinity)."""
    return sum(antibody)

def hypermutate(clone, affinity, max_possible_affinity):
    """
    Hypermutation: Introduces random mutations. 
    Crucial concept: Higher affinity = lower mutation rate (we don't want to ruin good solutions).
    """
    mutation_rate = 1.0 - (affinity / max_possible_affinity)
    
    mutation_rate = mutation_rate * 0.20 
    
    mutated_clone = list(clone)
    for i in range(len(mutated_clone)):
        if random.random() < mutation_rate:
            mutated_clone[i] = 1 if mutated_clone[i] == 0 else 0
            
    return mutated_clone

def run_clonalg():
    print(f"Goal: Evolve an antibody of length {GENOME_LENGTH} to be all 1s.\n")
    
    # 1. Initialization
    population = [create_antibody() for _ in range(POPULATION_SIZE)]
    
    for generation in range(GENERATIONS):
        # 2. Evaluation
        affinities = [calculate_affinity(ab) for ab in population]
        
        best_affinity = max(affinities)
        best_antibody = population[affinities.index(best_affinity)]
        
        print(f"Generation {generation:02d} | Best Affinity: {best_affinity}/{GENOME_LENGTH} | Best Antibody: {best_antibody}")
        
        if best_affinity == GENOME_LENGTH:
            print("\nPerfect antibody evolved! Infection neutralized.")
            break
            
        # Combine population and affinities for easy sorting
        pop_with_aff = list(zip(population, affinities))
        # Sort descending based on affinity
        pop_with_aff.sort(key=lambda x: x[1], reverse=True)
        
        # 3. Selection
        selected_antibodies = [item[0] for item in pop_with_aff[:SELECTION_SIZE]]
        
        clones_pool = []
        
        # 4. Cloning & 5. Hypermutation
        for ab in selected_antibodies:
            current_affinity = calculate_affinity(ab)
            for _ in range(CLONES_PER_ANTIBODY):
                # Clone it
                clone = list(ab)
                # Mutate it based on its current affinity
                mutated_clone = hypermutate(clone, current_affinity, GENOME_LENGTH)
                clones_pool.append(mutated_clone)
                
        # 6. Evaluation (of the new clones)
        clones_affinities = [calculate_affinity(clone) for clone in clones_pool]
        
        # Combine original population and mutated clones
        all_candidates = population + clones_pool
        all_affinities = affinities + clones_affinities
        
        combined_pop_with_aff = list(zip(all_candidates, all_affinities))
        combined_pop_with_aff.sort(key=lambda x: x[1], reverse=True)
        
        # 7. Selection and Replacement
        # Take the top 'POPULATION_SIZE' individuals to form the next generation
        population = [item[0] for item in combined_pop_with_aff[:POPULATION_SIZE]]

if __name__ == "__main__":
    run_clonalg()