import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

def add_custom_css():
    """
    Add custom CSS styling to the Streamlit app.
    """
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #e6f0ff;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1f77b4 !important;
            color: white !important;
        }
        .result-card {
            background-color: white;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def compare_results(results):
    """
    Compare multiple optimization results.
    
    Parameters:
        results (list): List of optimization result dictionaries
        
    Returns:
        pd.DataFrame: DataFrame with comparison data
    """
    if not results:
        return None
    
    # Extract data for comparison
    algorithms = [r['algorithm'] for r in results]
    makespans = [r['makespan'] for r in results]
    times = [r['execution_time'] for r in results]
    instances = [r['instance'] for r in results]
    jobs = [r['jobs'] for r in results]
    machines = [r['machines'] for r in results]
    
    # Create a DataFrame for comparison
    df_comparison = pd.DataFrame({
        'Algorithm': algorithms,
        'Instance': instances,
        'Makespan': makespans,
        'Execution Time (s)': times,
        'Jobs': jobs,
        'Machines': machines
    })
    
    return df_comparison

def save_result(result, file_format='json'):
    """
    Save an optimization result to a file.
    
    Parameters:
        result (dict): The optimization result to save
        file_format (str): Format to save the result in ('json' or 'csv')
        
    Returns:
        str: Path to the saved file
    """
    # Create a directory for results if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Generate a filename based on algorithm, instance and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"results/{result['algorithm']}_{result['instance']}_{timestamp}"
    
    if file_format.lower() == 'json':
        filename = f"{base_filename}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
    elif file_format.lower() == 'csv':
        filename = f"{base_filename}.csv"
        
        # Convert result to a format suitable for CSV
        # We'll create multiple CSV tables for different aspects
        
        # Main results
        main_data = {
            'algorithm': [result['algorithm']],
            'instance': [result['instance']],
            'makespan': [result['makespan']],
            'execution_time': [result['execution_time']],
            'jobs': [result['jobs']],
            'machines': [result['machines']],
            'timestamp': [result['timestamp']]
        }
        main_df = pd.DataFrame(main_data)
        main_df.to_csv(filename, index=False)
        
        # Save solution sequence
        solution_filename = f"{base_filename}_solution.csv"
        solution_df = pd.DataFrame({'job_sequence': result['solution']})
        solution_df.to_csv(solution_filename, index=False)
        
        # Save convergence data
        conv_filename = f"{base_filename}_convergence.csv"
        conv_df = pd.DataFrame(result['convergence_data'])
        conv_df.to_csv(conv_filename, index=False)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")
    
    return filename

def load_saved_results(directory='results'):
    """
    Load all saved results from the results directory.
    
    Parameters:
        directory (str): Directory containing saved results
        
    Returns:
        list: List of result dictionaries
    """
    if not os.path.exists(directory):
        return []
    
    results = []
    
    # Load all JSON result files
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as f:
                    result = json.load(f)
                    results.append(result)
            except Exception as e:
                st.warning(f"Error loading {filepath}: {e}")
    
    return results

def format_time(seconds):
    """
    Format a time in seconds to a human-readable string.
    
    Parameters:
        seconds (float): Time in seconds
        
    Returns:
        str: Formatted time string
    """
    if seconds < 0.001:
        return f"{seconds*1000:.2f} μs"
    elif seconds < 1:
        return f"{seconds*1000:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    else:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes} min {seconds:.2f} s"