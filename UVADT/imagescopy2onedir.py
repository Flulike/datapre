import os
from pathlib import Path

# Use raw strings or forward slashes for Windows paths to avoid issues
multidirpath = Path(r'D:\program\dataset\UAV-benchmark-M')
outdir = Path(r'D:\program\dataset\UAVDT\images')

# Create output directory if it doesn't exist
outdir.mkdir(parents=True, exist_ok=True)

# Iterate through directories
for dir_path in multidirpath.iterdir():
    # Skip if not a directory
    if not dir_path.is_dir():
        continue
        
    for image_file in dir_path.iterdir():
        if image_file.is_file():
            # Create new filename with directory prefix
            new_filename = f"{dir_path.name}_{image_file.name[-10:]}"
            dest_path = outdir / new_filename
            
            # Use Path.read_bytes() and write_bytes() instead of shutil
            dest_path.write_bytes(image_file.read_bytes())