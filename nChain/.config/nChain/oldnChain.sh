#!/usr/bin/env bash

config_dir="$HOME/nChain"
use_rofi=true  # Default behavior is to use rofi
theme_to_unstow=$(<$HOME/nChain/current-theme)
unstow_all=false

# Function to display help
display_help() {
  echo "Options:"
  echo "  -h       Display this help message."
  echo "  -c       Change to specified theme"
  echo "  -d       Unstow all themes and exit."
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
    stow -vDt "$HOME" -d "$config_dir" "$theme_to_unstow"
    echo "Deleted $theme_to_unstow links"
    echo "" > "$config_dir/current-theme"
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
  if [ -n "$theme_to_unstow" ]; then
    stow -vDt "$HOME" -d "$config_dir" "$theme_to_unstow"
  fi

  stow -vDt "$HOME" -d "$config_dir" "$theme_to_stow"
  # post-command options:
  #"$config_dir/post-commands.sh"
  echo "$theme_to_stow" > "$config_dir/current-theme"
fi
