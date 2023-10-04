#!/bin/bash
sh dunstmerge top-right
pidof dunst && killall dunst
#dunst -print &
dunst
notify-send -u critical "Urgent" "This is an urgent message!"
#dunstify "TT" "<span font='Iosevka 16' foreground='#618C8F'>BIG MSG</span>"
dunstify -A yes,ACCEPT -A no,DECLINE "Call waiting"
notify-send -a "System notification" -u low "Another message" "...while this is a low priority message"
notify-send -a "System notification" "Title" "Lorem ipsum dolor sit amet..."
#notify-send -a "Thunderbird" "saddaf@vectuz.se" "This is what Vectuz emails look like"
#notify-send -a "Thunderbird" "saddaf@prisfakta.se" "This is what Prisfakta emails look like"
#notify-send -a "discord" "utopiabot" ":scream_cat: You have been hit..."
#dunstify  "A title" "some text scripttest" -h int:value:12
#dunstify  "My scripttest" "some text"
