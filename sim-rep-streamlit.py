import numpy as np
import pandas as pd
import streamlit as st
import matplotlib as plt

# Streamlit Inputs for Parameters
st.title("Monte Carlo Simulation for Total Cost Estimation")

# Input parameters
num_simulations = st.number_input("Number of Monte Carlo simulations", min_value=100, value=10000, step=100)
sigma_percentage = st.number_input("Standard Deviation Percentage", min_value=0.1, max_value=1.0, value=0.3, step=0.05)

num_apps_mean = st.number_input("Mean number of applications", min_value=1, value=50, step=1)
num_endpoints_mean = st.number_input("Mean number of point-to-point connections", min_value=1, value=20, step=1)
num_apis_mean = st.number_input("Mean number of APIs", min_value=1, value=10, step=1)
hours_per_endpoint = st.number_input("Hours per endpoint", min_value=1, value=48, step=1)
hours_per_api = st.number_input("Hours per API", min_value=1, value=48, step=1)
fixed_hardware_cost = st.number_input("Fixed hardware cost ($)", min_value=1000, value=10000, step=1000)
cost_per_hour = st.number_input("Cost per hour ($)", min_value=10, value=100, step=10)
productivity_coefficient = st.number_input("Productivity adjustment", min_value=0.0, max_value=1.0, value=0.85, step=0.05)

# Calculate the standard deviation based on sigma_percentage
num_apps_std = num_apps_mean * sigma_percentage
num_endpoints_std = num_endpoints_mean * sigma_percentage
num_apis_std = num_apis_mean * sigma_percentage

# Generate distributions
num_apps = np.random.normal(num_apps_mean, num_apps_std, num_simulations)
num_endpoints = np.random.normal(num_endpoints_mean, num_endpoints_std, num_simulations)
num_apis = np.random.normal(num_apis_mean, num_apis_std, num_simulations)

# Calculated distributions
endpoint_hours = num_endpoints * hours_per_endpoint
api_hours = num_apis * hours_per_api

# Total development hours
total_hours = (endpoint_hours + api_hours) * productivity_coefficient

# Convert hardware cost to equivalent hours
hardware_hours = fixed_hardware_cost 

# Total cost (in dollars) without max value constraint
total_cost = (total_hours + hardware_hours) * cost_per_hour

# Store results in a DataFrame
results = pd.DataFrame({
    "Number of Applications": num_apps,
    "Number of Endpoints": num_endpoints,
    "Number of APIs": num_apis,
    "Endpoint Hours": endpoint_hours,
    "API Hours": api_hours,
    "Total Hours": total_hours,
    "Hardware Hours": hardware_hours,
    "Total Cost": total_cost
})

# Output the results
average_cost = results["Total Cost"].mean()
min_total_cost = results["Total Cost"].min()
max_total_cost = results["Total Cost"].max()

# Display the results in Streamlit
st.subheader("Simulation Results")
st.write(f"**Average Total Cost:** ${average_cost:,.2f}")
st.write(f"**Minimum Total Cost:** ${min_total_cost:,.2f}")
st.write(f"**Maximum Total Cost:** ${max_total_cost:,.2f}")

# Display first few rows of the DataFrame
st.write("**First few rows of the results:**")
st.write(results.head())

# Display the estimated price in large text next to the inputs
st.markdown(f"""
    <div style="font-size: 24px; font-weight: bold; color: #ff5733; text-align: center;">
        Estimated Total Price: ${average_cost:,.2f}
    </div>
""", unsafe_allow_html=True)

# Visualization: Histogram of Total Costs using Matplotlib, and display it with Streamlit's st.pyplot
st.subheader("Distribution of Total Costs")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(results["Total Cost"], bins=50, color='skyblue', alpha=0.7)
ax.set_title("Distribution of Total Costs (Monte Carlo Simulation)", fontsize=14)
ax.set_xlabel("Total Cost ($)", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
ax.grid(True)

# Display the plot using st.pyplot
st.pyplot(fig)

# Display the average cost in header
st.header(f"Estimated Total Cost: ${average_cost:,.2f}")
