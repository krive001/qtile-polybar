# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Match, Rule, ScratchPad, DropDown
from libqtile.command import lazy, Client
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer
#from libqtile.dgroups import simple_key_binder
from libqtile.manager import Qtile


try:
    from typing import List  # noqa: F401
except ImportError:
    pass

#Window buttom
mod = "mod4"
# Alt bottom
mod1 = "mod1"

myTerm="urxvt"
myBrowser="chromium"


cls_grp_dict = {
    "luakit": "1", "Firefox": "1", "Opera": "1", "Google-chrome": "1",
    "Chromium": "1", "Vivaldi-stable": "1", "Midori": "2", "Dillo": "2",
    "Netsurf-gtk3": "2", "QupZilla": "2", "Uget-gtk": "2", "Tor Browser": "1",
    "Waterfox": "1", "UXTerm": "3", "Termite": "3", "Terminator": "3",
    "URxvt": "3", "mlterm": "3", "Lxterminal": "3",
    "XTerm": "3", "discord": "4", "Pcmanfm": "8", "Thunar": "8", "dolphin": "8", "Caja": "8",
    "Catfish": "8", "Zathura": "5", "libreoffice-writer": "5", "libreoffice": "5",
    "Leafpad": "5", "kate": "5", "Pluma": "5", "Mousepad": "5", "Subl3": "6", 
    "kwrite": "5", "Geany": "5", "Gedit": "5", "Code": "5",
    "Atom": "5", "Gimp": "6", "Gthumb": "6", "org.kde.gwenview": "6",
    "Ristretto": "6", "lximage-qt": "6", "Eom": "6", "Gpicview": "6",
    "vlc": "7", "xv/mplayer": "7", "Clementine": "7", "MPlayer": "7",
    "smplayer": "7", "mpv": "7", "Gnome-mpv": "7", "Rhythmbotx": "7",
    "Steam": "8", "Wine": "8", "thunar": "8",
    "PlayOnLinux": "8", "VirtualBox": "9", "okular": "9", "calibre": "9",
    "octopi": "9", "Pamac-updater": "9", "Pamac-manager": "9", "Lxtask": "9",
    "Dukto": "9", "QuiteRss": "9", "Filezilla": "9",
    "jetbrains-pycharm-ce": "5",
}

role_grp_dict = {
    "browser": "1", "gimp-image-window": "5", "filemanager": "8",

}

group_exclusives = [
    False, False, False,
    False, False, False,
    False, False, False,
    False,
]

group_persists = [
    True, True, True,
    True, True, True,
    True, True, True,
    True,
]
group_inits = [
    True, True, True,
    True, True, True,
    True, True, True,
    True,
]


group_matches = [
    # 1
    [Match(wm_class=[
        "luakit", "Firefox", "Opera", "Google-chrome",
        "Chromium", "Vivaldi-stable", "Midori",
        "Dillo", "Netsurf-gtk3", "QupZilla",
        "Uget-gtk", "Tor Browser", "Waterfox",
    ], role=["browser"]), ],
    # 2
    [Match(wm_class=[
        "Zathura", "libreoffice-writer", "libreoffice",
        "Leafpad", "kate", "Pluma", "Mousepad", "kwrite",
        "Geany", "Gedit", "Code", "Atom",
        "jetbrains-pycharm-ce",
    ]), ],
    # 3
    [Match(wm_class=[
        "UXTerm", "Termite", "Terminator",
        "URxvt",
        "XTerm", "mlterm", "Lxterminal",
    ]), ],
    # 4
    [Match(wm_class=[
        "discord",
    ]), ],
    # 5
    [Match(wm_class=[
        "Gimp", "Gthumb", "org.kde.gwenview",
        "Ristretto", "lximage-qt", "Eom",
        "Gpicview",
    ], role=["gimp-image-window"]), ],
    # 6
    [Match(wm_class=[
        "Subl3",
     ]),],
    # 7
    [Match(wm_class=[
        "VirtualBox", "okular", "calibre",
        "octopi", "Pamac-updater",
        "Lxtask",
        "Dukto", "QuiteRss",
        "Filezilla",
    ]), ],
    # 8
    [Match(wm_class=[
        "Pcmanfm", "Thunar", "thunar", "dolphin",
        "Caja", "Catfish",
    ], role=["filemanager"]), ],
    # 9
    [Match(wm_class=[
        "vlc", "xv/mplayer", "Clementine",
        "MPlayer", "smplayer", "mpv",
        "Gnome-mpv", "Rhythmbox", "Pamac-manager",  
    ]), ],
    # 0
    [Match(wm_class=[
        "Steam", "Wine", "Zenity",
        "PlayOnLinux", 
    ]), ],

]


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)




