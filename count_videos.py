import os

video_src = "Videos"

# Change to the target directory
os.chdir(video_src)

count = 0


for root, dirs, files in os.walk("."):
    print(f"Root folder: {root}")
    
    count_dir_files = 0
    for file in files:
        print(f"File found: {file}")
        count += 1
        count_dir_files += 1
    
    print(f"Files in {root}: {count_dir_files}")

print(f"Final Video Count: {count}")
