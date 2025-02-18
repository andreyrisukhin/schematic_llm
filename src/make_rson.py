"""
Create a file in Redstone Object Notation (RSON) format. Save the dict to a json file.
A format designed for llms to prompt nicely.
Many redstone door circuits are packed tightly (dense), so using an adjacency matrix instead of a list is both appropriate and likely easier for the llm to understand.
"""

import json
import os

def save_rson(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def create_rson():
    # Example data
    schematic_name = "2x2 door, origin at door base (0,0,0)" # Door is the volume that moves.
    schematic_behavior = "There are four sticky pistons, two on each side, that push the blocks to create a 2x2 door. There is a lever to activate the pistons. When activated, the 2x2 space is filled with blocks, and when deactivated, the space is empty. There is redstone dust to connect the lever to the pistons.",
    door_blocks = [
        {"position": (0, 0, 0), "block": "minecraft:stone"},
        {"position": (1, 0, 0), "block": "minecraft:stone"},
        {"position": (0, 1, 0), "block": "minecraft:stone"},
        {"position": (1, 1, 0), "block": "minecraft:stone"}
    ]
    pistons = [
        {"position": (-1, 0, 0), "block": "minecraft:sticky_piston", "facing": "+x"},
        {"position": (2, 0, 0), "block": "minecraft:sticky_piston", "facing": "-x"},
        {"position": (-1, 1, 0), "block": "minecraft:sticky_piston", "facing": "+x"},
        {"position": (2, 1, 0), "block": "minecraft:sticky_piston", "facing": "-x"}
    ]
    redstone = [
        {"position": (-1, 2, 0), "block": "minecraft:quartz_block"}, # Potentially need to add redstone orientation... maybe not? Can simulate and block update to update all connections without encoding in llm? That is how I play the game, just place dust and it rotates. 
        {"position": (-1, 2, 0), "block": "minecraft:redstone_dust"},
        {"position": (0, 2, 0), "block": "minecraft:quartz_block"},
        {"position": (0, 2, 0), "block": "minecraft:redstone_dust"},
        {"position": (1, 2, 0), "block": "minecraft:quartz_block"},
        {"position": (1, 2, 0), "block": "minecraft:redstone_dust"},
        {"position": (2, 2, 0), "block": "minecraft:quartz_block"},
        {"position": (2, 2, 0), "block": "minecraft:redstone_dust"}
    ]
    lever = [
        {"position": (2, 2, 1), "block": "minecraft:lever", "attached_to": "quartz_block", "facing": "-z"}
    ]
        
    rson_data = {
        "schematic_name": schematic_name,
        "schematic_behavior": schematic_behavior,
        "blocks": {
            "door": door_blocks,
            "pistons": pistons,
            "redstone": redstone,
            "lever": lever
        }
    }

    # This is an adjacency list that assumes all else is air. While generating, 
    # the llm may make duplicate coordinates which is a problem. 
    # Test whether the benefit of planning (starting with volume to move, then 
    # place pistons, then redstone, then lever) outweighs the cost of the llm 
    # making duplicates. If it does, then we can add a check to remove duplicates.

    return rson_data

if __name__ == "__main__":   
    rson_data = create_rson()
    file_path = os.path.join(os.getcwd(), '../rson/rson_output.json')
    save_rson(rson_data, file_path)
