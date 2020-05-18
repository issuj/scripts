#!/bin/bash

#2560x1440+0+1080
#1920x1080+368+0

#xrandr --output DP-1 --scale 2x2 --mode 1920x1080 --fb 3840x3600 --pos 0x0
#xrandr --output eDP-1 --scale 1x1 --pos 640x2160
#set -x
INTERNAL="eDP-1"
EXTERNAL="DP-[1-2]"

xrandr=`xrandr`
hasScreen=`echo -n "$xrandr" | grep -e "^$EXTERNAL connected"`
isScreenOn=`echo -n "$xrandr" | grep -e "^$EXTERNAL connected.*+"`

EXTERNAL=`echo -n "$hasScreen" | cut -f 1 -d ' '`

for i in `echo -n "$xrandr" | grep -e '[[:alnum:][:punct:]]*[[:space:]]disconnected' | cut -d ' ' -f 1`; do
  xrandr --output "$i" --scale 1x1 --pos 0x0 --off
done

if [ -n "$hasScreen" -a \( "$1" == "plug" -o -z "$isScreenOn" \) ]; then
  xrandr --output $EXTERNAL --scale 1x1 --mode 2560x1440 --fb 2560x2880 --pos 0x0 --rate 60
  xrandr --output $INTERNAL --scale 1x1 --pos 0x1440 --rate 60
elif [ -n "$isScreenOn" -o "$1" == "unplug" ]; then
  if [ -n "$hasScreen" ]; then
    xrandr --output $EXTERNAL --scale 1x1 --pos 0x0 --off
  fi  
  xrandr --output $INTERNAL --scale 1x1 --pos 0x0 --fb 2560x1440 --rate 60
fi

