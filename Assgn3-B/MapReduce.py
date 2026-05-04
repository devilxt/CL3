import csv
import collections

def mapper(file_path):
    """
    Simulates the Mapper: Reads input from a CSV file, extracts Year and Temp, 
    and emits them as (Key, Value) pairs.
    """
    mapped_data = []
    
    # Open and read the CSV file
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row ("Date", "Temp")
        
        for row in csv_reader:
            # Ensure the row has at least 2 columns (Date and Temp)
            if len(row) >= 2:
                date_str = row[0].strip()
                temp_str = row[1].strip()
                
                try:
                    # Assuming standard date format (e.g., 2002-04-15 or 2002-04)
                    # Extract the first 4 characters for the Year
                    year = date_str[:4] 
                    temp = float(temp_str)
                    
                    mapped_data.append((year, temp))
                except ValueError:
                    # If there's blank data or text in the temp column, skip that row
                    continue
                    
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
        avg_temp = sum(temps) / len(temps)
        reduced_data[year] = avg_temp
        
    return reduced_data

if __name__ == "__main__":
    # Make sure this matches the name of your saved CSV file
    csv_file_name = "temperature.csv" 

    
    print(f"Starting Distributed MapReduce Simulation using {csv_file_name}...\n")
    
    print("-> Running Map Phase...")
    try:
        mapped = mapper(csv_file_name)
        
        print("-> Running Shuffle & Sort Phase...")
        grouped = shuffle_and_sort(mapped)
        
        print("-> Running Reduce Phase...")
        final_yearly_averages = reducer(grouped)
        
        print("\n--- MapReduce Output (Yearly Averages) ---")
        for year, avg in final_yearly_averages.items():
            print(f"Year {year}: {avg:.2f}°C")
            
        if final_yearly_averages:
            hottest_year = max(final_yearly_averages, key=final_yearly_averages.get)
            coolest_year = min(final_yearly_averages, key=final_yearly_averages.get)

            print("\n--- Final Analysis ---")
            print(f"Hottest Year: {hottest_year} (Avg: {final_yearly_averages[hottest_year]:.2f}°C)")
            print(f"Coolest Year: {coolest_year} (Avg: {final_yearly_averages[coolest_year]:.2f}°C)")
        else:
            print("\nNo valid data found to analyze.")
            
    except FileNotFoundError:
        print(f"\nError: Could not find the file '{csv_file_name}'. Please ensure it is in the same folder as this script.")