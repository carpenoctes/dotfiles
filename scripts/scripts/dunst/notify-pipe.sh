#!/usr/bin/env sh

read n1
read coord rgb1 hex rgb2
wl-copy $hex
notify-send -a "Grim" "Color copied!" "Hex: $hex \nRGB: $rgb1"
