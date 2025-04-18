import numpy as np
import os

def load_instance(instance_name):
    """
    Load a flowshop instance from a text file.
    
    Parameters:
        instance_name (str): Name of the instance to load (e.g., "tai20_5")
        
    Returns:
        tuple: (num_jobs, num_machines, processing_times)
    """
    # Map instance names to file names (adjust according to your file naming convention)
    instance_file_map = {
        "tai20_5_1": "20_5_1.txt",
        "tai20_5_2": "20_5_2.txt",
        "tai20_10_1": "20_10_1.txt",
        "tai20_10_2": "20_10_2.txt",
        "tai20_20_1": "20_20_1.txt",
        "tai20_20_2": "20_20_2.txt",
        "tai50_10_1": "50_10_1.txt",
        "tai50_10_2": "50_10_2.txt",
        "tai50_20_1": "50_20_1.txt",
        "tai50_20_2": "50_20_2.txt",
    }
    
    # Get file path for the requested instance
    file_name = instance_file_map.get(instance_name)
    if file_name is None:
        # Default to a small instance if not found
        return 10, 5, np.random.randint(1, 100, size=(10, 5))
    
    file_path = os.path.join("data", file_name)
    
    try:
        # Try to read the file
        with open(file_path, 'r') as f:
            # Read first line containing number of jobs and machines
            first_line = f.readline().strip().split()
            n_jobs = int(first_line[0])
            n_machines = int(first_line[1])
            
            # Read processing times
            processing_times = []
            for _ in range(n_machines):
                line = f.readline().strip().split()
                processing_times.append([int(x) for x in line])
            
            # Convert to numpy array and transpose to get job-machine format
            processing_times = np.array(processing_times).T
            
        return n_jobs, n_machines, processing_times
    
    except (FileNotFoundError, IOError) as e:
        print(f"Error loading instance {instance_name} from file {file_path}: {e}")
        # Return a smaller random instance as fallback
        return 10, 5, np.random.randint(1, 100, size=(10, 5))
    

def export_to_csv(result):
    """
    Export the optimization result to a CSV file.
    
    Parameters:
        result (dict): The optimization result to export
        
    Returns:
        str: Path to the exported file
    """
    # This is a placeholder for the export functionality
    # In a real implementation, you would create and save a CSV file
    return "results.csv"

def export_to_json(result):
    """
    Export the optimization result to a JSON file.
    
    Parameters:
        result (dict): The optimization result to export
        
    Returns:
        str: Path to the exported file
    """
    # This is a placeholder for the export functionality
    # In a real implementation, you would create and save a JSON file
    return "results.json"

def get_available_instances():
    """
    Get the list of available benchmark instances.
    
    Returns:
        list: List of instance names
    """
    return [
        "tai20_5_1",
        "tai20_5_2",
        "tai20_10_1",
        "tai20_10_2",
        "tai20_20_1",
        "tai20_20_2",
        "tai50_10_1",
        "tai50_10_2",
        "tai50_20_1",
        "tai50_20_2",
    ]

def get_algorithm_options():
    """
    Get the list of available optimization algorithms.
    
    Returns:
        list: List of algorithm names
    """
    return [
        "NEH Heuristic",
        "Local Search",
        "Iterated Local Search",
        "Simulated Annealing",
        "Genetic Algorithm",
        "Tabu Search",
        "Ant Colony Optimization",
        "Particle Swarm Optimization"
    ]