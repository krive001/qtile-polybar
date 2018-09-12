# coding=utf-8
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

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.config import ScratchPad, DropDown
from libqtile.command import lazy, Client
from libqtile import layout, bar, widget, hook
import os
import re
import subprocess
import json

import pickle
import weakref
from contextlib import contextmanager, suppress
from datetime import datetime
from itertools import islice
from logging import getLogger
from pathlib import Path

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, Screen, Rule, Match
from libqtile.widget.base import ORIENTATION_HORIZONTAL
from libqtile.widget.base import _TextBox as BaseTextBox


mod = "mod4"
term = "/usr/bin/termite"
home = os.path.expanduser('~')
client = Client()

cls_grp_dict = {
    "luakit": "1", "Firefox": "1", "Opera": "1", "Google-chrome": "1",
    "Chromium": "1", "Vivaldi-stable": "1", "Midori": "2", "Dillo": "2",
    "Netsurf-gtk3": "2", "QupZilla": "2", "Uget-gtk": "2", "Tor Browser": "1",
    "Waterfox": "1", "UXTerm": "3", "termite": "3", "Terminator": "3",
    "termite": "3", "termite": "3", "mlterm": "3", "Lxterminal": "3",
    "XTerm": "3", "Pcmanfm": "8", "Thunar": "8", "dolphin": "8", "Caja": "8",
    "Catfish": "8", "Zathura": "5", "libreoffice-writer": "5", "libreoffice": "5",
    "Leafpad": "5", "kate": "5", "Pluma": "5", "Mousepad": "5",
    "kwrite": "5", "Geany": "5", "Gedit": "5", "Code": "5",
    "Atom": "5", "Gimp": "6", "Gthumb": "6", "org.kde.gwenview": "6",
    "Ristretto": "6", "lximage-qt": "6", "Eom": "6", "Gpicview": "6",
    "vlc": "7", "xv/mplayer": "7", "Clementine": "7", "MPlayer": "7",
    "smplayer": "7", "mpv": "7", "Gnome-mpv": "7", "Rhythmbotx": "7",
    "Pragha": "7", "Steam": "8", "Wine": "8", "thunar": "8",
    "PlayOnLinux": "8", "VirtualBox": "9", "okular": "9", "calibre": "9",
    "octopi": "9", "Pamac-updater": "9", "Pamac-manager": "9", "Lxtask": "9",
    "Dukto": "9", "QuiteRss": "9", "Filezilla": "9",
    "jetbrains-pycharm-ce": "5",
}

role_grp_dict = {
    "browser": "1", "gimp-image-window": "5", "filemanager": "8",

}

group_labels = [
    "", "", "",
    "", "", "",
    "", "", "",
    "",
]

group_names = [
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9",
    "0",
]

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

group_layouts = [
    "tile", "max", "monadwide",
    "monadtall", "stack", "zoomy",
    "max", "max", "columns",
    "bsp",
]

group_matches = [

    [Match(wm_class=[
        "luakit", "Firefox", "Opera", "Google-chrome",
        "Chromium", "Vivaldi-stable", "Midori",
        "Dillo", "Netsurf-gtk3", "QupZilla",
        "Uget-gtk", "Tor Browser", "Waterfox",
    ], role=["browser"]), ],

    [Match(wm_class=[
        "Zathura", "libreoffice-writer", "libreoffice",
        "Leafpad", "kate", "Pluma", "Mousepad", "kwrite",
        "Geany", "Gedit", "Code", "Atom",
        "jetbrains-pycharm-ce",
    ]), ],

    [Match(wm_class=[
        "UXTerm", "Termite", "Terminator",
        "termite-tabbed", "termite",
        "XTerm", "mlterm", "Lxterminal",
    ]), ],

    [Match(wm_class=[
        "discord",
    ]), ],

    [Match(wm_class=[
        "Gimp", "Gthumb", "org.kde.gwenview",
        "Ristretto", "lximage-qt", "Eom",
        "Gpicview",
    ], role=["gimp-image-window"]), ],

    None,

    [Match(wm_class=[
        "VirtualBox", "okular", "calibre",
        "octopi", "Pamac-updater",
        "Pamac-manager", "Lxtask",
        "Dukto", "QuiteRss",
        "Filezilla",
    ]), ],

    [Match(wm_class=[
        "Pcmanfm", "Thunar", "thunar", "dolphin",
        "Caja", "Catfish",
    ], role=["filemanager"]), ],

    [Match(wm_class=[
        "vlc", "xv/mplayer", "Clementine",
        "MPlayer", "smplayer", "mpv",
        "Gnome-mpv", "Rhythmbox", "Pragha",
    ]), ],

    [Match(wm_class=[
        "Steam", "Wine", "Zenity",
        "PlayOnLinux",
    ]), ],

]


