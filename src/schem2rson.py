"""
Converts between .schem and rson files.
"""

import json
import os

import litemapy as lm
# import minecraftschematics as ms
import nbtlib

from nbtlib import File

def schem_to_rson(file_path):
    # Can read the .schem file
    nbt_file = nbtlib.load(file_path)
    print(f'{nbt_file=}')

    schem = nbt_file["Schematic"]
    width = int(schem["Width"])
    height = int(schem["Height"])
    length = int(schem["Length"])
    print(f'{width=}, {height=}, {length=}')    
    
    blocks = schem["Blocks"]
    print(f'{blocks=}')

    palette = blocks["Palette"]
    rson_palette = {}
    for key, value in palette.items():
        rson_palette[key] = int(value)
    print(f'{rson_palette=}')

    data = blocks["Data"]
    rson_data = []
    for value in data:
        rson_data.append(int(value))
    print(f'{rson_data=}')

    # reshape the 1d array to 3d using length, width, height

    # Write data to json
        

def main():
    # Example usage
    schem_file = "../schem/2x2door.schem"
    rson_file = "../schem/2x2door.json"

    rson_data = schem_to_rson(schem_file)


if __name__ == "__main__":
    main()
