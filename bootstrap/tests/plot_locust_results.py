import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("locust_results_stats_history.csv")

# Convert Timestamp to seconds since start
df["Timestamp"] = df["Timestamp"] - df["Timestamp"].min()

# Plot User Count over time
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(df["Timestamp"], df["User Count"], marker="o")
plt.title("User Count Over Time")
plt.xlabel("Time (s)")
plt.ylabel("User Count")

# Plot Median Response Time over time
plt.subplot(1, 2, 2)
plt.plot(df["Timestamp"], pd.to_numeric(df["50%"], errors="coerce"), marker="o", color="orange")
plt.title("Median Response Time Over Time")
plt.xlabel("Time (s)")
plt.ylabel("Median Response Time (ms)")

plt.tight_layout()
plt.show()