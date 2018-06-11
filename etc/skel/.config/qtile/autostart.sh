#!/bin/sh
feh --bg-scale ~/.config/qtile/6.jpg &
nm-applet &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
pasystray &
xcompmgr &
~/.config/polybar/launch.sh $
