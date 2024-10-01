#!/usr/bin/env sh
RESULT=$(grim -g "$(slurp -p -b FFFFFF00)" -t ppm - | magick - -format '%[pixel:p{0,0}]' txt:- | tail -n +2)
notify-send -a "colorpicker" "$RESULT"
rgb=$(echo "$RESULT" | awk '{print $2}')
hex=$(echo "$RESULT" | awk '{print $3}')
wl-copy "${hex}"
msg="Hex: ${hex} \nRGB: ${rgb} \n\n"
notify-send -a "Colorpicker" "Color copied!" "${msg}"
