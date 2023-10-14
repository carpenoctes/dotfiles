#!/usr/bin/env bash

launcher="rofi -dmenu -p 'Select theme:'"

folders_to_skip=(
  "otherfiles"
  "*LEFT"
  "*ALT"
)

pre_commands=(
  # "echo 'This is running before the change'"
)

post_commands=(
  "bash nChain.sh -l default"
  "killall waybar"
  "killall wbg"
  
  "waybar &"
  "wbg /home/saddaf/wallpapers/desktop.jpg &"
  "nwg-look -a"
  "cd /home/saddaf/.config/dunst"
  "sh dunstmerge top-right"
  "kill $(pidof dunst)"
  # "$HOME/.config/nChain/scripts/notify-send.sh &"
  # "kitty @ all set-colors -a -c $HOME/.config/kitty/theme.conf"
  #~/Documents/miniprojects/nChain/nChain.sh
)