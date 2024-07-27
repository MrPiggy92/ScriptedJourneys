#!/bin/sh

CONFIG_DIR="$HOME/.config/ScriptedJourneys"

if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
    cp -r ../lib/maps $CONFIG_DIR
    mkdir -p $CONFIG_DIR/playerdata
    python3 setup.py
fi
