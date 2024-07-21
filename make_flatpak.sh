#!/bin/bash
flatpak-builder --repo=repo --force-clean build-dir flatpak/io.github.MrPiggy92.Text_Adventure.json
flatpak build-bundle repo AdventureGame.flatpak io.github.MrPiggy92.Text_Adventure

