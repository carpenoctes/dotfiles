#!/usr/bin/env bash

mkdir $HOME/.cache/nQuire > /dev/null 2>&1
refresh_list=false;
file_list=$HOME/.cache/nQuire/file_list
source $HOME/.config/nQuire/settings.sh

display_help() {
  echo "Options:"
  echo "  -h       Display this help message."
  echo "  -r       refresh the list"
  echo ""
  echo "           Not choosing an option will run current list."
  exit 0
}

# options
while getopts "hr" opt; do
  case $opt in
    h)
      display_help
      ;;
    r)
      refresh_list=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done


if [ "$refresh_list" = true ]; then
  if [ "$include_all_dotfiles" = true ]; then
    find ~/ -type f > "$file_list"
  else
    included_files=""
    for dotfile in "${include_these_dotfiles[@]}"; do
        included_files+=" -o -path '*/$dotfile/*'"
    done

    eval "find ~/ \( -type f -a \( ! -path '*/.*' $included_files \) \)| sed 's|^$HOME/||' > $file_list"
  fi
fi

chosen_file=$(printf "%s\n" "$(cat $file_list )" | eval "$launcher")
if [ -n "$chosen_file" ]; then
  chosen_file="$HOME/$chosen_file"
  xdg-open "$chosen_file"
fi
