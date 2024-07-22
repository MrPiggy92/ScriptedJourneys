#!/bin/bash
flatpak-builder --repo=repo --force-clean build-dir flatpak/io.github.MrPiggy92.Scripted_Journeys.json
flatpak build-bundle repo Scripted_Journeys.flatpak io.github.MrPiggy92.Scripted_Journeys

