import argparse
import pandas as pd
import numpy as np
import math
from enum import Enum

class Entity_Type(Enum):
    OBJECT_DYNAMIC = 1 # e.g. projectiles
    OBJECT_STATIC = 2 # e.g. armor stand
    EXP_ORB = 3
    GLOBAL_ENTITY = 4
    MOB = 5
    PAINTING = 6
    PLAYER = 7
    UNDEFINED = 8

last_entity_positions = {}

def merge_chunk_indizes(packet):
    if not math.isnan(packet["ChunkX"]) and not math.isnan(packet["ChunkZ"]):
        return str(packet["ChunkX"]) + "," + str(packet["ChunkZ"])
    return np.nan

def calc_entity_chunks(packet):
    entity_id = packet["EntityId"]
    if not math.isnan(entity_id):
        if isinstance(packet["Chunk"], str):
            last_entity_positions[entity_id] = packet["Chunk"]
            return packet["Chunk"]
        else:
            if entity_id in last_entity_positions:
                chunk = last_entity_positions[entity_id]
                return chunk
            else:
                return packet["Chunk"]
    else:
        return packet["Chunk"]


def recover_chunk_x(packet):
    if isinstance(packet["Chunk"], str):
        return float(packet["Chunk"].split(",")[0])
    return np.nan


def recover_chunk_z(packet):
    if isinstance(packet["Chunk"], str):
        return float(packet["Chunk"].split(",")[1])
    return np.nan

entity_type = {}

def interpolate_entity_type(packet):
    entity_id = packet["EntityId"]
    if not math.isnan(entity_id):
        if entity_id in entity_type:
            return entity_type[entity_id]
        elif isinstance(packet["EntityType"], str):
            entity_type[entity_id] = packet["EntityType"]
            return packet["EntityType"]
        else:
            message_type = packet["MessageType"]
            if message_type == "SpawnPlayer":
                entity_type[entity_id] = Entity_Type.PLAYER
            elif message_type == "SpawnObject":
                entity_type[entity_id] = Entity_Type.OBJECT_DYNAMIC
            elif message_type == "SpawnExperienceOrb":
                entity_type[entity_id] = Entity_Type.EXP_ORB
            elif message_type == "SpawnGlobalEntity":
                entity_type[entity_id] = Entity_Type.GLOBAL_ENTITY
            elif message_type == "SpawnMob":
                entity_type[entity_id] = Entity_Type.MOB
            elif message_type == "SpawnPainting":
                entity_type[entity_id] = Entity_Type.PAINTING
            elif message_type == "JoinGame":
                entity_type[entity_id] = Entity_Type.PLAYER
            else:
                entity_type[entity_id] = Entity_Type.UNDEFINED
            return entity_type[entity_id];

    return np.nan

def execute(input_file):

    print("Process " + input_file)

    # 1 Parse CSV
    packets = pd.read_csv(input_file, sep="\t")

    if (len(packets) == 0):
        print("No Data")
        return

    # Add a column with chunk index format "x,z"
    packets["Chunk"] = packets.apply(merge_chunk_indizes, axis=1)

    # 2 For all entity IDs, interpolate all missing chunk indizes
    packets["Chunk"] = packets.apply(calc_entity_chunks, axis=1)
    packets["ChunkX"] = packets.apply(recover_chunk_x, axis=1)
    packets["ChunkZ"] = packets.apply(recover_chunk_z, axis=1)
    print("Chunk indizes interpolated")

    # Interpolate EntityTypes
    packets["EntityType"] = packets.apply(interpolate_entity_type, axis=1)
    print("Entity types interpolated")

    newName = "." + ("".join(input_file.split(".")[:-1]) + "_interpolated.csv")
    packets.to_csv(newName, sep="\t")

    # 3 Count messages per chunk




# Execute: python3 MCPacketStatistics -i /home/phmoll/Documents/Minecraft/network-traces/parsedPackets/143.205.122.57-38132_parsedPackets.log
# Batch Execution: ls | grep parsedPackets.log | xargs -I {} python3 ~/PythonScripts/minecraft/MCChunkInterpolation.py -i "./{}"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    args = parser.parse_args()

    input = args.input

    execute(input)