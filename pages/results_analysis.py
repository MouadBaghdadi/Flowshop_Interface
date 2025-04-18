import streamlit as st
import pandas as pd

from data import export_to_csv, export_to_json
from visualization import (
    visualize_schedule, 
    create_convergence_plot, 
    create_machine_utilization_chart, 
    create_job_completion_chart
)

def show_results_analysis():
    """
    Display the Results Analysis page content.
    """
    st.header("Results Analysis")
    
    if not st.session_state.history:
        st.info("No optimizations have been run yet. Go to the 'Run Optimization' tab to generate results.")
    else:
        # Select a result to analyze
        result_options = [f"{h['algorithm']} on {h['instance']} ({h['timestamp']})" for h in st.session_state.history]
        selected_result_idx = st.selectbox("Select Result to Analyze", range(len(result_options)), format_func=lambda x: result_options[x])
        
        if selected_result_idx is not None:
            result = st.session_state.history[selected_result_idx]
            
            # Display detailed analysis
            st.subheader(f"Analysis of {result['algorithm']} on {result['instance']}")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Makespan", f"{result['makespan']}")
            with col2:
                st.metric("Jobs", f"{result['jobs']}")
            with col3:
                st.metric("Machines", f"{result['machines']}")
            with col4:
                st.metric("Execution Time", f"{result['execution_time']:.4f} s")
            
            # Parameter settings
            st.subheader("Parameter Settings")
            param_df = pd.DataFrame(list(result['parameters'].items()), columns=['Parameter', 'Value'])
            st.dataframe(param_df, use_container_width=True)
            
            # Detailed visualizations
            st.subheader("Visualizations")
            
            tabs = st.tabs(["Schedule", "Convergence", "Machine Utilization", "Job Completion"])
            
            with tabs[0]:
                gantt_chart = visualize_schedule(result)
                st.plotly_chart(gantt_chart, use_container_width=True)
            
            with tabs[1]:
                conv_plot = create_convergence_plot(result['convergence_data'])
                st.plotly_chart(conv_plot, use_container_width=True)
            
            with tabs[2]:
                machine_chart = create_machine_utilization_chart(result['machine_utilization'])
                st.plotly_chart(machine_chart, use_container_width=True)
            
            with tabs[3]:
                job_chart = create_job_completion_chart(result['job_completion'])
                st.plotly_chart(job_chart, use_container_width=True)
            
            # Solution details
            st.subheader("Solution Details")
            st.write(f"Job Sequence: {', '.join(map(str, result['solution']))}")
            
            # Export options
            st.subheader("Export Results")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Export to CSV"):
                    file_path = export_to_csv(result)
                    st.success(f"Results exported to {file_path}")
            
            with col2:
                if st.button("Export to JSON"):
                    file_path = export_to_json(result)
                    st.success(f"Results exported to {file_path}")