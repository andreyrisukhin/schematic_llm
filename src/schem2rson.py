"""
Converts between .schem and rson files.
"""

import json
import os

import litemapy as lm
import minecraftschematics as ms
import nbtlib

import numpy as np

from nbtlib import File

from alpha_materials import id_to_block

def schem_to_rson(file_path, CLUSTER_COORDS=False):
    """"
    Converts a .schem file to a rson file.
    """
    if CLUSTER_COORDS: # Reformat palette and blocks to be "block": [(x,y,z), (x,y,z), ...]
        nbt_file = nbtlib.load(file_path)
        schem = nbt_file["Schematic"]
        blocks = schem["Blocks"]
        rson_palette = {key: int(value) for key, value in blocks["Palette"].items()}
        # print(f'{rson_palette=}')

        rson_data = [int(value) for value in blocks["Data"]] # Convert byte to int
        
        clustered_blocks = {}
        for block, block_id in rson_palette.items():
            clustered_blocks[block] = []

        # Reverse dictionary
        rson_reverse_palette = {v: k for k, v in rson_palette.items()}

        for i, block_id in enumerate(rson_data):
            # print(f'{i=}, {block_id=}')
            block = rson_reverse_palette[block_id]
            x = i % int(schem["Width"])
            y = (i // int(schem["Width"])) % int(schem["Height"])
            z = i // (int(schem["Width"]) * int(schem["Height"]))
            clustered_blocks[block].append((x, y, z))

        data = {
            "width": int(schem["Width"]),
            "height": int(schem["Height"]),
            "length": int(schem["Length"]),
            "block_positions": clustered_blocks
        }

    else:
        nbt_file = nbtlib.load(file_path)
        
        schem = nbt_file["Schematic"]
        blocks = schem["Blocks"]
        rson_palette = {key: int(value) for key, value in blocks["Palette"].items()}
        rson_data = [int(value) for value in blocks["Data"]] # Convert byte to int

        data = {
            "width": int(schem["Width"]),
            "height": int(schem["Height"]),
            "length": int(schem["Length"]),
            "block_to_id": rson_palette,
            "id_positions": rson_data
        }

    return data
        
def litematic_to_rson(file_path):
    nbt_file = nbtlib.load(file_path)
    # print(f'{nbt_file=}')

    metadata = nbt_file['Metadata']
    # print(f'{metadata=}')

    x = int(metadata['EnclosingSize']['x'])
    y = int(metadata['EnclosingSize']['y'])
    z = int(metadata['EnclosingSize']['z'])
    # print(f'{x=}, {y=}, {z=}')

    # for k, v in nbt_file['Regions']['Unnamed'].items():
    #     # print(f'{k=}')

    # print(f'{list(nbt_file["Regions"].values())[0]=}')

    # block_states = nbt_file['Regions']['Unnamed']['BlockStates']
    block_states = list(nbt_file["Regions"].values())[0]['BlockStates']
    # Convert from LongArray to list

    # print(f'{int(block_states[0])=}, {type(int(block_states[0]))}')

    block_states = [int(b) for b in block_states]
    # Note, some longs appear to be corrupt in the file (1264455964128444416)

    if any([len(str(b)) > 4 for b in block_states]):
        print(f'Corrupt block states detected in {file_path}')
        return None

    # palette = nbt_file['Regions']['Unnamed']['BlockStatePalette']
    palette = list(nbt_file["Regions"].values())[0]['BlockStatePalette']

    # rson_data_3d = np.reshape(block_states, (x, y, z)).tolist()


    # print(f'{block_states=}')
    # print(f'{palette=}')

    # Write data to json
    data = {
        "volume_width": x,
        "volume_height": y,
        "volume_length": z,
        "block_to_id": palette,
        "id_positions": block_states
    }

    return data

def schematic_to_rson(file_path, CLUSTER_COORDS=False):

    if CLUSTER_COORDS: # Reformat palette and blocks to be "block": [(x,y,z), (x,y,z), ...]
        nbt_file = nbtlib.load(file_path)

        height = int(nbt_file["Height"])
        length = int(nbt_file["Length"])
        width = int(nbt_file["Width"])
        
        block_bytes = nbt_file["Blocks"]
        block_bytes = list(block_bytes)
        block_ids = [int(b) for b in block_bytes]
        blocks = id_to_block(block_ids)

        # Reformat blocks to be "block": [(x,y,z), (x,y,z), ...]
        clustered_blocks = {}
        for block in blocks:
            clustered_blocks[block] = []

        for i, block in enumerate(blocks):
            x = i % width
            y = (i // width) % height
            z = i // (width * height)
            clustered_blocks[block].append((x, y, z))

        # Sort clustered_blocks by alphabetical order
        clustered_blocks = dict(sorted(clustered_blocks.items()))

        data = {
            "width": width,
            "height": height,
            "length": length,
            "block_positions": clustered_blocks
        }

    else:
        nbt_file = nbtlib.load(file_path)

        height = int(nbt_file["Height"])
        length = int(nbt_file["Length"])
        width = int(nbt_file["Width"])
        
        block_bytes = nbt_file["Blocks"]
        block_bytes = list(block_bytes)
        block_ids = [int(b) for b in block_bytes]
        blocks = id_to_block(block_ids)

        # Reshape blocks into 3d array
        blocks_3d = np.reshape(blocks, (height, length, width)).tolist()

        # Write data to json
        data = {
            "width": width,
            "height": height,
            "length": length,
            "block_to_id": "Blocks are directly in positions.",
            "id_positions": blocks_3d
        }

    return data


def main():
    # schem_file = "../dataset/raw/17128.litematic" 
    # schem_file = "../schem/compass.schem"
    schem_file = "../dataset/raw/261.schematic"

    # data = schem_to_rson(schem_file, CLUSTER_COORDS=True)
    # data = litematic_to_rson(schem_file)
    data = schematic_to_rson(schem_file, CLUSTER_COORDS=True)
    print(f'{data=}')

if __name__ == "__main__":
    main()
