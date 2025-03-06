"""
Converts between .schem and rson files.
"""

import json
import os

import litemapy as lm
# import minecraftschematics as ms
import nbtlib

from nbtlib import File

def nbtlib_schem_to_rson(file_path):
    with open(file_path, 'rb') as f:
        nbt_file = File.parse(f)

    print(f'{nbt_file=}')


def schem_to_rson(file_path):
    # Read the .schem file
    # try:

    nbt_file = nbtlib.load(file_path)
    print(f'{nbt_file=}')
    # Look at nbtlib docs to extract file 



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

    # # reshape the 1d array to 3d using length, width, height
    # for w in range(width):
    #     for h in range(height):
    #         print(f'{h}')
    #         # for l in range(length):
    #         print(f'\t{rson_data[h*w*0:h*w*(length - 1)]}\n')


    # Write data to json
    # rson_struct = {





    # for key, value in nbt_file.items():
    #     print(f'{key=}, {value=}')
    #     if type(value) == nbtlib.Compound:
    #         for k, v in value.items():
    #             print(f'{k=}, {v=}')
    #             if type(v) == nbtlib.Compound:
    #                 for k2, v2 in v.items():
    #                     print(f'{k2=}, {v2=}')
    #                     if type(v2) == nbtlib.Compound:
    #                         for k3, v3 in v2.items():
    #                             print(f'{k3=}, {v3=}')
    #                             if type(v3) == nbtlib.Compound:
    #                                 for k4, v4 in v3.items():
    #                                     print(f'{k4=}, {v4=}')
    #                                     if type(v4) == nbtlib.Compound:
    #                                         for k5, v5 in v4.items():
    #                                             print(f'{k5=}, {v5=}')
    #                                             if type(v5) == nbtlib.Compound:
    #                                                 for k6, v6 in v5.items():
    #                                                     print(f'{k6=}, {v6=}')
    #                                                     if type(v6) == nbtlib.Compound:
    #                                                         for k7, v7 in v6.items():
    #                                                             print(f'{k7=}, {v7=}')
    #                                                             if type(v7) == nbtlib.Compound:
    #                                                                 for k8, v8 in v7.items():
    #                                                                     print(f'{k8=}, {v8=}')
    #                                                                     if type(v8) == nbtlib.Compound:
    #                                                                         for k9, v9 in v8.items():
    #                                                                             print(f'{k9=}, {v9=}')
    #                                                                             if type(v9) == nbtlib.Compound:
    #                                                                                 for k10, v10 in v9.items():
    #                                                                                     print(f'{k10=}, {v10=}')
    #                                                                                     if type(v10) == nbtlib.Compound:
    #                                                                                         for k11, v11 in v10.items():
    #                                                                                             print(f'{k11=}, {v11=}')
    #                                                                                             if type(v11) == nbtlib.Compound:
    #                                                                                                 for k12, v12 in v11.items():
    #                                                                                                     print(f'{k12=}, {v12=}')
    #                                                                                                     if type(v12) == nbtlib.Compound:
    #                                                                                                         for k13, v13 in v12.items():
    #                                                                                                             print(f'{k13=}, {v13=}')
    #                                                                                                             if type(v13) == nbtlib.Compound:
    #                                                                                                                 for k14, v14 in v13.items():
    #                                                                                                                     print(f'{k14=}, {v14=}')
                                                                                                                        

    # schematic = lm.Schematic.from_nbt(nbt_file)

    # schematic = lm.Schematic.load(file_path)
    # schematic = ms.Schematic.load(file_path)

    # ms.Schematic.

    # print(f'{schematic=}')
    # print(f'{schematic.block_entities=}')

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


# def rson_to_schem(data, file_path):
#     # Write the rson data to a .schem file
#     try:
#         schematic = lm.Schematic(
#             name=data["schematic_name"],
#             description=data["schematic_behavior"],
#             regions=data["blocks"]["door"]
#         )
#         schematic.save(file_path)

#     except Exception as e:
#         print(f"Error saving schematic: {e} ({file_path=})")
#         # return None

# def write_rson_file(data, file):
#     with open(file, 'w') as f:
#         json.dump(data, f)

# def read_rson_file(file):
#     with open(file, 'r') as f:
#         data = json.load(f)
#     return data




