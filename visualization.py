import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def visualize_schedule(result):
    """
    Create a Gantt chart visualization of the flowshop schedule.
    
    Parameters:
        result (dict): The optimization result containing schedule information
        
    Returns:
        plotly.graph_objects.Figure: Gantt chart figure
    """
    # Extract data from result
    jobs = result['jobs']
    machines = result['machines']
    solution = result['solution']
    
    # Create a basic Gantt chart data
    gantt_data = []
    current_times = [0] * machines
    
    # Process each job in the solution order
    for job_idx in solution:
        job_id = job_idx  # Job ID is 1-based in this simulation
        
        # For each machine
        for machine_id in range(machines):
            # Simulated processing time (would be from your actual data)
            proc_time = np.random.randint(5, 20)
            
            # Start time depends on when previous job on this machine finished
            # and when this job finished on previous machine
            start_time = current_times[machine_id]
            if machine_id > 0:
                start_time = max(start_time, current_times[machine_id-1])
            
            # End time
            end_time = start_time + proc_time
            
            # Update current time for this machine
            current_times[machine_id] = end_time
            
            # Add to Gantt data
            gantt_data.append({
                'Job': f'Job {job_id}',
                'Machine': f'Machine {machine_id+1}',
                'Start': start_time,
                'Finish': end_time,
                'Duration': proc_time
            })
    
    # Create a DataFrame for the Gantt chart
    df_gantt = pd.DataFrame(gantt_data)
    
    # Create the Gantt chart using Plotly
    fig = px.timeline(
        df_gantt, 
        x_start='Start', 
        x_end='Finish', 
        y='Machine',
        color='Job',
        title=f"Machine Schedule for {result['algorithm']} on {result['instance']}",
        labels={"Machine": "Machine", "Start": "Time", "Finish": "Time"}
    )
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Machine",
        legend_title="Jobs",
        height=400,
    )
    
    return fig

def create_convergence_plot(convergence_data):
    """
    Create a line plot showing the algorithm's convergence.
    
    Parameters:
        convergence_data (list): List of dictionaries with iteration and makespan values
        
    Returns:
        plotly.graph_objects.Figure: Convergence plot figure
    """
    df_conv = pd.DataFrame(convergence_data)
    fig = px.line(
        df_conv, 
        x='iteration', 
        y='makespan',
        title="Algorithm Convergence",
        labels={"iteration": "Iteration", "makespan": "Makespan"}
    )
    fig.update_layout(height=300)
    return fig

def create_machine_utilization_chart(machine_utilization):
    """
    Create a bar chart showing machine utilization.
    
    Parameters:
        machine_utilization (list): List of utilization percentages for each machine
        
    Returns:
        plotly.graph_objects.Figure: Machine utilization bar chart
    """
    machine_data = pd.DataFrame({
        'Machine': [f"Machine {i+1}" for i in range(len(machine_utilization))],
        'Utilization (%)': machine_utilization
    })
    
    fig = px.bar(
        machine_data,
        x='Machine',
        y='Utilization (%)',
        title='Machine Utilization',
        color='Utilization (%)',
        color_continuous_scale='Viridis'
    )
    
    return fig

def create_job_completion_chart(job_completion):
    """
    Create a bar chart showing job completion times.
    
    Parameters:
        job_completion (list): List of completion times for each job
        
    Returns:
        plotly.graph_objects.Figure: Job completion bar chart
    """
    job_data = pd.DataFrame({
        'Job': [f"Job {i+1}" for i in range(len(job_completion))],
        'Completion Time': job_completion
    })
    
    # Sort by completion time for better visualization
    job_data = job_data.sort_values('Completion Time')
    
    fig = px.bar(
        job_data,
        x='Job',
        y='Completion Time',
        title='Job Completion Times',
        color='Completion Time',
        color_continuous_scale='Viridis'
    )
    
    return fig

def create_performance_scatter_plot(comparison_df):
    """
    Create a scatter plot comparing makespan vs execution time for different algorithms.
    
    Parameters:
        comparison_df (pd.DataFrame): DataFrame with algorithm performance data
        
    Returns:
        plotly.graph_objects.Figure: Performance scatter plot
    """
    # Create a scatter plot of makespan vs execution time
    fig = px.scatter(
        comparison_df,
        x='Execution Time (s)',
        y='Makespan',
        color='Algorithm',
        symbol='Instance',
        size='Jobs',
        hover_data=['Machines'],
        title='Makespan vs Execution Time (Lower values in both axes are better)',
        height=500
    )
    
    # Add quadrant lines (using median values as boundaries)
    med_makespan = comparison_df['Makespan'].median()
    med_time = comparison_df['Execution Time (s)'].median()
    
    fig.add_shape(
        type="line", line=dict(dash="dash", width=1, color="gray"),
        x0=comparison_df['Execution Time (s)'].min(), 
        y0=med_makespan,
        x1=comparison_df['Execution Time (s)'].max(), 
        y1=med_makespan
    )
    
    fig.add_shape(
        type="line", line=dict(dash="dash", width=1, color="gray"),
        x0=med_time, 
        y0=comparison_df['Makespan'].min(),
        x1=med_time, 
        y1=comparison_df['Makespan'].max()
    )
    
    # Add quadrant annotations
    fig.add_annotation(
        x=med_time * 0.5, 
        y=med_makespan * 0.9,
        text="Best Performance",
        showarrow=False,
        font=dict(size=12, color="green")
    )
    
    fig.add_annotation(
        x=med_time * 1.5, 
        y=med_makespan * 1.1,
        text="Worst Performance",
        showarrow=False,
        font=dict(size=12, color="red")
    )
    
    return fig

def create_makespan_comparison_chart(comparison_df):
    """
    Create a bar chart comparing makespan values for different algorithms.
    
    Parameters:
        comparison_df (pd.DataFrame): DataFrame with algorithm performance data
        
    Returns:
        plotly.graph_objects.Figure: Makespan comparison bar chart
    """
    fig = px.bar(
        comparison_df,
        x='Algorithm',
        y='Makespan',
        color='Instance',
        barmode='group',
        title='Makespan Comparison (Lower is Better)',
        height=400
    )
    
    return fig

def create_execution_time_comparison_chart(comparison_df):
    """
    Create a bar chart comparing execution times for different algorithms.
    
    Parameters:
        comparison_df (pd.DataFrame): DataFrame with algorithm performance data
        
    Returns:
        plotly.graph_objects.Figure: Execution time comparison bar chart
    """
    fig = px.bar(
        comparison_df,
        x='Algorithm',
        y='Execution Time (s)',
        color='Instance',
        barmode='group',
        title='Execution Time Comparison (Lower is Better)',
        height=400
    )
    
    return fig