keys = [

    #########################
    # SUPER + ... KEYS      #
    #########################
    Key([mod], "a", lazy.spawn('pamac-manager')),
    Key([mod], "c", lazy.spawn('discord')),
    Key([mod], "d", lazy.spawn("rofi -show run")),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "g", lazy.spawn('subl3')),    
    Key([mod], "h", lazy.spawn(myTerm+' -e htop')),
    Key([mod], "m", lazy.layout.maximize()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "r", lazy.spawn('rofi-theme-selector')),
    Key([mod], "t", lazy.spawn('termite')),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod], "w", lazy.spawn(myBrowser)),
    Key([mod], "x", lazy.spawn('oblogout')),
    Key([mod], "Return", lazy.spawn(myTerm)),
    Key([mod], "Left", lazy.screen.prev_group()),
    Key([mod], "Right", lazy.screen.next_group()),
    #########################
    # SUPER + FUNCTION KEYS #
    #########################
    Key([mod], "F1", lazy.spawn(myBrowser)),
    Key([mod], "F2", lazy.spawn('atom')),
    Key([mod], "F3", lazy.spawn('inkscape')),
    Key([mod], "F4", lazy.spawn('gimp')),
    Key([mod], "F5", lazy.spawn('meld')),
    Key([mod], "F6", lazy.spawn('vlc --video-on-top')),
    Key([mod], "F7", lazy.spawn('virtualbox')),
    Key([mod], "F8", lazy.spawn('thunar')),
    Key([mod], "F9", lazy.spawn('evolution')),
    Key([mod], "F10", lazy.spawn("spotify")),
    Key([mod], "F11", lazy.spawn('rofi -show run -fullscreen')),
    Key([mod], "F12", lazy.spawn('rofi -show run')),
    #########################
    # SUPER + SHIFT KEYS    #
    #########################
    Key([mod, "shift"], "m", lazy.spawn("dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=14'")),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "Return", lazy.spawn('thunar')),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "space", lazy.prev_layout()),
    #########################
    # CONTROL + ALT KEYS    #
    #########################
    Key(["mod1", "control"], "a", lazy.spawn('atom')),
    Key(["mod1", "control"], "b", lazy.spawn('thunar')),
    Key(["mod1", "control"], "c", lazy.spawn('Catfish')),
    Key(["mod1", "control"], "e", lazy.spawn('evolution')),
    Key(["mod1", "control"], "f", lazy.spawn('firefox')),
    Key(["mod1", "control"], "g", lazy.spawn('chromium -no-default-browser-check')),
    Key(["mod1", "control"], "i", lazy.spawn('nitrogen')),
    Key(["mod1", "control"], "k", lazy.spawn('slimlock')),
    Key(["mod1", "control"], "m", lazy.spawn('xfce4-settings-manager')),
    Key(["mod1", "control"], "o", lazy.spawn('~/.config/bspwm/scripts/compton-toggle.sh')),
    Key(["mod1", "control"], "r", lazy.spawn('rofi-theme-selector')),
    Key(["mod1", "control"], "s", lazy.spawn('subl3')),
    Key(["mod1", "control"], "t", lazy.spawn('termite')),
    Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),
    Key(["mod1", "control"], "v", lazy.spawn(myBrowser)),
    Key(["mod1", "control"], "w", lazy.spawn('atom')),
    Key(["mod1", "control"], "Return", lazy.spawn('termite')),
    #########################
    # ALT + ... KEYS        #
    #########################
    Key(["mod1"], "f", lazy.spawn('variety -f')),
    Key(["mod1"], "t", lazy.spawn('variety -t')),
    Key(["mod1"], "n", lazy.spawn('variety -n')),
    Key(["mod1"], "p", lazy.spawn('variety -p')),
    Key(["mod1"], "Left", lazy.spawn('variety -p')),
    Key(["mod1"], "Right", lazy.spawn('variety -n')),
    Key(["mod1"], "Up", lazy.spawn('variety --pause')),
    Key(["mod1"], "Down", lazy.spawn('variety --resume')),
    Key(["mod1"], "Tab", lazy.layout.next()),
    Key(["mod1"], "space", lazy.layout.previous()),
    Key(["mod1"], "F2", lazy.spawn('gmrun')),
    Key(["mod1"], "F3", lazy.spawn('xfce4-appfinder')),
    #########################
    #VARIETY KEYS WITH PYWAL#
    #########################
    Key(["mod1", "shift"], "t", lazy.spawn('variety -t && wal -i $(cat $HOME/.config/variety/wallpaper/wallpaper.jpg.txt)&')),
    Key(["mod1", "shift"], "p", lazy.spawn('variety -p && wal -i $(cat $HOME/.config/variety/wallpaper/wallpaper.jpg.txt)&')),
    Key(["mod1", "shift"], "f", lazy.spawn('variety -f && wal -i $(cat $HOME/.config/variety/wallpaper/wallpaper.jpg.txt)&')),
    Key(["mod1", "shift"], "u", lazy.spawn('walu.sh')),
    #########################
    # CONTROL + SHIFT KEYS  #
    #########################
    #yield control + shift + 'Escape', lazy.spawn('xfce4-taskmanager')
    #########################
    #     SCREENSHOTS       #
    #########################
    Key([mod, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),
    Key([mod], "Print", lazy.spawn('xfce4-screenshooter')),
    Key([], "Print", lazy.spawn("scrot ~/Képek/ArcoLinuxD_%Y_%m_%d_%H_%M_%S.jpg")),
    #########################
    #     MULTIMEDIA KEYS   #
    #########################

    #########################
    # Qtile LAYOUT KEYS     #
    #########################
    Key([mod], "k", lazy.layout.down()),
    Key([mod, "mod1"], "Down", lazy.layout.down()),
    Key([mod, "mod1"], "Up", lazy.layout.up()),
    Key([mod, "mod1"], "Right", lazy.layout.right()),
    Key([mod, "mod1"], "Left", lazy.layout.left()),
    #Grow size up, down, left, and right
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

    
#########################################################
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),

    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
