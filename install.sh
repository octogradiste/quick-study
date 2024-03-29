#!/usr/bin/env bash

# Path to the extension folder.
DIR=~/.local/share/gnome-shell/extensions/quickstudy@octogradiste/

EXT=quickstudy@octogradiste

# Stores whether or not the user has installed the extension.
INSTALLED=0

# Check if the extension is already installed.
# If it does, ask the user if he wants to overwrite it.
if [ -d "$DIR" ]; then
    read -p "The extension is already installed. Do you want to overwrite it? [y/N] "
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$DIR"
        cp -r "$EXT/" "$DIR"
        echo "└ Extension installed."
        INSTALLED=1
    fi
else
    cp -r "$EXT/" "$DIR"
    echo "Extension installed."
    INSTALLED=1
fi

# Ask the user if he has a config.json file.
# If he does, copy it to the extension folder.
# Otherwise ask if he is a student from the EPFL
# and wants to auto generate the config file.
# If so, ask for the horaire.ics file and the Dashboard.html file.
# Then run the python script.
read -p "Do you have a config.json file? [y/N] "
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -e -p "└ Enter the path to the config.json file: " CONFIG
    cp "$CONFIG" "$DIR"
    echo "  └ Config file copied."
else
    read -p "└ Are you a student from the EPFL? [y/N] "
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  ├ Download the iCalandar file from https://isa.epfl.ch/."
        echo "  ├ Download the your moodle page from https://moodle.epfl.ch/my/."
        read -e -p "  ├ Enter the path to the 'horaire.ics' file: " ICS
        read -e -p "  ├ Enter the path to the 'Dashboard.html' file: " DASHBOARD
        read -e -p "  ├ Enter the base path of your folder structure: " BASE
        python3 "epfl_generate_config.py" "$ICS" "$DASHBOARD" "$BASE" "${DIR}config.json"
        echo "  ├ Config file generated and copied to the extension folder."
        echo "  └ Edit ${DIR}config.json for further customization."
    else
        echo "  ├ Bad luck, you chose the wrong university."
        echo "  └ You will need to edit ${DIR}config.json by yourself."
    fi
fi

if [ $INSTALLED -eq 1 ]; then
    # Ask the user if he wants to enable the extension.  
    read -p "Do you want to enable the extension? [y/N] "
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gnome-extensions enable "$EXT"
        echo "└ Extension enabled."
    fi

    echo "You need to log out and log back in to restart the gnome shell."
    echo "Or, if you're on X11, type 'Alt+F2' and then enter 'restart'."
fi
