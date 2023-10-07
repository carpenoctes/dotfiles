#!/usr/bin/env sh
grim -g "$(slurp)" '/home/saddaf/scripts/dunst/grimtemp.png'
#wl-copy < "/home/saddaf/scripts/dunst/grimtemp.png" doesn't work anymore after reinstalling arch
xclip -in -selection clipboard -target image/png /home/saddaf/scripts/dunst/grimtemp.png