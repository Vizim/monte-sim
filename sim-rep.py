import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parameters
num_simulations = 10000  # Number of Monte Carlo simulations
sigma_percentage = 0.5  # 30% standard deviation for all parameters

# Input parameters (modifiable)
num_apps_mean = 50  # Mean number of applications
num_endpoints_mean = 20  # Mean number of point-to-point connections
num_apis_mean = 10  # Mean number of APIs
hours_per_endpoint = 48  # Param for hours per endpoint
hours_per_api = 48  # Param for hours per API
fixed_hardware_cost = 10000  # Fixed hardware cost ($)
cost_per_hour = 100  # Fixed cost per hour ($)
productivity_coefficient = 0.85  # Productivity adjustment

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
hardware_hours = fixed_hardware_cost / cost_per_hour

# Total cost (in dollars)
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
min_cost = results["Total Cost"].min()
max_cost = results["Total Cost"].max()

print(f"Average Total Cost: ${average_cost:,.2f}")
print(f"Minimum Total Cost: ${min_cost:,.2f}")
print(f"Maximum Total Cost: ${max_cost:,.2f}")

# Display first few rows of the DataFrame
print(results.head())

# Visualization: Histogram of Total Costs
plt.figure(figsize=(10, 6))
plt.hist(results["Total Cost"], bins=50, color='skyblue', alpha=0.7)
plt.title("Distribution of Total Costs (Monte Carlo Simulation)", fontsize=14)
plt.xlabel("Total Cost ($)", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.grid(True)
plt.show()

# Additional visualizations
# Plot Total Cost vs Number of Applications
plt.figure(figsize=(10, 6))
plt.scatter(results["Number of Applications"], results["Total Cost"], alpha=0.5, color='orange', label='Data points')
plt.title("Total Cost vs Number of Applications", fontsize=14)
plt.xlabel("Number of Applications", fontsize=12)
plt.ylabel("Total Cost ($)", fontsize=12)
plt.grid(True)
plt.show()
