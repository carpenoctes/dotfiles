#!/usr/bin/env sh
declare RESULT=$(grim -g "$(slurp -p -b FFFFFF00)" -t ppm - | convert - -format '%[pixel:p{0,0}]' txt:-)
rgb="${RESULT:5:-8}"
hex=${RESULT: -6}
wl-copy ${hex}
notify-send -a "Colorpicker" "Color copied!" "Hex: #${hex} \nRGB: ${rgb} \n\n"