def regex(name):
    return r'.*(^|\s|\t|\/)' + name + r'(\s|\t|$).*'


def window_to_prev_group():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.groups.index(qtile.currentGroup)
            if index > 0:
                qtile.currentWindow.togroup(qtile.groups[index - 1].name)
            else:
                qtile.currentWindow.togroup(qtile.groups[len(qtile.groups) - 2].name)

    return __inner


def window_to_next_group():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.groups.index(qtile.currentGroup)
            if index < len(qtile.groups) - 2:
                qtile.currentWindow.togroup(qtile.groups[index + 1].name)
            else:
                qtile.currentWindow.togroup(qtile.groups[0].name)

    return __inner


def window_to_prev_screen():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.screens.index(qtile.currentScreen)
            if index > 0:
                qtile.currentWindow.togroup(qtile.screens[index - 1].group.name)
            else:
                qtile.currentWindow.togroup(qtile.screens[len(qtile.screens) - 1].group.name)

    return __inner


def window_to_next_screen():
    @lazy.function
    def __inner(qtile):
        if qtile.currentWindow is not None:
            index = qtile.screens.index(qtile.currentScreen)
            if index < len(qtile.screens) - 1:
                qtile.currentWindow.togroup(qtile.screens[index + 1].group.name)
            else:
                qtile.currentWindow.togroup(qtile.screens[0].group.name)

    return __inner


def go_to_next_group():
    @lazy.function
    def __inner(qtile):
        index = qtile.groups.index(qtile.currentGroup)
        if index < len(qtile.groups) - 2:
            qtile.groups[index + 1].cmd_toscreen()
        else:
            qtile.groups[0].cmd_toscreen()

    return __inner


def go_to_prev_group():
    @lazy.function
    def __inner(qtile):
        index = qtile.groups.index(qtile.currentGroup)
        if index > 0:
            qtile.groups[index - 1].cmd_toscreen()
        else:
            qtile.groups[len(qtile.groups) - 2].cmd_toscreen()

    return __inner


def find_or_run(app, classes=(), group="", processes=()):
    if not processes:
        processes = [regex(app.split('/')[-1])]

    def __inner(qtile):
        if classes:
            for window in qtile.windowMap.values():
                for c in classes:
                    if window.group and window.match(wmclass=c):
                        qtile.currentScreen.setGroup(window.group)
                        window.group.focus(window, False)
                        return
        if group:
            lines = subprocess.check_output(["/usr/bin/ps", "axw"]).decode("utf-8").splitlines()
            ls = [line.split()[4:] for line in lines][1:]
            ps = [' '.join(l) for l in ls]
            for p in ps:
                for process in processes:
                    if re.match(process, p):
                        qtile.groupMap[group].cmd_toscreen()
                        return
        subprocess.Popen(app.split())

    return __inner


def to_urgent():
    @lazy.function
    def __inner(qtile):
        cg = qtile.currentGroup
        for group in qtile.groupMap.values():
            if group == cg:
                continue
            if len([w for w in group.windows if w.urgent]) > 0:
                qtile.currentScreen.setGroup(group)
                break

    return __inner

def exit_menu():
    @lazy.function
    def __inner(qtile):
        subprocess.Popen(["/usr/bin/sh", home + "/.script/qtile-rofi_exit_menu"])

    return __inner


def get_cur_grp_name():
    return client.group.info()['name']


date_command = ["/usr/bin/date", "+%a %D"]
kernel_command = ["/usr/bin/uname", "-r"]

def get_date():
    return '  ' + subprocess.check_output(date_command).decode('utf-8').strip()

