#!/bin/sh

if [ ! -f $XDG_CONFIG_HOME/finished_setup.txt ]; then
    cp -r /app/lib/maps $XDG_DATA_HOME
    cp /app/lib/LICENSE $XDG_DATA_HOME
    touch $XDG_CONFIG_HOME/playerdata.json
    python3 /app/bin/setup.py
    touch $XDG_CONFIG_HOME/finished_setup.txt
fi
