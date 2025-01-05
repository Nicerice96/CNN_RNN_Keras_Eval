import json
import matplotlib.pyplot as plt

# Load JSON data for both checkpoints
with open('checkpoint2/trainer_state.json', 'r') as file:
    data1 = json.load(file)
with open('checkpoint3/trainer_state.json', 'r') as file:
    data2 = json.load(file)

# Extract the 'log_history' list for both checkpoints
log_history1 = data1["log_history"]
log_history2 = data2["log_history"]

# Create empty lists to store values for different metrics
epochs1, epochs2 = [], []
losses1, losses2 = [], []
learning_rates1, learning_rates2 = [], []
grad_norms1, grad_norms2 = [], []

# Loop through the 'log_history' for both checkpoints and extract the required metrics
for entry in log_history1:
    epoch = entry["epoch"]
    epochs1.append(epoch)
    if "loss" in entry:
        losses1.append(entry["loss"])
    if "learning_rate" in entry:
        learning_rates1.append(entry["learning_rate"])
    if "grad_norm" in entry:
        grad_norms1.append(entry["grad_norm"])

for entry in log_history2:
    epoch = entry["epoch"]
    epochs2.append(epoch)
    if "loss" in entry:
        losses2.append(entry["loss"])
    if "learning_rate" in entry:
        learning_rates2.append(entry["learning_rate"])
    if "grad_norm" in entry:
        grad_norms2.append(entry["grad_norm"])

# Align the lengths of the lists
min_length = min(len(epochs1), len(epochs2), len(losses1), len(losses2), len(learning_rates1), len(learning_rates2), len(grad_norms1), len(grad_norms2))
epochs1, epochs2 = epochs1[:min_length], epochs2[:min_length]
losses1, losses2 = losses1[:min_length], losses2[:min_length]
learning_rates1, learning_rates2 = learning_rates1[:min_length], learning_rates2[:min_length]
grad_norms1, grad_norms2 = grad_norms1[:min_length], grad_norms2[:min_length]

# Create subplots for different metrics
fig, axs = plt.subplots(3, 1, figsize=(10, 18), gridspec_kw={'hspace': 0.5})

# Plot loss
axs[0].plot(epochs1, losses1, marker='o', linestyle='-', color='r', label='Checkpoint 2 Loss')
axs[0].plot(epochs2, losses2, marker='o', linestyle='-', color='b', label='Checkpoint 3 Loss')
axs[0].set_title("Loss vs. Epoch")
axs[0].set_xlabel("Epoch")
axs[0].set_ylabel("Loss")
axs[0].grid(True)
axs[0].legend()

# Plot learning rate
axs[1].plot(epochs1, learning_rates1, marker='o', linestyle='-', color='r', label='Checkpoint 2 Learning Rate')
axs[1].plot(epochs2, learning_rates2, marker='o', linestyle='-', color='b', label='Checkpoint 3 Learning Rate')
axs[1].set_title("Learning Rate vs. Epoch")
axs[1].set_xlabel("Epoch")
axs[1].set_ylabel("Learning Rate")
axs[1].grid(True)
axs[1].legend()

# Plot grad_norm
axs[2].plot(epochs1, grad_norms1, marker='o', linestyle='-', color='r', label='Checkpoint 2 Gradient Norm')
axs[2].plot(epochs2, grad_norms2, marker='o', linestyle='-', color='b', label='Checkpoint 3 Gradient Norm')
axs[2].set_title("Gradient Norm vs. Epoch")
axs[2].set_xlabel("Epoch")
axs[2].set_ylabel("Gradient Norm")
axs[2].grid(True)
axs[2].legend()

# Show all subplots
plt.tight_layout()
plt.show()

# Calculate the average loss and average gradient norm for each checkpoint
avg_loss1 = sum(losses1) / len(losses1) if losses1 else 0
avg_loss2 = sum(losses2) / len(losses2) if losses2 else 0
avg_grad_norm1 = sum(grad_norms1) / len(grad_norms1) if grad_norms1 else 0
avg_grad_norm2 = sum(grad_norms2) / len(grad_norms2) if grad_norms2 else 0

# Print the average values
print(f"Checkpoint 2 - Average Loss: {avg_loss1:.4f}, Average Gradient Norm: {avg_grad_norm1:.4f}")
print(f"Checkpoint 3 - Average Loss: {avg_loss2:.4f}, Average Gradient Norm: {avg_grad_norm2:.4f}")