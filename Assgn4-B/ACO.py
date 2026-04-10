import numpy as np
import random

distances = np.array([
    [0.0, 2.0, 9.0, 10.0, 7.0],
    [2.0, 0.0, 6.0, 4.0,  3.0],
    [9.0, 6.0, 0.0, 8.0,  2.0],
    [10.0, 4.0, 8.0, 0.0,  5.0],
    [7.0, 3.0, 2.0, 5.0,  0.0]
])

num_cities = len(distances)

num_ants = 10               # Number of ants exploring per iteration
num_iterations = 50         # Total number of iterations
alpha = 1.0                 # Importance of pheromone trail
beta = 2.0                  # Importance of distance (heuristic)
evaporation_rate = 0.5      # Rate at which pheromones disappear
Q = 100                     # Total pheromone left on path by one ant

# Initialize pheromones to 1 on all paths
pheromones = np.ones((num_cities, num_cities))

def calculate_path_length(path):
    """Calculates the total distance of a given tour, returning to start."""
    length = 0
    for i in range(len(path) - 1):
        length += distances[path[i]][path[i+1]]
    # Add distance to return to the starting city
    length += distances[path[-1]][path[0]] 
    return length

def construct_path(start_city):
    """An ant constructs a complete tour probabilistically."""
    path = [start_city]
    visited = set([start_city])

    while len(path) < num_cities:
        current_city = path[-1]
        probabilities = []

        # Calculate probability for moving to each unvisited city
        for next_city in range(num_cities):
            if next_city not in visited:
                # Formula: (Pheromone^alpha) * ((1/Distance)^beta)
                pheromone = pheromones[current_city][next_city] ** alpha
                heuristic = (1.0 / distances[current_city][next_city]) ** beta
                probabilities.append(pheromone * heuristic)
            else:
                probabilities.append(0)

        # Normalize probabilities so they sum to 1
        total_prob = sum(probabilities)
        probabilities = [p / total_prob for p in probabilities]

        # Roulette wheel selection based on calculated probabilities
        next_city = random.choices(range(num_cities), weights=probabilities)[0]
        path.append(next_city)
        visited.add(next_city)

    return path

def run_aco():
    best_path = None
    best_length = float('inf')

    print("Running Ant Colony Optimization...\n")

    for iteration in range(num_iterations):
        all_paths = []
        all_lengths = []

        # Step A: Ants construct paths
        for ant in range(num_ants):
            start_city = random.randint(0, num_cities - 1)
            path = construct_path(start_city)
            length = calculate_path_length(path)

            all_paths.append(path)
            all_lengths.append(length)

            # Keep track of the all-time best path
            if length < best_length:
                best_length = length
                best_path = path

        # Step B: Evaporate pheromones on all paths
        global pheromones
        pheromones *= (1.0 - evaporation_rate)

        # Step C: Deposit new pheromones based on path quality
        for path, length in zip(all_paths, all_lengths):
            pheromone_to_deposit = Q / length
            for i in range(num_cities - 1):
                pheromones[path[i]][path[i+1]] += pheromone_to_deposit
                pheromones[path[i+1]][path[i]] += pheromone_to_deposit # Paths are symmetric
            
            # Return trip pheromones
            pheromones[path[-1]][path[0]] += pheromone_to_deposit
            pheromones[path[0]][path[-1]] += pheromone_to_deposit

        # Print progress every 10 iterations
        if iteration % 10 == 0:
            print(f"Iteration {iteration:02d} | Best Length: {best_length:.2f} | Path: {best_path}")

    print("\n" + "="*30)
    print("--- Final Optimization Result ---")
    print(f"Shortest Path Found: {best_path} (Returns to {best_path[0]})")
    print(f"Minimum Distance:    {best_length:.2f}")
    print("="*30)

if __name__ == "__main__":
    run_aco()