import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
df = pd.read_csv('locust_results_stats.csv')

# Remove any rows where 'Type' is NaN or 'Aggregated'
df = df[df['Type'].notna() & (df['Name'] != 'Aggregated')]

# Independent grouped bar plots for Request Count and Average Response Time per Endpoint
labels = df['Name']
x = np.arange(len(labels))  # label locations
width = 0.35  # width of the bars

# Grouped bar plot with independent and logarithmic scales
fig, ax1 = plt.subplots(figsize=(12, 7))

# Bar for Request Count (left y-axis, linear)
bar1 = ax1.bar(x - width/2, df['Request Count'], width, label='Request Count', color='tab:blue')
ax1.set_ylabel('Request Count', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45)

# Bar for Average Response Time (right y-axis, logarithmic)
ax2 = ax1.twinx()
bar2 = ax2.bar(x + width/2, df['Average Response Time'], width, label='Avg Response Time', color='tab:orange', alpha=0.7)
ax2.set_ylabel('Average Response Time (ms)', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax2.set_yscale('log')

# Legends
bars = [bar1, bar2]
labels_legend = ['Request Count', 'Avg Response Time (log)']
ax1.legend(bars, labels_legend, loc='upper left')

plt.title('Grouped Bar: Request Count (linear) and Average Response Time (log) per Endpoint')
plt.tight_layout()
plt.show()