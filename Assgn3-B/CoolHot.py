import collections
weather_data = [
    "2001,01,15,32.0",
    "2001,02,20,35.0",
    "2001,08,11,33.5",
    "2002,03,10,28.0",
    "2002,04,12,40.0",
    "2002,11,05,34.6",
    "2003,06,01,25.0",
    "2003,07,15,22.0",
    "2003,12,25,18.5"
]

def mapper(data_lines):
    """
    Simulates the Mapper: Reads input lines, extracts Year and Temp, 
    and emits them as (Key, Value) pairs.
    """
    mapped_data = []
    for line in data_lines:
        fields = line.split(",")
        # Ensure the row has the correct number of columns
        if len(fields) == 4:
            year = fields[0]
            temp = float(fields[3])
            mapped_data.append((year, temp))
            
    return mapped_data

def shuffle_and_sort(mapped_data):
    """
    Simulates Hadoop's internal Shuffle/Sort: Groups all emitted values 
    by their Key (Year).
    """
    grouped_data = collections.defaultdict(list)
    for year, temp in mapped_data:
        grouped_data[year].append(temp)
        
    return grouped_data

def reducer(grouped_data):
    """
    Simulates the Reducer: Takes the grouped data, calculates the average 
    temperature per year, and emits the final (Key, Value) pairs.
    """
    reduced_data = {}
    for year, temps in grouped_data.items():
        # Calculate average
        avg_temp = sum(temps) / len(temps)
        reduced_data[year] = avg_temp
        
    return reduced_data

if __name__ == "__main__":
    print("Starting Distributed MapReduce Simulation...\n")
    
    # Step 1: Map
    print("-> Running Map Phase...")
    mapped = mapper(weather_data)
    
    # Step 2: Shuffle & Sort
    print("-> Running Shuffle & Sort Phase...")
    grouped = shuffle_and_sort(mapped)
    
    # Step 3: Reduce
    print("-> Running Reduce Phase...")
    final_yearly_averages = reducer(grouped)
    
    # Print the direct MapReduce output
    print("\n--- MapReduce Output (Yearly Averages) ---")
    for year, avg in final_yearly_averages.items():
        print(f"Year {year}: {avg:.2f}°C")

    # Step 4: Post-Processing (Finding Hottest/Coolest)
    # Find the key (year) with the maximum and minimum average values
    hottest_year = max(final_yearly_averages, key=final_yearly_averages.get)
    coolest_year = min(final_yearly_averages, key=final_yearly_averages.get)

    print("\n--- Final Analysis ---")
    print(f"Hottest Year: {hottest_year} (Avg: {final_yearly_averages[hottest_year]:.2f}°C)")
    print(f"Coolest Year: {coolest_year} (Avg: {final_yearly_averages[coolest_year]:.2f}°C)")