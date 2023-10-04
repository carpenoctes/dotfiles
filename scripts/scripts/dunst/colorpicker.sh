#!/usr/bin/env sh
declare RESULT=($(grim -g "$(slurp -p -b FFFFFF00)" -t ppm - | convert - -format '%[pixel:p{0,0}]' txt:-))
wl-copy ${RESULT[7]}
notify-send -a "Grim" "Color copied!" "Hex: ${RESULT[7]} \nRGB: ${RESULT[6]} \n\n"
