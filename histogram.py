import os
import matplotlib.pyplot as plt
from moviepy.video.io.VideoFileClip import VideoFileClip

# Define the path to the main directory
videos_dir = "Videos1"  # Replace with the actual path to your Videos1 folder

# Initialize a list to store video lengths
video_lengths = []

# Traverse through each subdirectory
for root, dirs, files in os.walk(videos_dir):
    for file in files:
        if file.endswith(('.mp4', '.avi', '.mkv', '.mov')):  # Add other extensions if needed
            video_path = os.path.join(root, file)
            try:
                # Load the video and get its duration
                with VideoFileClip(video_path) as video:
                    video_lengths.append(video.duration)  # Duration in seconds
            except Exception as e:
                print(f"Error processing {video_path}: {e}")

# Create a histogram of video lengths
plt.figure(figsize=(10, 6))
plt.hist(video_lengths, bins=20, color='skyblue', edgecolor='black')
plt.title("Distribution of Video Lengths")
plt.xlabel("Video Length (seconds)")
plt.ylabel("Frequency")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the histogram as an image
plt.savefig("video_lengths_histogram.png")
print("Histogram saved as 'video_lengths_histogram.png'.")

# Show the histogram
plt.show()