def get_kernel():
    return '  ' + subprocess.check_output(kernel_command).decode('utf-8').strip()

def get_time():
    #return '  ' + subprocess.check_output(['/usr/bin/date', '+%I:%M %p']).decode('utf-8').strip()
    return ' ' + subprocess.check_output(['/usr/bin/date', '+%I:%M %p']).decode('utf-8').strip()

def myclock():
    return libqtile.widget.clock()

def get_datetime():
    return get_date() + get_time()

keys = [

    #########################
    # SUPER + ... KEYS      #
    #########################
    Key([mod], "e", lazy.spawn('atom')),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "h", lazy.spawn('urxvt -e htop')),
    Key([mod], "p", lazy.spawn('pragha')),
    #Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "q", lazy.spawn('firefox')),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "s", lazy.spawn('rofi-theme-selector')),
    Key([mod], "t", lazy.spawn('termite')),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod], "w", lazy.spawn('vivaldi-stable')),
    Key([mod], "x", lazy.spawn('oblogout')),
    Key([mod], "Return", lazy.spawn('termite')),
    #########################
    # SUPER + FUNCTION KEYS #
    #########################
    Key([mod], "F1", lazy.spawn('vivaldi-stable')),
    Key([mod], "F2", lazy.spawn('atom')),
    Key([mod], "F3", lazy.spawn('inkscape')),
    Key([mod], "F4", lazy.spawn('gimp')),
    Key([mod], "F5", lazy.spawn('meld')),
    Key([mod], "F6", lazy.spawn('vlc --video-on-top')),
    Key([mod], "F7", lazy.spawn('virtualbox')),
    Key([mod], "F8", lazy.spawn('thunar')),
    Key([mod], "F9", lazy.spawn('evolution')),
    Key([mod], "F10", lazy.window.toggle_floating()),
    Key([mod], "F11", lazy.spawn('rofi -show run -fullscreen')),
    Key([mod], "F12", lazy.spawn('rofi -show run')),
    #########################
    # SUPER + SHIFT KEYS    #
    #########################
    Key([mod, "shift"], "Return", lazy.spawn('thunar')),
    Key([mod, "shift"], "m", lazy.spawn("dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=14'")),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
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
    Key(["mod1", "control"], "v", lazy.spawn('vivaldi-stable')),
    Key(["mod1", "control"], "w", lazy.spawn('atom')),
    Key(["mod1", "control"], "Return", lazy.spawn('termite')),
    #########################
    # ALT + ... KEYS        #
    #########################
    Key(["mod1"], "t", lazy.spawn('variety -t')),
    #Key(["mod1"], "n", lazy.spawn('variety -n')),
    Key(["mod1"], "n", lazy.spawn('nitrogen --random --set-scaled')),
    Key(["mod1"], "p", lazy.spawn('variety -p')),
    Key(["mod1"], "f", lazy.spawn('variety -f')),
    Key(["mod1"], "Left", lazy.spawn('variety -p')),
    #Key(["mod1"], "Right", lazy.spawn('variety -n')),
    Key(["mod1"], "Right", lazy.spawn('nitrogen --random --set-scaled')),
    Key(["mod1"], "Up", lazy.spawn('variety --pause')),
    Key(["mod1"], "Down", lazy.spawn('variety --resume')),
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
    Key([], "Print", lazy.spawn("/usr/bin/scrot " + home + "/Pictures/screenshot_%Y_%m_%d_%H_%M_%S.png")),
    #########################
    #     MULTIMEDIA KEYS   #
    #########################

    #########################
    # Qtile LAYOUT KEYS     #
    #########################
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "Left", lazy.layout.left()),
    # Grow size up, down, left, and right
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

    Key([mod], "m",
        lazy.layout.maximize(),
        ),

    Key([mod], "n",
        lazy.layout.normalize(),
        ),
#########################################################
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),

    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
