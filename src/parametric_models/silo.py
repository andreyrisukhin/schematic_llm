"""
Given a user parameter k, representing desired capacity, generate a schematic for a silo with k capacity.

Once coded, next steps include:
* Tiling Silos (space constraints)
"""

import mcschematic as ms

def _add_base_layer(silo:ms.MCSchematic):
    # base_layer = ms.MCSchematic()
    silo.setBlock((0,0,0), "minecraft:stone")
    silo.setBlock((1,0,0), "minecraft:barrel")
    silo.setBlock((0,0,-1), "minecraft:quartz_block")
    silo.setBlock((1,0,-1), "minecraft:hopper[enabled=true,facing=south]")
    silo.setBlock((0,0,-2), "minecraft:hopper[enabled=true,facing=east]")
    silo.setBlock((1,0,-2), "minecraft:hopper[enabled=true,facing=south]")

    # base_layer.save(".", "silo_base", ms.Version.JE_1_18_2)
    return silo

def _add_layer_A(silo:ms.MCSchematic, i:int):
    # layer_A = ms.MCSchematic()
    silo.setBlock((0,i,0), "minecraft:stone")
    silo.setBlock((1,i,0), "minecraft:redstone_lamp[lit=false]")
    silo.setBlock((0,i,-1), "minecraft:comparator[facing=north,mode=compare,powered=false]")

    silo.setBlock((0,i,-2), "minecraft:chest[facing=west,type=right,waterlogged=false]")
    silo.setBlock((1,i,-2), "minecraft:quartz_block")
    silo.setBlock((0,i,-3), "minecraft:chest[facing=west,type=left,waterlogged=false]")
    silo.setBlock((1,i,-3), "minecraft:hopper[enabled=true,facing=west]")
    
    # layer_A.save(".", "silo_layer_A", ms.Version.JE_1_18_2)
    return silo

def _add_layer_B(silo:ms.MCSchematic, i:int):
    # layer_B = ms.MCSchematic()
    silo.setBlock((0,i,0), "minecraft:stone")
    silo.setBlock((1,i,0), "minecraft:redstone_lamp[lit=false]")
    silo.setBlock((0,i,-1), "minecraft:quartz_block")
    silo.setBlock((1,i,-1), "minecraft:quartz_block")
    silo.setBlock((0,i,-2), "minecraft:hopper[enabled=true,facing=north]")
    silo.setBlock((1,i,-2), "minecraft:comparator[facing=north,mode=compare,powered=false]")
    silo.setBlock((0,i,-3), "minecraft:chest[facing=north,type=left,waterlogged=false]")
    silo.setBlock((1,i,-3), "minecraft:chest[facing=north,type=right,waterlogged=false]")
    
    # layer_B.save(".", "silo_layer_B", ms.Version.JE_1_18_2)
    return silo

def _reflect_x_schematic(schem:ms.MCSchematic, WIDTH:int, HEIGHT:int, LENGTH:int):
    """
    Reflects a schematic about the x-axis.

    Wait, no need to reflect!
    """
    # Reflect about x-axis
    for x in range(WIDTH):
        for y in range(HEIGHT):
            for z in range(LENGTH):
                block = schem.getBlockDataAt((x, y, z))
                schem.setBlock((WIDTH - x - 1, y, z), block)
    return schem

def generate_silo(k):
    """
    Parameters:
    k: int
        Desired capacity of the silo, inventory item slots.
    """
    assert k > 0, "Capacity must be greater than 0."

    CAPACITY_BASE = 27 + (3*5)
    CAPACITY_LAYER = (27*2) + 5

    layer_count = (k - CAPACITY_BASE) // CAPACITY_LAYER

    WIDTH = 2
    HEIGHT = layer_count + 1
    LENGTH = 4

    silo = ms.MCSchematic()
    silo = _add_base_layer(silo)

    # Alternate A B layers until height is reached
    for l in range(layer_count):
        if l % 2 == 0:
            silo = _add_layer_A(silo, l+1)
        else:
            silo = _add_layer_B(silo, l+1)

    silo.save(".", f"silo_{k}", ms.Version.JE_1_18_2)

    # Reflect about x-axis
    silo = _reflect_x_schematic(silo, WIDTH, HEIGHT, LENGTH)
    silo.save(".", f"silo_{k}_reflected", ms.Version.JE_1_18_2)
    

if __name__ == "__main__":
    generate_silo(1000)