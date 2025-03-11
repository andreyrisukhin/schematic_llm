"""
Read in a text file (output from the llm), and parse it into a dict of block and coordinate triples.
Then assemble the blocks into a schematic.
"""

from typing import Dict, List, Tuple

import litemapy as lm
# import minecraftschematics as ms
import mcschematic
import json

def file_to_text(filename):
    with open(filename, 'r') as f:
        text = f.read()
    return text

def verify_syntax(text) -> str:
    """
    Count matching parentheses and brackets and braces.
    If the counts are equal or can be fixed by removing the last one, return text that works.
    Else raise an error.
    """

    stack = []
    unmatched_closing_braces = 0
    
    for i, char in enumerate(text):
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack:
                # # If the last character is unmatched, remove it and return the text
                # if i == len(text) - 1:
                #     return text[:-1]
                
                # Track unmatched braces instead of raising an error immediately
                if char == '}':
                    unmatched_closing_braces += 1
                else:
                    raise ValueError(f"Unmatched closing {char} at position {i}")
                

                # # If there are unmatched closing brackets at the end, remove them
                # while char in ')]}' and i == len(text) - 1:
                #     text = text[:-1]
                #     i -= 1
                #     char = text[-1] if text else ''
                # if not text or char in ')]}':
                #     raise ValueError(f"Unmatched closing {char} at position {i}")
                # else:
                #     raise ValueError(f"Unmatched closing {char} at position {i}")
            else:
                top = stack.pop()
                if (top == '(' and char != ')') or \
                (top == '[' and char != ']') or \
                (top == '{' and char != '}'):
                    raise ValueError(f"Mismatched {top} and {char} at position {i}")
    
    if unmatched_closing_braces > 0:
        text = text[:-unmatched_closing_braces]
    
    if stack:
        raise ValueError(f"Unmatched opening {stack[-1]} at position {len(text)}")
    return text


def text_to_blocks(text) -> Dict[str, List[Tuple[int, int, int]]]:
    """
    Given text with matched {[()]}, with form {key: [[x1, y1, z1], [x2, y2, z2], ...]},
    return a dict of block names and coordinates.
    """
    blocks = {}

    text = text[1:-1] # Remove the outer { }

    parts = text.split("]],") # Split by "]],"
    for part in parts:
        part += "]]" # Add the missing ]]
        part = part.replace(' ', '')
        key, value = part.split(":")
        value = value[1:-1] # Remove the outer [ ]
        tuples = value.split("],") # Split values into the [x,y,z] tuples
        tuples = [t.replace('[', '').replace(']', '') for t in tuples]

        coords = []
        for t in tuples:
            x, y, z = t.split(',')
            coords.append((int(x), int(y), int(z)))
            
        blocks[key] = coords
    return blocks

def get_dims(blocks) -> Tuple[int, int, int]:
    """Given a dict of blocks and their coordinates, return the height."""
    width = 0
    length = 0
    height = 0
    for coords in blocks.values():
        for x, y, z in coords:
            height = max(height, y)
            width = max(width, x)
            length = max(length, z)
    return width, height, length

def quick_check():
    json_str = """
    {"width": 5, "height": 4, "length": 7, "block_positions": {"hopper[facing=down,enabled=true]": [[2, 0, 3]], "iron_door[hinge=right,half=lower,powered=false,facing=east,open=false]": [[2, 0, 2], [2, 1, 2]], "note_block": [[2, 1, 1]], "redstone_wire[east=none,south=none,north=none,west=none,power=0]": [[3, 2, 2]], "stone_bricks": [[0, 2, 3], [1, 1, 3], [3, 1, 2], [3, 1, 3], [4, 2, 3]], "stone_slab[type=bottom]": [[2, 2, 1], [2, 2, 2], [2, 1, 4], [2, 0, 5]], "tripwire[disarmed=false,east=false,powered=false,south=false,north=false,west=false,attached=false]": [[2, 2, 3]], "tripwire_hook[powered=false,attached=false,facing=south]": [[1, 2, 3], [3, 2, 3]], "water[level=0]": [[2, 1, 3]]}}
    """
    json_str_richer = """
    {'width': 5, 'height': 4, 'length': 7, 'block_positions': {'chest[facing=south,type=single]': [(2, 0, 4)], 'hopper[facing=south,enabled=true]': [(2, 0, 3)], 'iron_door[hinge=right,half=lower,powered=false,facing=north,open=false]': [(2, 0, 2)], 'iron_door[hinge=right,half=upper,powered=false,facing=east,open=false]': [(2, 1, 2)], 'note_block': [(2, 1, 1)], 'redstone_wire[east=none,south=none,north=none,west=none,power=0]': [(3, 2, 2)], 'stone_brick_slab[type=bottom]': [(2, 2, 1), (2, 2, 2), (2, 1, 4), (2, 0, 5)], 'stone_bricks': [(0, 2, 3), (1, 1, 3), (3, 1, 2), (3, 1, 3), (4, 2, 3)], 'tripwire[disarmed=false,east=false,powered=false,south=false,north=false,west=false,attached=true]': [(2, 2, 3)], 'tripwire_hook[powered=false,attached=true,facing=east]': [(1, 2, 3)], 'tripwire_hook[powered=false,attached=true,facing=west]': [(3, 2, 3)], 'water[level=0]': [(2, 1, 3)]}}
    """
    # replace ' with "
    json_str = json_str_richer.replace("'", '"')
    print(f'json_str: {json_str}')

    data = json.loads(json_str)
    print(data)
    # Read as json, construct schematic 
    blocks = data['block_positions']
    schem = mcschematic.MCSchematic()
    for key, coords in blocks.items():
        for x, y, z in coords:
            schem.setBlock((x, y, z), "minecraft:" + key)
    # return schem
    schem.save(f"../llm_output_processed", "quick_check", mcschematic.Version.JE_1_18_2)

def blocks_to_schem(blocks):
    # """Given a dict of str blocks and their coordinates, return a schematic."""
    # width, height, length = get_dims(blocks)
    # reg = lm.Region(0,0,0, width, height, length)
    # schem = lm.Schematic(reg)
    # for key, coords in blocks.items():
    #     for x, y, z in coords:
    #         schem.register_block(x, y, z, key)

    
    # schem = lm.Schematic()
    # for key, coords in blocks.items():
    #     for x, y, z in coords:
    #         schem.reg

    schem = mcschematic.MCSchematic()
    for key, coords in blocks.items():
        for x, y, z in coords:
            schem.setBlock((x, y, z), "minecraft:" + key)
    return schem
    

if __name__ == '__main__':
    # quick_check()

    # import sys
    # if len(sys.argv) != 2:
    #     print("Usage: python output2schem.py <filename>")
    #     sys.exit(1)
    # filename = sys.argv[1]

    # Bad Syntax
    # filename = '../llm_output/Title_ 3x3 piston door Width_ 7 Height_ 9 Length_ 3'
    
    # Good Syntax
    # filename = '../llm_output/Title_ Compact Angle Cannon Width_ 6 Height_ 4 Length_ 6'
    filename = '../llm_output/Title_ FarmFish Width_ 5 Height_ 4 Length_ 7'

    text = file_to_text(filename)
    text = verify_syntax(text)
    blocks = text_to_blocks(text)
    # print(blocks)

    schem = blocks_to_schem(blocks)

    # Save the name, between Title_ and Width_
    name = filename.split('Title_')[1].split('Width_')[0].strip()
    schem.save(f"../llm_output_processed", name, mcschematic.Version.JE_1_18_2)
    print(f"Saved {filename}")

    