##########################################################
    # Switch window focus to other pane(s) of stack
    Key(["mod1"], "Tab", lazy.layout.next()),
    Key(["mod1"], "space", lazy.layout.previous()),
    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    # Switch Groups using a prompt
    Key([mod], "g", lazy.switchgroup()),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "space", lazy.prev_layout()),
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),
    # Swap panes of split stack
    Key([mod, "shift"], "space",
        lazy.layout.rotate()
        ),
    # Reload Qtile
    Key([mod, "shift"], "r", lazy.restart()),
    # Exit Qtile
    Key([mod, "shift"], "x", lazy.shutdown()),

    Key([], "F10", to_urgent()),

    # Media player controls
    Key([], "XF86AudioPlay", lazy.spawn("/usr/bin/playerctl play")),
    Key([], "XF86AudioPause", lazy.spawn("/usr/bin/playerctl pause")),
    Key([], "XF86AudioNext", lazy.spawn("/usr/bin/playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("/usr/bin/playerctl previous")),


    # Pulse Audio controls
    Key([], "XF86AudioMute",
        lazy.spawn("/usr/bin/pactl set-sink-mute alsa_output.pci-0000_00_1b.0.analog-stereo toggle")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo -5%")),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("/usr/bin/pactl set-sink-volume alsa_output.pci-0000_00_1b.0.analog-stereo +5%"))
]

layout_style = {
    'font': 'xos4 terminus reparagular 13',
    'margin': 0,
    'border_width': 3,
    'border_normal': '#000000',
    'border_focus': '8588E5',

}

layouts = [
    layout.Tile(**layout_style),
    layout.Columns(num_columns=2, autosplit=True, **layout_style),
    layout.Stack(num_stacks=1, **layout_style),
    layout.MonadTall(**layout_style),
    layout.MonadWide(**layout_style),
    layout.Bsp(**layout_style),
    # layout.Matrix(**layout_style),
    layout.Zoomy(**layout_style),
    layout.Max(**layout_style),
    # layout.Floating(**layout_style),
]

groups = []

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

groups.append(
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("term", "/usr/bin/termite", opacity=0.88, height=0.55, width=0.80, ),

        # define another terminal exclusively for qshell at different position
        DropDown("qshell", "/usr/bin/termite -e qshell",
                 x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
                 on_focus_lost_hide=True)
    ]), )

keys.extend([
    # Scratchpad
    # toggle visibiliy of above defined DropDown named "term"
    Key([], 'F12', lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([], 'F11', lazy.group['scratchpad'].dropdown_toggle('qshell')),
])

widget_defaults = dict(
    font='NotoSans',
    fontsize=14,
    padding=5,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.7, foreground="00BCD4", padding=0, ),
                widget.GenPollText(func=get_cur_grp_name, update_interval=0.5, foreground='FFBB00', padding=5, font='NotoSans bold', fontsize=16, ),
                widget.Sep(foreground='968F92', linewidth=2, padding=5, size_percent=50, ),
                widget.GroupBox(active='6790eb', inactive='F3F4F5', #968F92
                                this_current_screen_border='FFBB00', #00BCD4
                                this_screen_border='00BCD4',
                                highlight_method='line',
                                highlight_color=['2F343F', '2F343F'],
                                fontsize=20,
                                padding=3,
                                ),
                widget.Sep(foreground='968F92', linewidth=2, padding=5, size_percent=50, ),
                widget.Prompt(font= 'NotoSans', fontsize=14, cursor_color='FFBB00', foreground='FDF3A9', background='2F343F'),
                widget.WindowName(fontsize=13, foreground='7AA0BC', ),
    #            widget.Clock(font='NotoSans', fontsize=14, update_interval=1, foreground='B1D0FF', ),
    #            widget.Memory(fmt='{MemTotal}M', fontsize=21, foreground='F3F4F5', padding=5, update_interval=600, ),
                widget.GenPollText(func=get_kernel, update_interval=0.5, foreground='6790eb', padding=5, font='NotoSans', fontsize=14, ),
                widget.Sep(foreground='968F92', linewidth=2, padding=10, size_percent=50, ),
                widget.CPUGraph(border_color='3EC13F', border_width=1, core='all', fill_color='3EC13F.3', frequency=1, graph_color='3EC13F', line_width=1, margin_x=3, margin_y=3, samples=100, start_pos='bottom', type='linefill', ),
                widget.MemoryGraph(border_color='215578', border_width=1, fill_color='1667EB.3', frequency=1, graph_color='18BAEB', line_width=1, margin_x=3, margin_y=3, samples=100, start_pos='bottom', type='linefill', ),
                widget.Sep(foreground='968F92', linewidth=2, padding=10, size_percent=50, ),
                widget.DF(foreground='F3F4F5', font='NotoSans', fongtsize=22, partition='/', measure='G', padding=5, update_interval=60, visible_on_warn=False, warn_color='ff0000', warn_space=2, format=' {p}: {uf}{m} free of {s}{m} - {r:.0f}% used',  ),
                #widget.DF(foreground='F3F4F5', partition='/', measure='G', padding=5, update_interval=60, visible_on_warn=False, warn_color='ff0000', warn_space=2, format='{p} ({uf}{m}|{r:.0f}%)',  ),
                widget.Sep(foreground='968F92', linewidth=2, padding=10, size_percent=50, ),
    #            widget.Volume(foreground='F3F4F5',  ),
                widget.Systray(background='2F343F', foreground='B1D0FF', icon_size=18, padding=5, ),
                widget.Sep(foreground='968F92', linewidth=2, padding=10, size_percent=50, ),
    #            widget.YahooWeather(font='NotoSans', fontsize='14', metric=False, woeid='12791633', user_agent='Qtile', padding=5, format='{location_city}: {condition_temp} °{units_temperature}', update_interval='600', xml=False, up='^', down='v', json=True, ),
                widget.Sep(foreground='968F92', linewidth=2, padding=10, size_percent=50, ),
                widget.GenPollText(func=get_datetime, update_interval=1, font='NotoSans', fongtsize=22, foreground='F3F4F5', ),
    #            widget.GenPollText(func=myclock, update_interval=1, foreground='B1D0FF', ),
            ],
            36,
            background=['2F343F', '2F343F'], #1A2024,#060A0F
            opacity=0.96,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

