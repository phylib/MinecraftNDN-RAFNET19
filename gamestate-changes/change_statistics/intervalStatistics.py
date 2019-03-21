import csv
import sys
from change_statistics.basicUtils import *
from change_statistics.intervalDataSinks.plotStatusInformation import StatusInformationPlot
from change_statistics.intervalDataSinks.printIntervals import IntervalPrinter
from change_statistics.intervalDataSinks.plotChangesPerType import ChangesPerTypePlot
from change_statistics.intervalDataSinks.plotEntityAddRemove import EntityAddRemovePlot
from change_statistics.intervalDataSinks.printIntervalStats import IntervalStatPrinter
from change_statistics.intervalDataSinks.plotChangeTypeTotals import ChangeTypeTotalsPlot
from change_statistics.intervalDataSinks.statisticChangesPerType import StatisticChangesPerType
from change_statistics.intervalDataSinks.plotIntervalTimeDifference import InterIntervalTimeChanges
from change_statistics.intervalDataSinks.plotPlayerPositionsAndChunkChanges import PlotPlayerPositionAndChunkChanges
from change_statistics.intervalDataSinks.plotChunkChanges import PlotChunkChanges
INTERVAL_LENGTH_SECONDS = 0.5  # determined by LoggerPlugin game state diff interval being roughly 500ms
TICKS_PER_SECOND = 20 # minecraft-server -> around 20 ticks per second
if len(sys.argv)<2:
    print('usage: python3 ' + sys.argv[0] + ' <pathToChangeLog.txt>')
    exit(-1)

print('target: ' + sys.argv[1])

with open(sys.argv[1], 'r') as f:
    # skip header (three lines in this file)
    # 20-10-2018_19:34:40:724	time	type="block"	xpos	ypos	zpos	world	chunk	section	material	skylight	emittedLight	BlockData
    # 20-10-2018_19:34:40:724	time	type="entity"	xpos	ypos	zpos	world	chunk	section	uuid	[changed attributes]
    # 20-10-2018_19:34:40:724	time	type="status"	#loadedChunks	#changedChunks	#tileEntities	#changedTileEntities	#entities	#changedEntities	#onlinePlayers	totalStateDiffTime
    headerlen = 3
    for i in range(0,headerlen): # skip over the above mentioned three header lines
        next(f)

    status_line_count = 0 # running counter as to measure interval length (splitting up lines)
    # number of status messages (processed state diffs) / number of combined intervals
    interval_size = 2 # 1 * 0.5s -> half second intervals, 2 * 0.5s -> one second intervals (lines of two intervals "merged"/processed as one unit)
    world_filter=[]

    # consecutive intervals (packages of lines/change-entries) are pushed to these sinks
    #data_sinks = [IntervalStatPrinter(INTERVAL_LENGTH_SECONDS * interval_size), ChangeTypeTotalsPlot(), ChangesPerTypePlot(), EntityAddRemovePlot(),
    #              StatusInformationPlot()]
    #data_sinks = [InterIntervalTimeChanges(TICKS_PER_SECOND), ChangeTypeTotalsPlot(TICKS_PER_SECOND), StatisticChangesPerType(TICKS_PER_SECOND)]
    #data_sinks = [PlotChunkChanges(), InterIntervalTimeChanges(TICKS_PER_SECOND), IntervalStatPrinter(INTERVAL_LENGTH_SECONDS * interval_size), ChangeTypeTotalsPlot(TICKS_PER_SECOND), StatusInformationPlot()]
    data_sinks = [InterIntervalTimeChanges(TICKS_PER_SECOND), IntervalStatPrinter(INTERVAL_LENGTH_SECONDS * interval_size), ChangeTypeTotalsPlot(TICKS_PER_SECOND), StatusInformationPlot()]

    intervalQueue = {}
    intervalKeys = []

    reader = csv.reader(f, delimiter="\t") # sequentially read all lines in the CSV file
    for row in reader:
        type = getType(row[2])
        worldTimeTick = int(row[1])
        world = row[6]
        if len(world_filter) > 0 and not world in world_filter:
            continue

        if worldTimeTick not in intervalQueue:
            intervalQueue[worldTimeTick] = IntervalData() # create new instance of instance data class
            intervalKeys.append(worldTimeTick)

        interval = intervalQueue[worldTimeTick]
        interval.addLogRowItems(row)
    f.close()

    intervalKeys = sorted(intervalKeys)
    i = 0
    while i < len(intervalKeys):
        iv = IntervalData()
        for j in range(0, interval_size):
            if i+j >= len(intervalKeys): break
            key = intervalKeys[i+j]
            iv.append(intervalQueue[key])
            del(intervalQueue[key])

        # push new interval to all sinks (wait for sinks to process interval data)
        for sink in data_sinks:
            sink.receiveIntervalData(iv)
        i += interval_size

    # no more lines, notify sinks
    for sink in data_sinks:
        sink.noMoreIntervals()
