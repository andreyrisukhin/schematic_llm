# schematic_llm

## Done
* RSON (RedStone Object Notation) of a 2x2 door is input to ChatGPT with a matching prompt, and ChatGPT returns well-formed RSON of a 2x3 door.
* Automatically evaluate RSON (block positions collide)

## TODO
* P0: Parse litematica --> RSON (create training data)
* P0: Parse RSON --> litematica (give user a schematic to test)
* P1: Load and evaluate the minecraft schematic (check door volume, toggle lever, check door volume) (return stone positions in debug information)

## Maybe 
* RSON piston placement validator? More work to calculate, firing seq important, maybe cheaper to just test in game simulator.