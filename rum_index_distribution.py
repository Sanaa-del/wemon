import json
import matplotlib.pyplot as plt

# Load JSON data from a file
with open('/home/sghandi/Téléchargements/wemon-main/LWIP.Metrics.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract RUMSpeedIndex values
rumspeedindex_values = []
for entry in data:
    if 'webInfo' in entry and 'ttfb' in entry['webInfo']:
        rumspeedindex_values.append(entry['webInfo']['ttfb'])

# Plot the distribution of RUMSpeedIndex values
plt.figure(figsize=(10, 5))
plt.hist(rumspeedindex_values, bins=range(min(rumspeedindex_values), max(rumspeedindex_values) + 1), edgecolor='black', alpha=0.7)

# Add titles and labels
plt.title('Distribution of ttfb Values')
plt.xlabel('Time to first byte')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.75)
plt.show()