import re

# def convert_to_json(input_str):
#     # # Replace single-letter suffixes (e.g., `2s`, `4189L`, `5B`) with just the number
#     # input_str = re.sub(r'(\d+)[sSB]', r'\1', input_str)  # Remove `s`, `S`, `B` suffixes
#     # input_str = re.sub(r'(\d+)L', r'\1', input_str)  # Remove `L` suffix
    
#     # Replace unquoted keys with quoted keys
#     input_str = re.sub(r'(\{|,)\s*([\w:]+)\s*:', r'\1 "\2":', input_str)
    
#     # # Replace `[I; ...]` and `[B; ...]` with standard lists
#     # input_str = re.sub(r'\[I; ([^]]+)]', r'[\1]', input_str)
#     # input_str = re.sub(r'\[B; ([^]]+)]', r'[\1]', input_str)
    
#     # Convert to valid JSON
#     input_str = input_str.replace("'", '"')  # Ensure all quotes are double quotes
    
#     return json.loads(input_str)

# def fix_json_like_string(s):
#     # Fix keys (unquoted words before colons)
#     s = re.sub(r'(?<!["{\[])\b([A-Za-z_][A-Za-z0-9_]*)\b(?=\s*:)', r'"\1"', s)
    
#     # Fix unquoted string values (not already quoted, followed by comma, brace, bracket, or newline)
#     s = re.sub(r':\s*([^"{\[0-9\-tfn])([^,:}\]])*', r': "\1\2"', s)
    
#     # Fix long integers (trailing 'L')
#     s = re.sub(r'(\d+)L', r'\1', s)
    
#     # Fix short integers (trailing 's')
#     s = re.sub(r'(\d+)s', r'\1', s)
    
#     # Fix array prefixes ([I;, [B;, etc.)
#     s = re.sub(r'\[([IBSLF]);', r'"\1-array":', s)
    
#     return s



def main():
    # Example usage
    schem_file = "../schem/2x2door.schem"
    rson_file = "../schem/2x2door.json"

    # # Example input
    # input_str = '''{Schematic: {Version: 3, DataVersion: 4189, Metadata: {Date: 1741138531212L, WorldEdit: {Version: "7.3.10", EditingPlatform: "enginehub:fabric", Origin: [I; 589, 58, 258], Platforms: {"enginehub:fabric": {Name: "Fabric-Official", Version: "7.3.10+7004-768a436"}}}}, Width: 2s, Height: 7s, Length: 6s, Offset: [I; 3, -3, -3], Blocks: {Palette: {"minecraft:air": 0, "minecraft:sticky_piston[extended=false,facing=south]": 1, "minecraft:smooth_stone": 2, "minecraft:sticky_piston[extended=false,facing=north]": 3, "minecraft:quartz_block": 4, "minecraft:redstone_wire[east=none,north=side,power=0,south=side,west=none]": 5, "minecraft:lever[face=floor,facing=east,powered=false]": 6, "minecraft:redstone_wire[east=none,north=side,power=0,south=none,west=side]": 7}, Data: [B; 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 0B, 1B, 0B, 2B, 0B, 0B, 0B, 0B, 0B, 2B, 0B, 3B, 0B, 1B, 0B, 2B, 0B, 0B, 0B, 0B, 0B, 2B, 0B, 3B, 0B, 4B, 0B, 4B, 0B, 4B, 0B, 4B, 0B, 4B, 4B, 4B, 0B, 5B, 0B, 5B, 0B, 5B, 0B, 5B, 0B, 5B, 6B, 7B], BlockEntities: []}}}'''

    # # Convert and print JSON
    # parsed_json = fix_json_like_string(input_str)
    # schem = json.dumps(parsed_json, indent=2)
    # # print()

    # # Write to file
    # with open("schem_test.json", 'w') as f:
    #     f.write(schem)


    # nbtlib_schem_to_rson(schem_file)

    # Convert .schem to rson
    rson_data = schem_to_rson(schem_file)
    # write_rson_file(rson_data, rson_file)

    # # Convert rson to .schem
    # rson_data = read_rson_file(rson_file)
    # rson_to_schem(rson_data, "../schem/2x2door_new.schem")


if __name__ == "__main__":
    main()
