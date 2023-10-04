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

    # Check if the filename contains "-LEFT"
    if [[ "$filename" == *"-LEFT"* ]]; then
        # Check if it doesn't already contain "-ALT"
        if [[ ! "$filename" == *"-ALT"* ]]; then
            # Add "-ALT" before "-LEFT" in the filename
            new_filename="${filename//-LEFT/-ALT-LEFT}"
        else
            # Remove "-ALT" from the filename
            new_filename="${filename//-ALT/}"
        fi
    else
        # Check if the filename doesn't already contain "-ALT"
        if [[ ! "$filename" == *"-ALT"* ]]; then
            # Add "-ALT" to the filename
            new_filename="${filename}-ALT"
        else
            # Remove "-ALT" from the filename
            new_filename="${filename//-ALT/}"
        fi
    fi

    # Run the command with the modified filename
    nChain -c "$new_filename"
done
