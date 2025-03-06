"""
Converts between .schem and rson files.
"""

import json
import os

import litemapy as lm
# import minecraftschematics as ms
import nbtlib

import numpy as np

from nbtlib import File

def schem_to_rson(file_path):
    # Can read the .schem file
    nbt_file = nbtlib.load(file_path)
    # print(f'{nbt_file=}')

    schem = nbt_file["Schematic"]
    width = int(schem["Width"])
    height = int(schem["Height"])
    length = int(schem["Length"])
    # print(f'{width=}, {height=}, {length=}')    
    
    blocks = schem["Blocks"]
    # print(f'{blocks=}')

    palette = blocks["Palette"]
    rson_palette = {}
    for key, value in palette.items():
        rson_palette[key] = int(value)
    # print(f'{rson_palette=}')

    data = blocks["Data"]
    rson_data = []
    for value in data:
        rson_data.append(int(value))
    # print(f'{rson_data=}')

    # reshape the 1d array to 3d using length, width, height
    rson_data_3d = np.reshape(rson_data, (height, length, width)).tolist()
    # print(f'{rson_data_3d=}') # Looks like [[x col] [x col] [x col]], another y layer, 


    # Write data to json
    data = {
        "width": width,
        "height": height,
        "length": length,
        "palette": rson_palette,
        "data": rson_data
    }

    return data
        
def litematic_to_rson(file_path):
    nbt_file = nbtlib.load(file_path)
    print(f'{nbt_file=}')

    metadata = nbt_file['Metadata']
    # print(f'{metadata=}')

    x = int(metadata['EnclosingSize']['x'])
    y = int(metadata['EnclosingSize']['y'])
    z = int(metadata['EnclosingSize']['z'])
    # print(f'{x=}, {y=}, {z=}')

    for k, v in nbt_file['Regions']['Unnamed'].items():
        print(f'{k=}')

    print(f'{nbt_file["Regions"]["Unnamed"]["BlockStates"]=}')
    print(f'{nbt_file["Regions"]["Unnamed"]["BlockStatePalette"]=}')



def main():
    # Example usage
    schem_file = "../dataset/raw/22096.litematic" #"../schem/compass.schem"
    # rson_file = "../schem/2x2door.json"

    # rson_data = schem_to_rson(schem_file)
    litematic_to_rson(schem_file)


if __name__ == "__main__":
    main()
