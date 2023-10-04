#!/usr/bin/env bash

target_dir="$HOME"

# Function to add symlinks and directories

# Function to add symlinks and directories
add_links() {
    # Check if the user provided an input variable
    if [ -z "$input_variable" ]; then
        echo "Error: Missing theme name to link"
        exit 1
    fi

    # Use the second argument if provided, otherwise use the first argument
    link_finder="${2:-$input_variable}"

    source_dir="$HOME/.config/nChain/themes/$input_variable"
    target_link_dir="$HOME/.config/nChain/links/${link_finder}"  # Use a different variable

    # Iterate through all files and directories in the source directory
    find "$source_dir" -type f -o -type d | while read source_item; do
        # Get the relative path from the source directory
        relative_path="${source_item#$source_dir}"

        # Build the corresponding target path
        target_item="$target_dir$relative_path"

        if [ -d "$source_item" ]; then
            # If it's a directory, create it in the target directory
            mkdir -p "$target_item"
        elif [ -f "$source_item" ]; then
            # Check if a file already exists at the target location
            if [ ! -e "$target_item" ]; then
                # If it doesn't exist, create a symlink in the target directory
                ln -s "$source_item" "$target_item"

                # Append the path to the linkFinder file
                echo "$target_item" >> "$target_link_dir"
                echo "Linked: $target_item" 
            else
                echo "Conflict: $target_item (skipping)"
            fi
        fi
    done
}

# Function to delete symlinks and empty folders
delete_links() {
    # Check if the user provided an input variable
    if [ -z "$input_variable" ]; then
        echo "Error: Missing theme name to unlink."
        exit 1
    fi

    link_finder="$HOME/.config/nChain/links/${input_variable}"

    # Check if the linkFinder file exists
    if [ ! -f "$link_finder" ]; then
        echo "Error: $link_finder not found."
        exit 1
    fi

    # Create an associative array to track folder statuses
    declare -A folder_status

    # Read each line (link path) from the linkFinder file
    while IFS= read -r link_path; do
        # Check if the link exists
        if [ -L "$link_path" ]; then
            # Remove the link
            rm "$link_path"
            echo "Removed: $link_path"

            # Determine the folder containing the link
            link_folder=$(dirname "$link_path")

            # Update folder status
            folder_status["$link_folder"]="not_empty"
        else
            echo "Not found: $link_path"
        fi
    done < "$link_finder"

    # Remove the linkFinder file after removing the links
    rm "$link_finder"

    # Check and remove empty folders
    for folder in "${!folder_status[@]}"; do
        if [ "${folder_status[$folder]}" == "not_empty" ] && [ -z "$(ls -A "$folder")" ]; then
            rmdir "$folder"
            echo "Removed empty folder: $folder"
        fi
    done
}

# Handle options and input variable
while [[ $# -gt 0 ]]; do
    case "$1" in
        -l | -link)
            input_variable="$2"
            shift 2  # Shift the first two arguments (the flag and the first argument)
            if [ -n "$1" ]; then
                link_finder="$1"  # Set link_finder to the second argument if provided
            else
                link_finder="$input_variable"  # Use the first argument as the default
            fi
            add_links "$input_variable" "$link_finder"
            ;;
        -d | -delete)
            input_variable="$2"
            delete_links
            ;;
        *)
            exit 1
            ;;
    esac
    shift
done
