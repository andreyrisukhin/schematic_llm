# import json

# def validate_no_duplicate_coordinates(json_data):
#     coordinates = set()
#     for block in json_data.get('blocks', []):
#         print(f"{block=}, {type(block)=}")
#         coord = (block['x'], block['y'], block['z'])
#         if coord in coordinates:
#             return False
#         coordinates.add(coord)
#     return True

# # Example usage
# if __name__ == "__main__":
#     filepath = '../prompts/chatgpt_response_2x2.json'
#     with open(filepath, 'r') as file:
#         data = json.load(file)
#         if validate_no_duplicate_coordinates(data):
#             print("No duplicate coordinates found.")
#         else:
#             print("Duplicate coordinates found.")


import json
from collections import defaultdict

def check_for_duplicate_coordinates(rson_data):
    # Initialize a dictionary to track blocks by their coordinates
    coordinates_dict = defaultdict(list)
    
    # Iterate through the blocks in the schematic
    for group in rson_data['blocks']:
        for block in rson_data['blocks'][group]:
            # Get the coordinates of each block
            position = tuple(block['position'])
            
            # Add the block to the list of blocks at this coordinate
            coordinates_dict[position].append(block)
    
    # Find coordinates with multiple blocks
    conflicts = {coords: blocks for coords, blocks in coordinates_dict.items() if len(blocks) > 1}
    
    # Return conflicts if there are any, otherwise return empty dictionary
    return conflicts

# Run the function on the example data
filepath = '../prompts/chatgpt_response_2x2.json'
filepath_conflict = '../prompts/dupes_chatgpt.json'

with open(filepath_conflict, 'r') as file:
    rson_data = json.load(file)
conflicts = check_for_duplicate_coordinates(rson_data)

# Print conflicts if any
if conflicts:
    print("Found conflicts at the following coordinates:")
    for coords, blocks in conflicts.items():
        print(f"Coordinate: {coords}")
        for block in blocks:
            print(f"  Block: {block}")
else:
    print("No conflicts found!")