floating_layout = layout.Floating(float_rules=[
    {"role": "EventDialog"},
    {"role": "Msgcompose"},
    {"role": "Preferences"},
    {"role": "pop-up"},
    {"role": "prefwindow"},
    {"role": "task_dialog"},
    {"wname": "Module"},
    {"wname": "Terminator Preferences"},
    {"wname": "Search Dialog"},
    {"wname": "Goto"},
    {"wname": "IDLE Preferences"},
    {"wname": "Sozi"},
    {"wname": "Create new database"},
    {"wname": "Preferences"},
    {"wname": "File Transfer"},
    {"wname": 'branchdialog'},
    {"wname": 'pinentry'},
    {"wname": 'confirm'},
    {"wmclass": 'dialog'},
    {"wmclass": 'download'},
    {"wmclass": 'error'},
    {"wmclass": 'file_progress'},
    {"wmclass": 'notification'},
    {"wmclass": 'splash'},
    {"wmclass": 'toolbar'},
    {"wmclass": 'confirmreset'},
    {"wmclass": 'makebranch'},
    {"wmclass": 'maketag'},
    {"wmclass": 'Dukto'},
    {"wmclass": 'Guake'},
    {"wmclass": 'Tilda'},
    {"wmclass": 'yakuake'},
    {"wmclass": 'Xfce4-appfinder'},
    {"wmclass": "GoldenDict"},
    {"wmclass": "Synapse"},
    {"wmclass": "Pamac-updater"},
    {"wmclass": "TelegramDesktop"},
    {"wmclass": "Galculator"},
    {"wmclass": "notify"},
    {"wmclass": "Lxappearance"},
    {"wmclass": "Nitrogen"},
    {"wmclass": "Oblogout"},
    {"wmclass": "Pavucontrol"},
    {"wmclass": "VirtualBox"},
    {"wmclass": "Skype"},
    {"wmclass": "Steam"},
    {"wmclass": "nvidia-settings"},
    {"wmclass": "Eog"},
    {"wmclass": "Rhythmbox"},
    {"wmclass": "obs"},
    {"wmclass": "Gufw.py"},
    {"wmclass": "Catfish"},
    {"wmclass": "libreoffice-calc"},
    {"wmclass": "LibreOffice 3.4"},
    {"wmclass": 'ssh-askpass'},
    {"wmclass": "Mlconfig"},
    #{"wmclass": "Termite"},
])
auto_fullscreen = True
focus_on_window_activation = "smart"

