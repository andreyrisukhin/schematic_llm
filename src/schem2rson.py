"""
Converts between .schem and rson files.
"""

import json
import os

import litemapy as lm
# import minecraftschematics as ms
import nbtlib

def schem_to_rson(file_path):
    # Read the .schem file
    # try:

    nbt_file = nbtlib.load(file_path)
    print(f'{nbt_file=}')
    # Look at nbtlib docs to extract file 

    schematic = lm.Schematic.from_nbt(nbt_file)

    # schematic = lm.Schematic.load(file_path)
    # schematic = ms.Schematic.load(file_path)

    # ms.Schematic.

    print(f'{schematic=}')
    print(f'{schematic.block_entities=}')

    # rson_data = {
    #     "schematic_name": schematic.,
    #     "schematic_behavior": schematic.description,
    #     "blocks": {
    #         "door": schematic.regions
    #     }
    # }

    # return rson_data

    # except Exception as e:
    #     print(f"Error loading schematic: {e} ({file_path=})")
    #     # return None


def rson_to_schem(data, file_path):
    # Write the rson data to a .schem file
    try:
        schematic = lm.Schematic(
            name=data["schematic_name"],
            description=data["schematic_behavior"],
            regions=data["blocks"]["door"]
        )
        schematic.save(file_path)

    except Exception as e:
        print(f"Error saving schematic: {e} ({file_path=})")
        # return None

def write_rson_file(data, file):
    with open(file, 'w') as f:
        json.dump(data, f)

def read_rson_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def main():
    # Example usage
    schem_file = "../schem/2x2door.schem"
    rson_file = "../schem/2x2door.json"

    # Convert .schem to rson
    rson_data = schem_to_rson(schem_file)
    write_rson_file(rson_data, rson_file)

    # Convert rson to .schem
    rson_data = read_rson_file(rson_file)
    rson_to_schem(rson_data, "../schem/2x2door_new.schem")


if __name__ == "__main__":
    main()
