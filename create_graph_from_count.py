import os
import matplotlib.pyplot as plt

# Define the root folder (you can replace this with the actual path)
root_folder = "Videos1"

# Initialize a dictionary to store counts
folder_counts = {}

# Loop through the folders
for folder_name in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder_name)
    if os.path.isdir(folder_path):
        # Count the number of files in the folder
        file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        folder_counts[folder_name] = file_count

# Prepare data for the pie chart
labels = folder_counts.keys()
sizes = folder_counts.values()

# Create the pie chart
plt.figure(figsize=(10, 10))

plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title("Distribution of Videos in Each Category", pad = 20)
plt.tight_layout()
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
plt.show()