floating_types = ["notification", "toolbar", "splash", "dialog",
                  "utility", "menu", "dropdown_menu", "popup_menu", "tooltip,dock",
                  ]


@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


@hook.subscribe.client_managed
def go_to_group(window):
    if (window.window.get_wm_class()[1] in cls_grp_dict.keys()
            or window.window.get_wm_window_role() in role_grp_dict.keys()):
        window.group.cmd_toscreen()


# Qtile startup commands, not repeated at qtile restart
@hook.subscribe.startup_once
def autostart():
    from datetime import datetime
    try:
        subprocess.call([home + '/.config/qtile/autostart.sh'])
    except Exception as e:
        with open('qtile_log', 'a+') as f:
            f.write(
                datetime.now().strftime('%Y-%m-%dT%H:%M') +
                + ' ' + str(e) + '\n')






    # multiple stack panes
    #Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    #Key([mod], "Return", lazy.spawn()),
    #Key([mod], "x", lazy.window.kill()),
    #Key([mod, "shift"], "Pause", exit_menu()),
    #Key([mod, "shift"], "Scroll_Lock", lazy.spawn("/usr/bin/slock")),
    #Key([mod, "shift", "control"], "Print", lazy.spawn("/usr/bin/systemctl -i suspend")),

    # Applications
    #Key([mod], "d", lazy.spawn("/usr/bin/rofi -modi run,drun -show drun run")),
    #Key([mod], "Delete", lazy.function(find_or_run("/usr/bin/lxtask", ("Lxtask",),
    #                                                cls_grp_dict["Lxtask"]))),
    #Key([mod], "F1", lazy.function(find_or_run("/usr/bin/catfish", ("Catfish",),
    #                                          cls_grp_dict["Catfish"], ("^/usr/bin/python /usr/bin/catfish$",)))),
    #Key([mod], "e", lazy.function(find_or_run("/usr/bin/leafpad",
    #                                          ("Leafpad", "Mousepad", "Pluma"), cls_grp_dict["Leafpad"],
    #                                          (regex("leafpad"),
    #                                           regex("mousepad"), regex("pluma"))))),
    #Key([mod, "shift"], "e", lazy.function(find_or_run("/usr/bin/geany", ("Geany", "kate"),
    #                                                   cls_grp_dict["Geany"], (regex("geany"), regex("kate"))))),
    #Key([mod], "Home", lazy.function(find_or_run("/usr/bin/pcmanfm", ("Pcmanfm", "Thunar", "dolphin"),
    #                                             cls_grp_dict["Pcmanfm"],
    #                                             (regex("pcmanfm"), regex("thunar"), regex("dolphin"))))),
    #Key([mod, "shift"], "Home", lazy.function(find_or_run(term + " -e /usr/bin/ranger", (),
    #                                                      cls_grp_dict["termite"]))),
    #Key([mod], "p", lazy.function(find_or_run("/usr/bin/pragha", ("Pragha", "Clementine"),
    #                                          cls_grp_dict["Pragha"], [regex("pragha"), regex("clementine")]))),
    #Key([mod], "c", lazy.function(find_or_run(term + " -e /usr/bin/cmus", (),
    #                                          cls_grp_dict["termite"]))),
    #Key([mod], "w", lazy.function(find_or_run("/usr/bin/firefox", ("Firefox", "Chromium", "Vivaldi-stable"),
    #                                          cls_grp_dict["Firefox"],
    #                                          ("/usr/lib/firefox/firefox", "/usr/lib/chromium/chromium",
    #                                           "/opt/vivaldi/vivaldi-bin")))),
    #Key([mod, "shift"], "w", lazy.function(find_or_run(home +
    #                                                   "/Apps/Internet/tor-browser_en-US/Browser/start-tor-browser "
    #                                                   "--detach ", ("Tor Browser",), cls_grp_dict["Tor Browser"],
    #                                                   ("\./firefox",)))),
    #Key([mod], "i", lazy.function(find_or_run("/usr/bin/pamac-manager", ["Pamac-manager"],
    #                                          cls_grp_dict["Pamac-manager"]))),
