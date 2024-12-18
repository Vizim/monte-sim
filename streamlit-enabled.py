import numpy as np
import pandas as pd
import streamlit as st
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt

# Streamlit App Header
st.title("Monte Carlo Simulation for Cost Estimation")

# Define the input dataset as a pandas DataFrame
default_data = {
    "Feature": [
        "Number Of Applications",
        "% Of Applications With Point to Point Integrations",
        "Average Number Of Point to Point Integrations",
        "Number Of APIs to integrate with record keeping system",
        "Development Hours",
        "Annual Support Hours",
        "Hardware Costs",
        "Productivity Coefficient",
        "Cost Per Hour",
    ],
    "Mean": [
        100,  # Number Of Applications
        0.3,  # % With Point to Point Integrations
        5,    # Avg Number of Point to Point Integrations
        10,   # Number Of APIs
        500,  # Development Hours
        200,  # Annual Support Hours
        10000,  # Hardware Costs
        0.9,  # Productivity Coefficient
        50,   # Cost Per Hour
    ],
    "StdDev (%)": [10] * 9,  # Standard deviation as a % of mean (adjustable)
}

# Convert to pandas DataFrame
df = pd.DataFrame(default_data)
df.head()
# Streamlit Sliders for Adjusting Input Data
st.sidebar.header("Adjust Input Parameters")

for i in range(len(df)):
    if df["Feature"][i] == "% Of Applications With Point to Point Integrations" or df["Feature"][i] == "Productivity Coefficient":
        # For percentages and coefficients, use slider in [0, 1] range
        df.at[i, "Mean"] = st.sidebar.slider(
            df["Feature"][i],
            min_value=0.0,
            max_value=1.0,
            value=float(df["Mean"][i]),
            step=0.01,
        )
    else:
        # For numeric features, use integer sliders
        df.at[i, "Mean"] = st.sidebar.slider(
            df["Feature"][i],
            min_value=0,
            max_value=int(df["Mean"][i] * 2),  # Allow adjusting up to 2x the default
            value=int(df["Mean"][i]),
            step=1,
        )

# Allow standard deviation adjustment
std_dev_percentage = st.sidebar.slider(
    "Standard Deviation (%)",
    min_value=1,
    max_value=50,
    value=10,
    step=1,
)

# Update stddev in DataFrame
df["StdDev"] = df["Mean"] * (std_dev_percentage / 100)

# Display adjusted input data
st.subheader("Adjusted Input Parameters")
st.write(df)

# Step 1: Create Gaussian Mixture Model for the Monte Carlo Simulation
means = df["Mean"].values
std_devs = df["StdDev"].values
cov_matrix = np.diag(std_devs**2)  # Start with independence

# Fit Gaussian Mixture Model
gmm = GaussianMixture(n_components=1, covariance_type="full", random_state=42)
gmm.means_ = means.reshape(1, -1)
gmm.covariances_ = cov_matrix.reshape(1, len(means), len(means))
gmm.weights_ = np.array([1])
gmm.precisions_cholesky_ = np.linalg.cholesky(np.linalg.inv(cov_matrix)).reshape(1, len(means), len(means))

# Step 2: Generate Monte Carlo samples
num_simulations = st.sidebar.slider("Number of Simulations", min_value=1000, max_value=50000, value=10000, step=1000)
simulated_data = gmm.sample(n_samples=num_simulations)[0]
simulated_df = pd.DataFrame(simulated_data, columns=df["Feature"])

# Step 3: Calculate costs for each simulation
simulated_df["Cost"] = (
    (simulated_df["Development Hours"] + simulated_df["Annual Support Hours"]) * simulated_df["Cost Per Hour"]
    + simulated_df["Hardware Costs"] * simulated_df["Productivity Coefficient"]
)

# Step 4: Analyze results
mean_cost = simulated_df["Cost"].mean()
std_cost = simulated_df["Cost"].std()
alpha = 0.05
lower_bound = np.percentile(simulated_df["Cost"], 100 * (alpha / 2))
upper_bound = np.percentile(simulated_df["Cost"], 100 * (1 - alpha / 2))
confidence_interval = (lower_bound, upper_bound)

# Display results
st.subheader("Simulation Results")
st.write(f"Mean Cost: ${mean_cost:,.2f}")
st.write(f"Standard Deviation of Cost: ${std_cost:,.2f}")
st.write(f"95% Confidence Interval: ${confidence_interval[0]:,.2f} - ${confidence_interval[1]:,.2f}")

# Step 5: Visualize the cost distribution
st.subheader("Cost Distribution")
fig, ax = plt.subplots()
ax.hist(simulated_df["Cost"], bins=50, alpha=0.75, color="blue")
ax.set_title("Cost Distribution (Monte Carlo Simulation)")
ax.set_xlabel("Cost ($)")
ax.set_ylabel("Frequency")
st.pyplot(fig)