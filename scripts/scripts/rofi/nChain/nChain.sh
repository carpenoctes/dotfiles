#!/usr/bin/env bash

default_name="default"
default_path="$HOME/.config/nChain/$default_name"
config_dir="$HOME/.config/nChain"
use_rofi=true  # Default behavior is to use rofi
theme_to_unstow=$(<$HOME/.config/nChain/current-theme)
unstow_all=false

if [[ "$theme_to_unstow" = $default_name ]]; then
  theme_to_unstow=""
fi

# Function to display help
display_help() {
  echo "Options:"
  echo "  -h       Display this help message."
  echo "  -c       Change to specified theme"
  echo "  -d       Unstow all themes and exit. *WARNING* ONLY USE THIS IF YOU KNOW WHAT YOU ARE DOING"
  echo ""
  echo "           Not choosing an option will run nChain with rofi."
  exit 0
}

# options
while getopts ":cdh" opt; do
  case $opt in
    c)
      use_rofi=false
      ;;
    d)
      unstow_all=true
      break
      ;;
    h)
      display_help
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [ "$unstow_all" = true ]; then
  if [ -n "$theme_to_unstow" ]; then
    # Display a warning and get user confirmation
    echo -e "\e[91m*WARNING* This will remove all your symlinks created by nChain. Are you sure you want to do this? (confirm with yes/no)\e[0m"
    read -r confirmation

    if [ "$confirmation" = "yes" ]; then
      stow -vDt "$HOME" -d "$config_dir" "$default_name"
      stow -vDt "$HOME" -d "$config_dir" "$theme_to_unstow"
      echo "Deleted $theme_to_unstow links"
      echo "" > "$config_dir/current-theme"
    else
      echo "Operation canceled."
      exit 0
    fi
  else
    echo "No previous theme to unstow."
  fi
  exit 0
fi

shift $((OPTIND-1))

if [ "$use_rofi" = false ]; then
  theme_to_stow="$1"
else
  available_themes=()

  while IFS= read -r line; do
    available_themes+=("$line")
  done < <(find "$config_dir"/* -maxdepth 0 -type d -printf "%f\n")
  theme_to_stow=$(printf "%s\n" "${available_themes[@]}" | rofi -dmenu -p "Select theme:") 
fi

if [ -n "$theme_to_stow" ]; then
  echo "A"
  echo -n "$theme_to_stow" > "$config_dir/current-theme"
  echo "B"
  if [ -n "$theme_to_unstow" ]; then
    echo "B2"
    echo "$theme_to_unstow"
    #stow -vDt "$HOME" -d "$config_dir" "$theme_to_unstow"
  fi
  echo "C"
  stow --override='.' -vSt "$HOME" -d "$config_dir" "$default_name"
  echo "D"
  stow --override='.' -vSt "$HOME" -d "$config_dir" "$theme_to_stow"
  echo "E"
  # stow -vSt "$HOME" -d "$config_dir" "$theme_to_stow"
  # post-command options:
  "$config_dir/post-commands.sh"
fi