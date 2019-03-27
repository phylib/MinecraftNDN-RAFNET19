import argparse
import pandas as pd
import numpy as np
import math
from enum import Enum
from tqdm import tqdm

import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from heatmaphelper import heatmap
from boxplothelper import draw_multiple_boxplots
from plothelper import draw_burstiness

class Entity_Type(Enum):
    OBJECT_DYNAMIC = 1 # e.g. projectiles
    OBJECT_STATIC = 2 # e.g. armor stand
    EXP_ORB = 3
    GLOBAL_ENTITY = 4
    MOB = 5
    PAINTING = 6
    PLAYER = 7
    UNDEFINED = 8

# Possible Entity Types are: PROJECTILE, STATIC_OBJECT, EXP_ORB,
entity_types = {}

packets_per_entity = {}

class SpatialStatistics:

    def __init__(self, second):
        self.second = second
        self.entity_related = {}
        self.block_related = {}
        self.other = 0
        self.minChunkX = 10000
        self.minChunkZ = 10000
        self.maxChunkX = -10000
        self.maxChunkZ = -10000
        self.l = -1
        self.h = -1
        self.stats = None


    def add_packet(self, csv_row):

        if not isinstance(csv_row["Chunk"], str):
            self.other += 1
        else:
            chunk = csv_row["Chunk"]
            chunk_x = int(float(chunk.split(",")[0]))
            chunk_z = int(float(chunk.split(",")[1]))

            if chunk_x < self.minChunkX:
                self.minChunkX = chunk_x
            if chunk_x > self.maxChunkX:
                self.maxChunkX = chunk_x
            if chunk_z < self.minChunkZ:
                self.minChunkZ = chunk_z
            if chunk_z > self.maxChunkZ:
                self.maxChunkZ = chunk_z

            entity_id = csv_row["EntityId"]
            if math.isnan(entity_id):
                if chunk not in self.block_related:
                    self.block_related[chunk] = 0
                self.block_related[chunk] += 1
            else:
                if chunk not in self.entity_related:
                    self.entity_related[chunk] = 0
                self.entity_related[chunk] += 1

#            if csv_row["ChunkZ"] > 100:
#                print(csv_row["MessageType"])

    def calcuate_matrix(self, map):

        if self.l == - 1:
            self.l = self.maxChunkX - self.minChunkX
        if self.h == -1:
            self.h = self.maxChunkZ - self.minChunkZ
        matrix = np.zeros((self.l, self.h))
        for coords in map.keys():
            chunk_x = int(float(coords.split(",")[0]))
            chunk_z = int(float(coords.split(",")[1]))
            matrix[chunk_x - self.minChunkX - 1, chunk_z - self.minChunkZ - 1] = map[coords]
        return matrix


    def get_statistics(self):

        if self.stats == None:
            self.stats =  {"entityRelated": self.calcuate_matrix(self.entity_related),
                "blockRelated": self.calcuate_matrix(self.block_related),
                "other": self.other}

        return self.stats

spatialStatistics = SpatialStatistics(-1)
spatialStatisticsOverTime = {}
start_time = -1
TIME_INTERVAL = 50
DRAW_ANIMATION = False
DRAW_BURSTYNESS = False
FILETYPE = "pdf"

max_block_changes = 0
max_entity_changes = 0

def classify_packet(csv_entry):

    spatialStatistics.add_packet(csv_entry)

    tick_no = csv_entry["Tick"]
    if DRAW_ANIMATION:
        if tick_no not in spatialStatisticsOverTime:
            spatialStatisticsOverTime[tick_no] = SpatialStatistics(tick_no)
        spatialStatisticsOverTime[tick_no].add_packet(csv_entry)

    entity_id = csv_entry["EntityId"]
    if math.isnan(entity_id):
        # print((csv_entry["MessageType"], csv_entry["Chunk"]))
        return
    entity_id = int(entity_id)

    # count packets per entity_id
    if entity_id not in packets_per_entity:
        packets_per_entity[entity_id] = []
    packets_per_entity[entity_id].append(csv_entry.to_dict())

    # Classify Entity type by spawn message
    entity_types[entity_id] = csv_entry["EntityType"]


def getTickNo(csvEntry):
    global start_time
    if start_time == -1:
        start_time = int(csvEntry["Timestamp"] / 1000 / TIME_INTERVAL)
    return int(csvEntry["Timestamp"] / 1000 / TIME_INTERVAL) - start_time


