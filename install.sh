#!/usr/bin/env bash

# Path to the extension folder.
DIR=~/.local/share/gnome-shell/extensions/quickstudy@octogradiste/

# Name of the extension.
EXT=quickstudy@octogradiste

# Check if the extension is already installed.
# If it does, ask the user if he wants to overwrite it.
# Else copy the extension and config file to the extensions folder.
if [ -d "$DIR" ]; then
    read -p "The extension is already installed. Do you want to overwrite it? [y/N] " -n 1
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$DIR"
        cp -r "$EXT/" "$DIR"
        echo "Extension installed."
    else
        echo "Installation aborted."
    fi
else
    cp -r "$EXT/" "$DIR"
    echo "Extension installed."
fi

# Ask the user if he has a config.json file.
# If he does, copy it to the extension folder.
read -p "Do you have a config.json file? [y/N] " -n 1
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter the path to the config.json file: " CONFIG
    cp "$CONFIG" "$DIR"
    echo "Config file copied."
fi

# Ask the user if he wants to enable the extension.
read -p "Do you want to enable the extension? [y/N] " -n 1
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    gnome-extensions enable "$EXT"
    echo "Extension enabled."
else
    echo "Extension not enabled."
fi

# Tell the user he needs to log out to restart the gnome shell.
echo "You need to log out to restart the gnome shell."
