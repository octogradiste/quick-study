#!/usr/bin/env bash

# Path to the extension folder.
DIR=~/.local/share/gnome-shell/extensions/quickstudy@octogradiste/

EXT=quickstudy@octogradiste

# Check if the extension is already installed.
# If it does, ask the user if he wants to overwrite it.
if [ -d "$DIR" ]; then
    read -p "The extension is already installed. Do you want to overwrite it? [y/N] "
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$DIR"
        cp -r "$EXT/" "$DIR"
        echo "Extension installed."
    fi
else
    cp -r "$EXT/" "$DIR"
    echo "Extension installed."
fi

# Ask the user if he has a config.json file.
# If he does, copy it to the extension folder.
# Otherwise ask if he is a student from the EPFL
# and wants to auto generate the config file.
# If so, ask for the horaire.ics file and run the python script.
read -p "Do you have a config.json file? [y/N] "
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter the path to the config.json file: " CONFIG
    cp "$CONFIG" "$DIR"
    echo "Config file copied."
else
    read -p "Are you a student from the EPFL? [y/N] "
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter the path to the horaire.ics file: " ICS
        python3 "epfl_generate_config.py" "$ICS" "${DIR}config.json"
        echo "Config file generated and copied to the extension folder."
    fi
fi

# Ask the user if he wants to enable the extension.
read -p "Do you want to enable the extension? [y/N] "
if [[ $REPLY =~ ^[Yy]$ ]]; then
    gnome-extensions enable "$EXT"
    echo "Extension enabled."
else
    echo "Extension not enabled."
fi

# Tell the user he needs to log out to restart the gnome shell.
echo "You need to log out to restart the gnome shell."
