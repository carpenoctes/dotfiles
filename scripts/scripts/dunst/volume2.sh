#!/bin/bash
# Requires dunst och dunstify
# Based on https://gist.github.com/sebastiencs/5d7227f388d93374cebdf72e783fbd6a

function get_volume {
    #amixer -M get Master | awk 'END { print $0, value }' | awk '{print $3}'
    amixer get Master | grep '%' | head -n 1 | cut -d '[' -f 2 | cut -d '%' -f 1

}

function is_mute {
    amixer get Master | grep '%' | grep -oE '[^ ]+$' | grep off > /dev/null
}

function send_notification {
    volume=`get_volume`
    #dunstify  "Title" -r 2593 -h int:value:${volume} "Volume: ${volume}%"
    dunstify  -a "Volym" -i audio-volume-high "" -r 2593 -h int:value:${volume}
}

case $1 in
    up)
        amixer set Master on > /dev/null
        amixer set Master 5+ > /dev/null
        send_notification
	;;
    down)
        amixer set Master on > /dev/null
        amixer set Master 5- > /dev/null
        send_notification
	;;
    mute)
        #pactl set-sink-mute @DEFAULT_SINK@ toggle > /dev/null
        amixer set Master toggle > /dev/null
        amixer sset Headphone unmute
        if is_mute ; then
            dunstify -a "Muter" -i audio-volume-muted -r 2593 -u normal "Volume muted!"
            else
            send_notification
    	fi
	;;
esac