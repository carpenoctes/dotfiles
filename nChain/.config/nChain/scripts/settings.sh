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
	"bash nChain.sh -l AmethystAria"
	"killall waybar"
	#"killall swww"

	"waybar &"
	"swww img --transition-type=wipe --transition-fps 60 /home/saddaf/wallpapers/desktop.jpg &"
	"nwg-look -a"
	"cd /home/saddaf/.config/dunst"
	"sh dunstmerge top-right"
	"kill $(pidof dunst)"
	'for file in /home/saddaf/.config/nChain/links/*; do [ "$(basename "$file")" != "AmethystDusk" ] && [ -f "$file" ] && filename=$(basename "$file") && filename="${filename^}" && notify-send -a "nChain" "Theme: $filename"; done'
	'dunstify -a "Muter" -i audio-volume-muted -r 2593 "Volume muted!"'
	'notify-send -a "nChain" -u critical "Urgent" "This is an urgent message!"'
	'notify-send -a "nChain" -u low "Another message" "This is a low priority message"'
	'notify-send -a "nChain" "Normal message" "This is a normal message"'
	# "$HOME/.config/nChain/scripts/notify-send.sh &"
	# "kitty @ all set-colors -a -c $HOME/.config/kitty/theme.conf"
	#~/Documents/miniprojects/nChain/nChain.sh
)

