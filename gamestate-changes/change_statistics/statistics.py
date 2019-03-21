import csv
import sys
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from change_statistics.basicUtils import *


if len(sys.argv)<2:
    print("usage: python3 " + sys.argv[0] + "<pathToChangeLog.txt>")
    exit(-1)

print("target: " + sys.argv[1])

with open(sys.argv[1], 'r') as f:
    # skip header (three lines in this file)
    # 20-10-2018_19:34:40:724	time	type="block"	xpos	ypos	zpos	world	chunk	section	material	skylight	emittedLight	BlockData
    # 20-10-2018_19:34:40:724	time	type="entity"	xpos	ypos	zpos	world	chunk	section	uuid	[changed attributes]
    # 20-10-2018_19:34:40:724	time	type="status"	#loadedChunks	#changedChunks	#tileEntities	#changedTileEntities	#entities	#changedEntities	#onlinePlayers	totalStateDiffTime
    next(f)
    next(f)
    next(f)

    timepoints = []
    loaded_chunks = []
    changed_chunks = []
    tile_entities = []
    changed_tile_entities = []
    entities = []
    changed_entities = []
    online_players = []
    diff_times = [] # ms


    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        if getType(row[2]) == ChangeType.status:
            timepoints.append(to_date(row[0]))
            loaded_chunks.append(int(row[3]))
            changed_chunks.append(int(row[4]))
            tile_entities.append(int(row[5]))
            changed_tile_entities.append(int(row[6]))
            entities.append(int(row[7]))
            changed_entities.append(int(row[8]))
            online_players.append(int(row[9]))
            diff_times.append(float(row[10].replace("ms","")))

    fig, ax = plt.subplots()
    ax.plot(timepoints, loaded_chunks, label='#loaded chunks', linestyle="-", color='g')

    ax.plot(timepoints, tile_entities, label='#tile entities', color='orange')
    ax.plot(timepoints, entities, label='#entities', color='red')
    ax.plot(timepoints, changed_entities, label='#changed entities', linestyle='--', color='red')

    ax.plot(timepoints, diff_times, label='#time for statediff [ms]', color='black')

    ax2 = ax.twinx()
    ax2.plot(timepoints, online_players, label='#online players', color = 'b')
    ax2.plot(timepoints, changed_chunks, label='#changed chunks',  linestyle='--', color='g')
    ax2.plot(timepoints, changed_tile_entities, label='#changed tile entities', linestyle='--', color='orange')


    # fix legend
    #lines, labels = ax.get_legend_handles_labels()
    #lines2, labels2 = ax2.get_legend_handles_labels()
    #ax.legend(lines + lines2, labels + labels2, loc=2)
    ax.legend(loc=2) # upper left
    ax2.legend(loc=1) # upper right

    ax.set(xlabel='Time', title='Status information')
    ax.grid()
    datacursor()
    plt.show()