def draw_heat_map(entity_related, block_related, x_min, x_max, z_min, z_max, title="heatmap." + FILETYPE):
    x_labels = np.arange(x_min, x_max, 1)
    str_x_labels = []
    for i in x_labels:
        if i % 2 == 1:
            str_x_labels.append(str(i))
        else:
            str_x_labels.append("")
    z_labels = np.arange(z_min, z_max, 1)
    str_z_labels = []
    for i in z_labels:
        if i % 2 == 1:
            str_z_labels.append(str(i))
        else:
            str_z_labels.append("")

    fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(15,6))

    im, _ = heatmap(entity_related, str_x_labels, str_z_labels, "Entity Packets", ax=ax1,
                       cmap="YlGn", cbarlabel="Packets per Chunk")

    im, _ = heatmap(block_related, str_x_labels, str_z_labels, "Block Packets", ax=ax2,
                       cmap="YlGn", cbarlabel="Packets per Chunk")
    #texts = annotate_heatmap(im, valfmt="{x:.1f} t")

    plt.tight_layout()
    plt.savefig(title)


def animate_heat_map(spatialStatistics, timedSpatialStatistics, title="heatmap.mp4"):
    x_labels = np.arange(spatialStatistics.minChunkX, spatialStatistics.maxChunkX, 1)
    z_labels = np.arange(spatialStatistics.minChunkZ, spatialStatistics.maxChunkZ, 1)
    matrixes = spatialStatistics.get_statistics()

    plt.close("all")
    fig, ((ax1, ax2)) = plt.subplots(ncols=2, figsize=(15,6))

    im_left, _ = heatmap(matrixes["entityRelated"], x_labels, z_labels, "Entity Related Packets", ax=ax1,
                       cmap="YlGn", cbarlabel="Packets per Chunk", max_value=max_entity_changes)

    im_right, _ = heatmap(matrixes["blockRelated"], x_labels, z_labels, "Block Related Packets", ax=ax2,
                       cmap="YlGn", cbarlabel="Packets per Chunk", max_value=max_block_changes)
    #texts = annotate_heatmap(im, valfmt="{x:.1f} t")

    plt.tight_layout()

    print("Max entity changes: {}, max block changes: {}".format(max_entity_changes, max_block_changes))

    print("Build animation")
    ims = []
    for i in timedSpatialStatistics:
        stats = timedSpatialStatistics[i]
        im1, cb1 = heatmap(stats["entityRelated"], x_labels, z_labels, "Entity Related Packets", ax=ax1,
                       cmap="YlGn", cbarlabel="Packets per Chunk", colorbar=False, max_value=max_entity_changes)
        im2, cb2 = heatmap(stats["blockRelated"], x_labels, z_labels, "Block Related Packets", ax=ax2,
                       cmap="YlGn", cbarlabel="Packets per Chunk", colorbar=False, max_value=max_block_changes)
        del stats["entityRelated"]
        del stats["blockRelated"]

        # Colorbar

        ims.append([im1, im2,])

    print("Assemble animation")
    ani = animation.ArtistAnimation(fig, ims, blit=False, interval=50)

    print("Save animation")
    plt.tight_layout()
    #plt.show()
    #plt.savefig(title)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=300)
    ani.save(title, writer=writer)


