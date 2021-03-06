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
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer, Pacman, LaunchBar, CheckUpdates


try:
    from typing import List  # noqa: F401
except ImportError:
    pass

mod = "mod4"

def app_or_group(group, app):
    def f(qtile):
        if qtile.groupMap[group].windows:
            qtile.groupMap[group].cmd_toscreen()
        else:
            qtile.groupMap[group].cmd_toscreen()
            qtile.cmd_spawn(app)
    return f


keys = [
            Key(
                [mod], "Return", 
                lazy.spawn(myTerm)                        # Open terminal
                ),
            Key(
                [mod], "Tab", 
                lazy.next_layout()                        # Toggle through layouts
                ),
            Key(
                [mod], "q", 
                lazy.window.kill()                        # Kill active window
                ),
            Key(
                [mod, "shift"], "r", 
                lazy.restart()                            # Restart Qtile
                ),
            Key(
                [mod, "shift"], "q", 
                lazy.shutdown()                           # Shutdown Qtile
                ),
            Key([mod], "i",
                lazy.to_screen(0)                         # Keyboard focus screen(0)
                ),
            Key([mod], "o",
                lazy.to_screen(1)                         # Keyboard focus screen(1)
                ),
            Key([mod], "p",
                lazy.to_screen(2)                         # Keyboard focus screen(2)
                ),
            # Window controls
            Key(
                [mod], "k", 
                lazy.layout.down()                        # Switch between windows in current stack pane
                ),
            Key(
                [mod], "j", 
                lazy.layout.up()                          # Switch between windows in current stack pane
                ),
            Key(
                [mod, "shift"], "k", 
                lazy.layout.shuffle_down()                # Move windows down in current stack
                ),
            Key(
                [mod, "shift"], "j", 
                lazy.layout.shuffle_up()                  # Move windows up in current stack
                ),
            Key(
                [mod, "shift"], "l", 
                lazy.layout.grow(),                       # Grow size of current window (XmonadTall)
                lazy.layout.increase_nmaster(),           # Increase number in master pane (Tile)
                ),
            Key(
                [mod, "shift"], "h", 
                lazy.layout.shrink(),                     # Shrink size of current window (XmonadTall)
                lazy.layout.decrease_nmaster(),           # Decrease number in master pane (Tile)
                ),
            Key(
                [mod], "n", 
                lazy.layout.normalize()                   # Restore all windows to default size ratios 
                ),
            Key(
                [mod], "m", 
                lazy.layout.maximize()                    # Toggle a window between minimum and maximum sizes
                ),
                
            Key(
                [mod, "shift"], "KP_Enter", 
                lazy.window.toggle_floating()             # Toggle floating
                ),
            Key(
                [mod, "shift"], "space", 
                lazy.layout.rotate(),                     # Swap panes of split stack (Stack)
                lazy.layout.flip()                        # Switch which side main pane occupies (XmonadTall)
                ),
            # Stack controls
            Key(
                [mod], "space", 
                lazy.layout.next()                        # Switch window focus to other pane(s) of stack
                ),
            Key(
                [mod, "control"], "Return", 
                lazy.layout.toggle_split()                # Toggle between split and unsplit sides of stack
                ),
            # GUI Apps
            Key(
                [mod], "w", 
                lazy.function(app_or_group("", "chromium"))
                ),
            Key(
                [mod, "shift"], "w", 
                lazy.function(app_or_group("", "chromium https://arcolinux.info"))
                ),
            Key(
                [mod], "Print", 
                lazy.spawn("spectacle")
                ),    
            Key(
                [mod], "c", 
                lazy.function(app_or_group("", "discord"))
                ),
            Key(
                [mod], "t", 
                lazy.spawn("spotify")
                ),
            Key(
                [mod], "f", 
                lazy.function(app_or_group("", "thunar"))
                ),
            Key(
                [mod], "F1", 
                lazy.spawn("pamac-manager")
                ),
            Key(
                [mod], "g", 
                lazy.function(app_or_group("", "subl3"))
                ),
            # Terminal Apps
            Key(
                [mod], "d",                                  # Keypad 0
                lazy.spawn("rofi -show run")                                      # Run Dialog
                ),
            Key(
                [mod], "KP_End",                                     # Keypad 1
                lazy.spawn(myTerm+" -e ranger")
                ),
            Key(
                [mod], "KP_Down",                                    # Keypad 2
                lazy.spawn(myTerm+" -e htop")
                ),
            Key(
                [mod], "KP_Page_Down",                               # Keypad 3
                lazy.spawn(myTerm+" -e irssi") 
                ), 
            Key(
                [mod], "KP_Left",                                    # Keypad 4
                lazy.spawn(myTerm+" -e lynx http://www.omgubuntu.co.uk")
                ),
            Key(
                [mod], "KP_Begin",                                   # Keypad 5
                lazy.spawn(myTerm+" -e mutt")
                ), 
            Key(
                [mod], "KP_Right",                                   # Keypad 6
                lazy.spawn(myTerm+" -e canto-curses")
                ),
            Key(
                [mod], "KP_Home",                                    # Keypad 7
                lazy.spawn(myTerm+" -e alsamixer")
                ),
            Key(
                [mod], "KP_Up",                                      # Keypad 8
                lazy.spawn(myTerm+" -e ncmpcpp")
                ),
            Key(
                [mod], "KP_Page_Up",                                 # Keypad 9
                lazy.spawn(myTerm+" -e mpsyt")
                ),
            ]

groups = [Group("", layout = "Max"),
          Group(""),
          Group("", layout="Bsp"),
          Group(""),
          Group(""),
          Group(""),
          Group("")
        ]

#for i in groups:
#    keys.extend([
#        # mod1 + letter of group = switch to group
#        Key([mod], i.name, lazy.group[i.name].toscreen()),
#
#        # mod1 + shift + letter of group = switch to & move focused window to group
#        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
#    ])

    
def init_layout_theme():
    return {"border_width": 3,
            "margin": 3,
            "border_focus": "#AF1231",
            "border_normal": "#000000"
            }


layouts = [
    layout.Max(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Stack(num_stacks=2)
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(bottom=bar.Gap(size=35),
            top=bar.Gap(size=35))
            ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = simple_key_binder(mod)
dgroups_app_rules = []  # type: List
layout_theme = init_layout_theme()
main = None
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
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
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
