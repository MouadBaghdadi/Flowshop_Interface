import streamlit as st
import pandas as pd

from utils import compare_results
from visualization import (
    visualize_schedule, 
    create_performance_scatter_plot, 
    create_makespan_comparison_chart,
    create_execution_time_comparison_chart
)

def show_algorithm_comparison():
    """
    Display the Algorithm Comparison page content.
    """
    st.header("Algorithm Comparison")
    
    if not st.session_state.comparison_data:
        st.info("No optimizations have been run yet. Go to the 'Run Optimization' tab to generate results for comparison.")
    else:
        st.write("Compare the performance of different algorithms on the same instances")
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            # Filter by instance
            available_instances = list(set([r['instance'] for r in st.session_state.comparison_data]))
            selected_instances = st.multiselect(
                "Filter by Instance", 
                available_instances,
                default=available_instances
            )
        
        with col2:
            # Filter by algorithm
            available_algorithms = list(set([r['algorithm'] for r in st.session_state.comparison_data]))
            selected_algorithms = st.multiselect(
                "Filter by Algorithm", 
                available_algorithms,
                default=available_algorithms
            )
        
        # Filter the data
        filtered_data = [
            r for r in st.session_state.comparison_data 
            if r['instance'] in selected_instances and r['algorithm'] in selected_algorithms
        ]
        
        if not filtered_data:
            st.warning("No data matches your filter criteria.")
        else:
            # Create comparison table
            st.subheader("Performance Comparison")
            
            comparison_df = compare_results(filtered_data)
            st.dataframe(comparison_df, use_container_width=True)
            
            # Create visualizations for comparison
            st.subheader("Visual Comparison")
            
            # Makespan comparison
            makespan_chart = create_makespan_comparison_chart(comparison_df)
            st.plotly_chart(makespan_chart, use_container_width=True)
            
            # Execution time comparison
            time_chart = create_execution_time_comparison_chart(comparison_df)
            st.plotly_chart(time_chart, use_container_width=True)
            
            # Performance overview
            st.subheader("Performance Overview")
            
            # Create a scatter plot of makespan vs execution time
            scatter_plot = create_performance_scatter_plot(comparison_df)
            st.plotly_chart(scatter_plot, use_container_width=True)
            
            # Best solution
            if st.session_state.best_solution:
                st.subheader("Best Solution Found")
                
                best = st.session_state.best_solution
                st.success(f"The best solution found was using {best['algorithm']} on {best['instance']} with a makespan of {best['makespan']}.")
                
                # Show solution
                st.write(f"Optimal Sequence: {', '.join(map(str, best['solution']))}")
                
                # Show Gantt chart for best solution
                best_gantt = visualize_schedule(best)
                st.plotly_chart(best_gantt, use_container_width=True)