def execute(filename):
    df = pd.read_csv(filename, sep="\t")

    # Filter only clientbound packets
    df = df[df["Direction"] == "S->C"]
    #df = df.head(20000)

    # Adds a column "Tick" to the data frame
    df["Tick"] = df.apply(getTickNo, axis=1)

    # Creates the following items
    # - SpatialStatistics...Contains entity and block packets grouped by the spatial distribution
    # - SpatialStatisticsOverTime...(IFF ANIMATE=True) Spatial statistics with tick-no as additional dimension
    # - packets_per_entity...map with entity_id as key and list of packets for the entity as value
    # - entity_types...map with entity_id as key and entity_type as value
    df.apply(classify_packet, axis=1)

    # Map with entity_type as key and list with number of packets of the individual entities as value
    entities_per_type = {}
    # Map with entity_type as key and list with the number of ticks the individual entities are living as value
    ticks_per_type = {}
    packets_per_type = {}

    # Count ticks_per_entity_type and packets_per_entity_type
    for entity_id in entity_types:
        entity_type = entity_types[entity_id]

        if entity_type not in entities_per_type:
            entities_per_type[entity_type] = []
        entities_per_type[entity_type].append(len(packets_per_entity[entity_id]))

        if entity_id in packets_per_entity:
            if packets_per_entity[entity_id][0]["EntityId"] is not None:
                start = packets_per_entity[entity_id][0]["Tick"]
                end = packets_per_entity[entity_id][-1]["Tick"]
                ticks = end - start
                if entity_type not in ticks_per_type:
                    ticks_per_type[entity_type] = []
                ticks_per_type[entity_type].append(ticks)

    print("Draw boxplots")
    # print(entities_per_type)
    draw_multiple_boxplots(entities_per_type, title="Packets per entity type (complete game)", filename="bp_packets_types_fullgame." + FILETYPE, add_total_count=True)
    draw_multiple_boxplots(ticks_per_type, title="No. of active ticks per entity type (complete game)", filename="bp_ticks_types_fullgame." + FILETYPE, add_total_count=True)
    draw_multiple_boxplots(entities_per_type, title="Packets per entity type (complete game)", filename="bp_packets_types_fullgame_nofl." + FILETYPE, add_total_count=True, outliers=False)
    draw_multiple_boxplots(ticks_per_type, title="No. of active ticks per entity type (complete game)", filename="bp_ticks_types_fullgame_nofl." + FILETYPE, add_total_count=True, outliers=False)

    print("Draw Heatmap")

    matrixes = spatialStatistics.get_statistics()

    start_x = 8
    start_z = 12
    width = 21
    draw_heat_map(matrixes["entityRelated"][start_x:start_x+width:1, start_z:start_z+width:1], matrixes["blockRelated"][start_x:start_x+width:1, start_z:start_z+width:1],
                  spatialStatistics.minChunkX + start_x, spatialStatistics.minChunkX + start_x + width,
                  spatialStatistics.minChunkZ + start_z, spatialStatistics.minChunkZ + start_z + width, "OverallStatistic.png")
    #print(spatialStatisticsOverTime.keys())
    if DRAW_ANIMATION: ############# If this is set to true, the animatedSpatialStatistics, but also the burstiness_graphs for chunks are generated
        print("Animate Heatmap")
        for key in spatialStatisticsOverTime:
            spatialStatistic = spatialStatisticsOverTime[key]
            spatialStatistic.minChunkX = spatialStatistics.minChunkX
            spatialStatistic.minChunkZ = spatialStatistics.minChunkZ
            spatialStatistic.maxChunkX = spatialStatistics.maxChunkX
            spatialStatistic.maxChunkZ = spatialStatistics.maxChunkZ
            spatialStatistic.l = spatialStatistics.l
            spatialStatistic.h = spatialStatistics.h
            statistics = spatialStatisticsOverTime[key].get_statistics()
            del spatialStatisticsOverTime[key].entity_related
            del spatialStatisticsOverTime[key].block_related
            spatialStatisticsOverTime[key] = statistics
            global max_entity_changes, max_block_changes
            if np.max(spatialStatisticsOverTime[key]["blockRelated"]) > max_block_changes:
                max_block_changes = np.max(spatialStatisticsOverTime[key]["blockRelated"])
            if np.max(spatialStatisticsOverTime[key]["entityRelated"]) > max_entity_changes:
                max_entity_changes = np.max(spatialStatisticsOverTime[key]["entityRelated"])

        # animate_heat_map(spatialStatistics, spatialStatisticsOverTime)
        print("Draw burstiness of chunks")
        chunk_burstiness_entity = {} # Map ChunkIndex -> List with number of entity packets for each tick
        chunk_burstiness_block = {} # Map ChunkIndex -> List with number of block packets for each tick
        chunk_burstiness_other = []
        for i in range(0, df.iloc[-1]["Tick"] + 1):
            if i not in spatialStatisticsOverTime: # No packet for this tick exists
                for x in range(0, spatialStatistics.l):
                    for z in range(0, spatialStatistics.h):
                        chunk_index = str(x) + "," + str(z)
                        if chunk_index not in chunk_burstiness_block:
                            chunk_burstiness_block[chunk_index] = []
                        if chunk_index not in chunk_burstiness_entity:
                            chunk_burstiness_entity[chunk_index] = []
                        chunk_burstiness_block[chunk_index].append(0)
                        chunk_burstiness_entity[chunk_index].append(0)
                chunk_burstiness_other.append(-1)
            else: # At least one packet for that tick exists
                stats = spatialStatisticsOverTime[i]
                for x in range(0, spatialStatistics.l):
                    for z in range(0, spatialStatistics.h):
                        chunk_index = str(x) + "," + str(z)
                        if chunk_index not in chunk_burstiness_block:
                            chunk_burstiness_block[chunk_index] = []
                        if chunk_index not in chunk_burstiness_entity:
                            chunk_burstiness_entity[chunk_index] = []

                        #print((x,z), stats["blockRelated"][x,z], stats["entityRelated"][x,z])
                        chunk_burstiness_block[chunk_index].append(stats["blockRelated"][x,z])
                        chunk_burstiness_entity[chunk_index].append(stats["entityRelated"][x,z])
                chunk_burstiness_other.append(stats["other"])

        cmap = mp.colors.ListedColormap(['black', 'white', 'green', 'blue'])
        cmap_bounds = [0, 1, 2, 10, 1000]
        draw_burstiness(list(chunk_burstiness_entity.values()), autoincrease=False, title="Burstiness of entity packets grouped by chunk", filename="SpatialBurstinessEntities." + FILETYPE, yLabel="Chunk Index", cmap=cmap, cmap_bounds=cmap_bounds, colorbar=True)
        draw_burstiness(list(chunk_burstiness_block.values()), autoincrease=False, title="Burstiness of block packets grouped by chunk", filename="SpatialBurstinessBlocks." + FILETYPE, yLabel="Chunk Index", cmap=cmap, cmap_bounds=cmap_bounds, colorbar=True)
        draw_burstiness([chunk_burstiness_other], autoincrease=False, title="Burstiness of packets not related to chunks and entities", filename="OtherBurstiness." + FILETYPE, cmap=cmap, cmap_bounds=cmap_bounds, colorbar=True)
        calcBurstRateParams(list(chunk_burstiness_entity.values()), "ChunkBasedEntityPackets", noPacket=0, packet=1)
        calcBurstRateParams(list(chunk_burstiness_block.values()), "ChunkBasedBlockPackets", noPacket=0, packet=1)
        calcBurstRateParams([chunk_burstiness_other], "OtherPackets", noPacket=0, packet=1)



    # Draw Burstiness charts for entity types and boxplots for interval between packets
    if DRAW_BURSTYNESS:
        print("Draw burstiness of entity types")
        burstiness_per_entityType = {} # Map: Entity-Type -> Burstiness Vectors for each invdividual entity (Packet/No packet for each tick)
        intervals_per_entityType = {} # Map: Entity-Type -> List with all Interpacket intervals
        print("Calculate inter packet intervals for every entity")
        for entity_id in tqdm(entity_types):
            entity_type = entity_types[entity_id]

            if entity_id in packets_per_entity:
                # Check if packets are valid
                if packets_per_entity[entity_id][0]["EntityId"] is not None:
                    last_tick = 0
                    burstiness_vector = []
                    interval_vector = []
                    last_packet_index = 0
                    for tick_no in range(packets_per_entity[entity_id][0]["Tick"], packets_per_entity[entity_id][-1]["Tick"] + 1):

                        tick_found = -1
                        for packet_index in range(last_packet_index, len(packets_per_entity[entity_id])):
                            packet = packets_per_entity[entity_id][packet_index]
                            if packet["Tick"] == tick_no:
                                tick_found = 1
                                if last_tick != 0:
                                    interval_vector.append(tick_no - last_tick)
                                last_tick = tick_no
                                last_packet_index = packet_index
                                break

                        burstiness_vector.append(tick_found)
                    if entity_type not in burstiness_per_entityType:
                        burstiness_per_entityType[entity_type] = []
                    if entity_type not in intervals_per_entityType:
                        intervals_per_entityType[entity_type] = []

                    burstiness_per_entityType[entity_type].append(burstiness_vector)
                    intervals_per_entityType[entity_type] = intervals_per_entityType[entity_type] + interval_vector



        #for key in burstiness_per_entityType:
        #    calcBurstRateParams(burstiness_per_entityType[key], key)

        for key in burstiness_per_entityType:
            draw_burstiness(burstiness_per_entityType[key], title=key, filename=key+"_burstiness.png", yLabel="Individual entities")

        draw_multiple_boxplots(intervals_per_entityType, title="Inter-packet intervals per entity type", yLabel="Inter-packet interval [ticks]",
                               filename="bp_intervals_types_fullgame." + FILETYPE, add_total_count=False)
        draw_multiple_boxplots(intervals_per_entityType, title="Inter-packet intervals per entity type", yLabel="Inter-packet interval [ticks]",
                               filename="bp_intervals_types_fullgame_nofl." + FILETYPE, add_total_count=False, outliers=False)


def calcBurstRateParams(listOfBurstVectors, label, noPacket=-1, packet=1):
    T = 0
    F = 0
    T_F = 0
    F_T = 0
    for vector in listOfBurstVectors:
        for i in range(0, len(vector)):
            tick_found = vector[i]
            if tick_found == noPacket:
                F += 1
                if i > 0 and vector[i - 1] >= packet:
                    T_F += 1

            elif tick_found >= packet:
                T += 1
                if i > 0 and vector[i - 1] == noPacket:
                    F_T += 1
    print("{}: T={}, T->F={}, F={}, F->T={}, p=F->T/F={}, q=T->F/T={}".format(label, T, T_F, F, F_T, F_T / float(F),
                                                                              T_F / float(T)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-a", "--animation", default=False, type=bool)
    parser.add_argument("-b", "--burstiness", default=True, type=bool)
    parser.add_argument("-t", "--filetype", default="pdf", type=str)
    args = parser.parse_args()

    input = args.input
    DRAW_ANIMATION = args.animation
    DRAW_BURSTYNESS = args.burstiness
    FILETYPE = args.filetype

    execute(input)
