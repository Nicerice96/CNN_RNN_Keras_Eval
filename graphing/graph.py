import json
import matplotlib.pyplot as plt

# Load your JSON data
with open('checkpoint2/trainer_state.json', 'r') as file:
    data = json.load(file)

# Extract the 'log_history' list
log_history = data["log_history"]

# Create empty lists to store values for different metrics
epochs = []
losses = []
learning_rates = []
grad_norms = []
train_losses = []

# Loop through the 'log_history' and extract 'epoch', 'loss', 'learning_rate', 'grad_norm', etc.
for entry in log_history:
    epoch = entry["epoch"]

    # Extract 'loss' or 'train_loss', and 'learning_rate' and 'grad_norm'
    if "loss" in entry:
        losses.append(entry["loss"])
    elif "train_loss" in entry:  # Handle case where 'train_loss' exists
        train_losses.append(entry["train_loss"])
    if "learning_rate" in entry:
        learning_rates.append(entry["learning_rate"])
    if "grad_norm" in entry:
        grad_norms.append(entry["grad_norm"])

    # Add the epoch to the epochs list
    epochs.append(epoch)

# Debugging: Print lengths to see where the mismatch is
print(f"Number of epochs: {len(epochs)}")
print(f"Number of losses: {len(losses)}")

# If there are any mismatches, handle them by trimming to the smaller list length
min_length = min(len(epochs), len(losses))
epochs = epochs[:min_length]
losses = losses[:min_length]

# Create subplots for different metrics
fig, axs = plt.subplots(3, 1, figsize=(10, 18), gridspec_kw={'hspace': 0.5})

# Plot loss
axs[0].plot(epochs, losses, marker='o', linestyle='-', color='b', label='Loss')
axs[0].set_title("Loss vs. Epoch")
axs[0].set_xlabel("Epoch")
axs[0].set_ylabel("Loss")
axs[0].grid(True)
axs[0].legend()

# Plot learning rate
axs[1].plot(epochs, learning_rates, marker='o', linestyle='-', color='g', label='Learning Rate')
axs[1].set_title("Learning Rate vs. Epoch")
axs[1].set_xlabel("Epoch")
axs[1].set_ylabel("Learning Rate")
axs[1].grid(True)
axs[1].legend()

# Plot grad_norm
axs[2].plot(epochs, grad_norms, marker='o', linestyle='-', color='r', label='Gradient Norm')
axs[2].set_title("Gradient Norm vs. Epoch")
axs[2].set_xlabel("Epoch")
axs[2].set_ylabel("Gradient Norm")
axs[2].grid(True)
axs[2].legend()

# Show all subplots
plt.tight_layout()
plt.show()