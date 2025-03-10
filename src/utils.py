# Scripted Journeys

#
# Copyright (C) 2024 MrPiggy92
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

import time
import os
import config

def output(text, colour, delay=0.01):
    text = colourify(colour) + text
    text = wrap_text(text)
    if config.wants_scroll:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
    else:
        print(text, end='')
    print(colourify("clear"))

def colourify(colour):
    colours = {
        "black": "\033[0;30m",
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[0;33m",
        "blue": "\033[0;34m",
        "magenta": "\033[0;35m",
        "cyan": "\033[0;36m",
        "white": "\033[0;37m",
        "bright_black": "\033[0;90m",
        "bright_red": "\033[0;91m",
        "bright_green": "\033[0;92m",
        "bright_yellow": "\033[0;93m",
        "bright_blue": "\033[0;94m",
        "bright_magenta": "\033[0;95m",
        "bright_cyan": "\033[0;96m",
        "bright_white": "\033[0;97m",
        "clear": "\033[0m",
        "orange": "\033[38;2;255;165;0m",
        "bold_pink": "\033[1m\033[38;2;255;105;180m"
    }
    return colours[colour] if config.wants_colour else ''

def wrap_text(text, line_length=150):
    lines = []
    while len(text) > line_length:
        wrap_pos = text.rfind(' ', 0, line_length)
        if wrap_pos == -1:
            wrap_pos = line_length
        lines.append(text[:wrap_pos])
        text = text[wrap_pos:].lstrip()
    lines.append(text)
    return "\n".join(lines)

def fuzzy_match(target, matches, threshold=5):
    bestMatch = ''
    bestSimilarity = 9999
    for string in matches:
        similarity = levenshteinDistance(string, target)
        if similarity < bestSimilarity:
            bestSimilarity = similarity
            bestMatch = string
    if bestSimilarity >= 5:
        return None
    if bestMatch != target:
        output(f"Assuming you mean {bestMatch}.", "magenta")
    return bestMatch
            

def levenshteinDistance(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix =[[0 for _ in range(0, len2+1)] for _ in range(0, len1+1)]
    for i in range(0, len1+1):
        matrix[i][0] = i
    for j in range(0, len2+1):
        matrix[0][j] = j
    for i in range(1, len1+1):
        for j in range(1, len2+1):
            if string1[i-1] == string2[j-1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(matrix[i-1][j]+1, matrix[i][j-1]+1, matrix[i-1][j-1]+cost)
    #print('\n'.join([str(i) for i in matrix]))
    return matrix[len1][len2]
    
