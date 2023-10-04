#!/usr/bin/env bash

# Define the directory to check
directory="$HOME/.config/nChain/links"

# Loop through the files in the directory
for file in "$directory"/*; do
    # Extract the filename without the path
    filename=$(basename "$file")

    # Check if the filename is "default"
    if [[ "$filename" = "default"* ]]; then
        continue  # Skip the "default" file
    fi

    # Check if the filename contains "-ALT"
    if [[ "$filename" == *"-ALT"* ]]; then
        echo "  "
    else
        echo "  "
    fi
done