##########################################################
    # Switch window focus to other pane(s) of stack
    
    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    
    # Toggle between different layouts as defined below
    
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),
    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    

    # Media player controls
    Key([], "XF86AudioPlay", lazy.spawn("/usr/bin/playerctl play")),
    Key([], "XF86AudioPause", lazy.spawn("/usr/bin/playerctl pause")),
    Key([], "XF86AudioNext", lazy.spawn("/usr/bin/playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("/usr/bin/playerctl previous")),


    # Pulse Audio controls
    Key([], "XF86AudioMute", lazy.spawn("/usr/bin/pactl set-sink-mute alsa_output.pci-0000_00_1b.0.analog-stereo toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo +5%"))
]


groups = []

group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

group_labels = ["", "", "", "", "", "", "", "", "", "",]

group_layouts = ["monadtall", "monadtall", "bsp", "max", "max", "max", "max", "max", "max", 
"max",]


for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            matches=group_matches[i],
            exclusive=group_exclusives[i],
            layout=group_layouts[i].lower(),
            persist=group_persists[i],
            init=group_inits[i],
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])





#my_group = ["", "", "", "", "", "", "",]

# group layout

#for i in my_group:
#    if i == "":
#        groups.append(Group(i, layout = "monadtall"))
#    elif i == "":
#        groups.append(Group(i, layout = "monadtall"))
#    elif i == "":
#        groups.append(Group(i, layout = "bsp"))
#    else:
#        groups.append(Group(i, layout = "max"))

#groups.append(ScratchPad("s", [
#        # define a drop down terminal.
#        # it is placed in the upper third of screen by default.
#        DropDown("term", "urxvt", opacity=0.8),

        # define another terminal exclusively for qshell at different position
#        DropDown("qshell", "urxvt -hold -e qshell",
#                 x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
#                 on_focus_lost_hide=True)
#        
#         ])), 

# Add numeric key Group
#for c, name in enumerate(my_group, 1):
#    keys.append(
#            Key([mod], str(c), lazy.group[name].toscreen())
#            )
#    keys.append(
#            Key([mod, "shift"], str(c), lazy.window.togroup(name))
#            )



def init_layout_theme():
    return {"border_width": 3,
            "margin": 6,
            "border_focus": "#800000",
            "border_normal": "#50EDCE"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.Max(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme)
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

  

def init_screens():
    return [Screen(bottom=bar.Gap(size=35),
                   top=bar.Gap(size=35))
            ]
            #Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=35)), 
            #Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=35))]
screens = init_screens()


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

@hook.subscribe.client_managed
def go_to_group(window):
    if (window.window.get_wm_class()[1] in cls_grp_dict.keys()
      or window.window.get_wm_window_role() in role_grp_dict.keys()):
       window.group.cmd_toscreen()





follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': "Openbox Logout"}, 
    {'wname': "Spotify"},
    {'wname': 'branchdialog'},      # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"
wmname = "qtile"
