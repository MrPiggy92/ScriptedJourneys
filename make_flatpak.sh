#!/bin/bash
flatpak-builder --repo=repo --force-clean build-dir flatpak/com.MrPiggy.AdventureGame.json
flatpak build-bundle repo AdventureGame.flatpak com.MrPiggy.AdventureGame

