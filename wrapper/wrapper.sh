#!/bin/bash
echo -ne "\033]0;Scripted Journeys\007"
python3 /app/bin/setup.py
python3 /app/bin/__main__.py
