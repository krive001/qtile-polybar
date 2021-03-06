#!/bin/bash
set -e

sudo pacman -Syy

# pacman packages qtile
sudo pacman -S feh polkit-gnome xcompmgr  python-xdg python-requests  --needed --noconfirm

# Thunar
sudo pacman -S thunar gvfs tumbler thunar-volman thunar-archive-plugin thunar-media-tags-plugin  --needed --noconfirm

# smplayer
sudo pacman -S smplayer smplayer-skins smplayer-themes --needed --noconfirm

# Editors
sudo pacman -S leafpad geany --needed --noconfirm

# Notify
sudo pacman -S xfce4-notifyd --needed --noconfirm

# Browser
sudo pacman -S chromium firefox --needed --noconfirm

# firefox  hungarian lang
sudo pacman -S  firefox-i18n-hu --needed --noconfirm

# powerline
sudo pacman -S powerline --needed --noconfirm
yay -S powerline-fonts-git --noconfirm

wget https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf
wget https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf

sudo mv PowerlineSymbols.otf /usr/share/fonts/
sudo mv 10-powerline-symbols.conf /etc/fonts/conf.d/

# gtk+  and qt set theme icon eg.
sudo pacman -S lxappearance qt5ct --needed --noconfirm

# ttf and otf
sudo pacman -S ttf-inconsolata  ttf-font-awesome  --needed --noconfirm

#neofetch
sudo pacman -S neofetch --needed --noconfirm

# AUR packages
yay -S ttf-font-awesome otf-font-awesome pasystray-gtk3-git  --noconfirm

#Pamac
yay -S pamac-aur  --noconfirm

#sublime-text3
yay -S sublime-text-dev --noconfirm

#polybar

yay -S polybar siji-git  --noconfirm

sudo pacman -S rxvt-unicode wmctrl rofi xdg-user-dirs --noconfirm
yay -S urxvt-perls ttf-font-awesome-4  --noconfirm
