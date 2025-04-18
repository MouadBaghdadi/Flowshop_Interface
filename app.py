import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px

# Import from our custom modules
from data import load_instance
from algorithms import run_algorithm
from visualization import visualize_schedule
from utils import add_custom_css


# Set page configuration
st.set_page_config(
    page_title="Flowshop Scheduler Optimizer",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for black theme
st.markdown("""
<style>
    .stApp {
        background-color: black;
        color: white;
    }
    .stButton button {
        background-color: #333;
        color: white;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox, .stMultiselect {
        background-color: #333;
        color: white;
    }
    .stSidebar {
        background-color: #111;
    }
    div[data-testid="stMarkdownContainer"] {
        color: white;
    }
    .stDataFrame {
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# Add custom CSS for styling
add_custom_css()

# Initialize session state variables if they don't exist
if 'history' not in st.session_state:
    st.session_state.history = []
if 'comparison_data' not in st.session_state:
    st.session_state.comparison_data = []
if 'best_solution' not in st.session_state:
    st.session_state.best_solution = None

# App header
st.title("🏭 Flowshop Scheduler Optimizer")
st.markdown("Optimize job scheduling in a flowshop environment using various algorithms")

# Create tabs for different sections of the app
tab1, tab2, tab3 = st.tabs(["Run Optimization", "Results Analysis", "Algorithm Comparison"])

with tab1:
    st.header("Run Flowshop Optimization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Instance selection
        instance_options = [
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
        selected_instance = st.selectbox(
            "Select Flowshop Instance", 
            instance_options,
            help="Choose one of the benchmark instances to optimize"
        )
        
        # Display instance details
        jobs, machines, processing_times = load_instance(selected_instance)        
        st.info(f"Selected instance: {selected_instance} ({jobs} jobs × {machines} machines)")
        # show the processing times in a table make it
        st.write(processing_times)
    
    with col2:
        # Algorithm selection
        algorithm_options = [
            "NEH Heuristic",
            "Local Search",
            "Iterated Local Search",
            "Simulated Annealing",
            "Genetic Algorithm",
            "Tabu Search",
            "Ant Colony Optimization",
            "Particle Swarm Optimization"
        ]
        selected_algorithm = st.selectbox(
            "Select Optimization Algorithm", 
            algorithm_options,
            help="Choose which algorithm to use for solving the flowshop problem"
        )
    
    # Algorithm-specific parameters
    st.subheader("Algorithm Parameters")
    
    # Display different parameters based on the selected algorithm
    parameters = {}
    
    if selected_algorithm == "Local Search":
        col1, col2 = st.columns(2)
        with col1:
            parameters["neighborhood_type"] = st.selectbox(
                "Neighborhood Type",
                ["Swap", "Insert", "2-opt"]
            )
        with col2:
            parameters["max_iterations"] = st.number_input("Max Iterations", 10, 1000, 100)
    
    elif selected_algorithm == "Iterated Local Search":
        col1, col2, col3 = st.columns(3)
        with col1:
            parameters["perturbation"] = st.selectbox(
                "Perturbation Strength",
                ["Low", "Medium", "High"]
            )
        with col2:
            parameters["max_iterations"] = st.number_input("Max Iterations", 10, 1000, 100)
        with col3:
            parameters["acceptance_criterion"] = st.selectbox(
                "Acceptance Criterion",
                ["Better", "Always", "Temperature Based"]
            )
    
    elif selected_algorithm == "Simulated Annealing":
        col1, col2 = st.columns(2)
        with col1:
            parameters["initial_temp"] = st.slider("Initial Temperature", 100, 1000, 500)
            parameters["cooling_rate"] = st.slider("Cooling Rate", 0.7, 0.99, 0.95, 0.01)
        with col2:
            parameters["max_iterations"] = st.number_input("Max Iterations", 100, 5000, 1000)
            parameters["neighborhood"] = st.selectbox(
                "Neighborhood Type",
                ["Swap", "Insert", "Scramble"]
            )
    
    elif selected_algorithm == "Genetic Algorithm":
        col1, col2 = st.columns(2)
        with col1:
            parameters["population_size"] = st.slider("Population Size", 10, 200, 50)
            parameters["crossover_rate"] = st.slider("Crossover Rate", 0.5, 1.0, 0.8, 0.1)
        with col2:
            parameters["mutation_rate"] = st.slider("Mutation Rate", 0.01, 0.5, 0.2, 0.01)
            parameters["generations"] = st.number_input("Generations", 10, 500, 100)
            parameters["selection_method"] = st.selectbox(
                "Selection Method",
                ["Tournament", "Roulette Wheel", "Rank Based"]
            )
    
    elif selected_algorithm == "Tabu Search":
        col1, col2 = st.columns(2)
        with col1:
            parameters["tabu_size"] = st.slider("Tabu List Size", 5, 50, 20)
            parameters["max_iterations"] = st.number_input("Max Iterations", 50, 1000, 200)
        with col2:
            parameters["neighborhood"] = st.selectbox(
                "Neighborhood Type",
                ["Swap", "Insert", "Hybrid"]
            )
            parameters["aspiration"] = st.checkbox("Use Aspiration Criteria", True)
    
    elif selected_algorithm in ["Ant Colony Optimization", "Particle Swarm Optimization"]:
        col1, col2 = st.columns(2)
        with col1:
            parameters["population"] = st.slider("Population", 10, 100, 30)
            parameters["iterations"] = st.number_input("Iterations", 10, 500, 100)
        with col2:
            if selected_algorithm == "Ant Colony Optimization":
                parameters["pheromone_weight"] = st.slider("Pheromone Weight", 0.5, 3.0, 1.0, 0.1)
                parameters["evaporation_rate"] = st.slider("Evaporation Rate", 0.1, 0.9, 0.5, 0.1)
            else:  # PSO
                parameters["inertia"] = st.slider("Inertia Weight", 0.1, 1.0, 0.7, 0.1)
                parameters["cognitive"] = st.slider("Cognitive Weight", 0.5, 2.5, 1.5, 0.1)
                parameters["social"] = st.slider("Social Weight", 0.5, 2.5, 1.5, 0.1)
    
    # Run optimization button
    if st.button("Run Optimization", type="primary", use_container_width=True):
        with st.spinner(f"Running {selected_algorithm} on {selected_instance}..."):
            # Execute the selected algorithm
            result = run_algorithm(selected_algorithm, selected_instance, parameters)
            
            # Add result to history
            st.session_state.history.append(result)
            
            # Add to comparison data if not already present
            algorithm_instance_key = f"{selected_algorithm}_{selected_instance}"
            existing_keys = [f"{r['algorithm']}_{r['instance']}" for r in st.session_state.comparison_data]
            
            if algorithm_instance_key not in existing_keys:
                st.session_state.comparison_data.append(result)
            else:
                # Update existing entry
                idx = existing_keys.index(algorithm_instance_key)
                st.session_state.comparison_data[idx] = result
            
            # Check if this is the best solution found so far
            if (st.session_state.best_solution is None or 
                result['makespan'] < st.session_state.best_solution['makespan']):
                st.session_state.best_solution = result
            
            # Show success message
            st.success("Optimization completed successfully!")
            
            # Display result
            st.subheader("Optimization Result")
            
            # Create a nice results card
            st.markdown('<div class="result-card">', unsafe_allow_html=True)            
            res_col1, res_col2, res_col3 = st.columns(3)
            with res_col1:
                st.metric("Makespan", f"{result['makespan']}")
            with res_col2:
                st.metric("Execution Time", f"{result['execution_time']:.4f} s")
            with res_col3:
                st.metric("Jobs × Machines", f"{result['jobs']} × {result['machines']}")
            
            # Display the solution
            st.subheader("Job Sequence")
            st.write(f"Optimal Sequence: {', '.join(map(str, result['solution']))}")
            
            # Plot convergence graph
            st.subheader("Convergence Graph")
            df_conv = pd.DataFrame(result['convergence_data'])
            fig_conv = px.line(
                df_conv, 
                x='iteration', 
                y='makespan',
                title="Algorithm Convergence",
                labels={"iteration": "Iteration", "makespan": "Makespan"}
            )
            fig_conv.update_layout(height=300)
            st.plotly_chart(fig_conv, use_container_width=True)
            
            # Visualize the schedule
            st.subheader("Schedule Visualization")
            gantt_chart = visualize_schedule(result)
            st.plotly_chart(gantt_chart, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    from pages.results_analysis import show_results_analysis
    show_results_analysis()

with tab3:
    from pages.algorithm_comparison import show_algorithm_comparison
    show_algorithm_comparison()

# Sidebar - Tutorial and info
with st.sidebar:
    st.header("📘 User Guide")
    
    with st.expander("📋 About Flowshop Scheduling"):
        st.write("""
        **Flowshop scheduling** is a production scheduling problem where:
        
        - A set of jobs must be processed on multiple machines
        - Each job must be processed on all machines in the same order
        - The goal is to find a sequence of jobs that minimizes the makespan (total completion time)
        
        This interface allows you to test different optimization algorithms on benchmark instances.
        """)
    
    with st.expander("🧩 Available Algorithms"):
        st.write("""
        - **NEH Heuristic**: Fast constructive heuristic
        - **Local Search**: Iteratively improves solution through neighborhood search
        - **Iterated Local Search**: Applies perturbations to escape local optima
        - **Simulated Annealing**: Probabilistic technique for global optimization
        - **Genetic Algorithm**: Evolutionary algorithm inspired by natural selection
        - **Tabu Search**: Uses memory structures to escape local optima
        - **Ant Colony Optimization**: Bio-inspired algorithm using pheromone trails
        - **Particle Swarm Optimization**: Population-based stochastic approach
        """)
    
    with st.expander("📊 Understanding Results"):
        st.write("""
        - **Makespan**: Total completion time (lower is better)
        - **Execution Time**: How long the algorithm took to run
        - **Machine Utilization**: How efficiently each machine is used
        - **Convergence**: How solution quality improves over iterations
        - **Job Sequence**: The optimal order to process jobs
        """)
    
    st.divider()
    
    # Add a timestamp
    # st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d')}")
    st.caption("© Flowshop Optimizer Project")