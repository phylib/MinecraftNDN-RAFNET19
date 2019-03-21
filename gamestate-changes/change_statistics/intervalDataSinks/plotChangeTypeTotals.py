import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from mpldatacursor import datacursor
from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType


class ChangeTypeTotalsPlot(IntervalDataSink.IntervalDataSink):

    def __init__(self, ticksPerSecond):
        super(ChangeTypeTotalsPlot, self).__init__()
        self.intervals = OrderedDict()
        self.intervalsBlockDetails = OrderedDict()
        self.intervalSums = OrderedDict()
        self.blockDetailIntervalSums = OrderedDict()
        self.materialChanges = {}
        self.intervalStartTick = 0
        self.ticksPerSecond = ticksPerSecond    #  e.g. 20 ticks per second
        self.numberOfNonStatusEntries = 0

    # sum up all changes in an interval (no deduplication, one block changing two times is counted as if two blocks changed one time each)
    def receiveIntervalData(self, intervalData):
        worldFullTime = intervalData.entries[0]["worldFullTime"]
        self.intervalStartTick = worldFullTime
        self.intervals[self.intervalStartTick] = {ChangeType.entity: {}, ChangeType.tile_entity: {},
                                                  ChangeType.block: {}}
        self.intervalsBlockDetails[self.intervalStartTick] = {}

        for entry in intervalData.entries:
            type = entry["type"]
            if type not in [ChangeType.entity, ChangeType.tile_entity, ChangeType.block, ChangeType.status]:
                raise ValueError("type " + str(type) + " not handled")

            if type == ChangeType.status:
                continue
            # else (change to block, block_entity or entity)
            self.numberOfNonStatusEntries += 1

            key = entry["typeStr"]
            if type == ChangeType.block:
                # keep track of individual block changes for a more detailed view
                for item in ['material', 'skylight', 'emittedLight', 'blockData']:
                    if entry[item]:
                        if item not in self.intervalsBlockDetails[self.intervalStartTick]:
                            self.intervalsBlockDetails[self.intervalStartTick][item] = 1
                        else:
                            self.intervalsBlockDetails[self.intervalStartTick][item] += 1

                        # more detailed information about material changes
                        if item == 'material':
                            material = entry[item]
                            if material not in self.materialChanges:
                                self.materialChanges[material] = 1
                            else:
                                self.materialChanges[material] += 1

            # increment the change count per type
            if key not in self.intervals[self.intervalStartTick][type]:
                self.intervals[self.intervalStartTick][type][key] = 1
            else:
                self.intervals[self.intervalStartTick][type][key] += 1


    def noMoreIntervals(self):
        self.sumUpIntervals() # preprocessing for plotTotals and simple sanity check
        self.sumUpBlockDetailIntervals()
        # plot total changes
        self.plotTotals(self.intervalSums[ChangeType.entity], "Changes per EntityType")
        self.plotTotals(self.intervalSums[ChangeType.tile_entity], "Changes per BlockEntityType")
        self.plotTotals(self.blockDetailIntervalSums, "Types of Changes concerning Blocks")

        # plot more detailed information about changes of block material
        self.plotTotals(self.materialChanges, "Changes to Block Materials")

        # plot changes per type over time
        self.plotChangesPerTypeOverTime()

        # plot fine grained changes (every subtype) over time
        changes = 0
        changes += self.plotChangesOverTime(self.intervals, ChangeType.block, "plain block changes, only for sanity check")
        self.plotChangesOverTime(self.intervalsBlockDetails, "", "Changes per BlockType") # just display these, as multiple things can change in one block change (messes up the sum)
        changes += self.plotChangesOverTime(self.intervals, ChangeType.tile_entity, "Changes per BlockEntity/TileEntity")
        changes += self.plotChangesOverTime(self.intervals, ChangeType.entity, "Changes per Entity")

        # check if everything "sums up"
        if changes != self.numberOfNonStatusEntries:
            raise ValueError("Sum of changes (" + str(changes) + ") does not match the number of non-status change entries (" + str(
                self.numberOfNonStatusEntries) + ")")


    def sumUpIntervals(self):
        self.intervalSums = {ChangeType.entity: {}, ChangeType.tile_entity: {},
                                                          ChangeType.block: {}}

        for interval, intervalDict in self.intervals.items():
            for type, item in intervalDict.items():
                for key, count in item.items():
                    if key not in self.intervalSums[type]:
                        self.intervalSums[type][key] = count
                    else:
                        self.intervalSums[type][key] += count

        # sum up all changes in order to sanity-check sums
        changeSum = 0
        for type in self.intervalSums.keys():
            for key, count in self.intervalSums[type].items():
                changeSum += count
        print("Number of non-status entries: " + str(self.numberOfNonStatusEntries))
        print("Total sum of changes: " + str(changeSum))
        if changeSum != self.numberOfNonStatusEntries:
            raise ValueError("Sum of changes (" + str(changeSum) +") does not match the number of non-status change entries (" + str(self.numberOfNonStatusEntries) + ")")


    def sumUpBlockDetailIntervals(self):
        for interval, intervalDict in self.intervalsBlockDetails.items():
            for key, count in intervalDict.items():
                if key not in self.blockDetailIntervalSums:
                    self.blockDetailIntervalSums[key] = count
                else:
                    self.blockDetailIntervalSums[key] += count


    def plotTotals(self, dict, title):
        labels = sorted(dict.keys())
        values = [dict[i] for i in labels]

        print(title)
        for i in range(0,len(labels)):
            print("\t" + labels[i] + "\t" + str(values[i]))
        print("\n")

        fig, ax1, = plt.subplots()
        ax1.pie(values, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)

        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title(title + " (" + str(sum(values)) + " indiv. changes in total)")

        separateLegend(ax1)
        datacursor()
        plt.show()


    # sum of respective change-type over time
    def plotChangesPerTypeOverTime(self):
        x = []
        changes = {ChangeType.entity: [], ChangeType.tile_entity: [], ChangeType.block: []}
        # just go through all intervals
        for interval, intervalDict in self.intervals.items():
            x.append(interval/self.ticksPerSecond)

            for type, item in intervalDict.items():
                sum = 0                         # create list x as all interval start ticks
                for key, count in item.items():
                    sum += count
                changes[type].append(sum)  # create list y as sum of changes for specific type

        # draw a plain "plot" of block, blockEntity, entity changes (y) per interval (x)
        fig, ax1 = plt.subplots()
        for type in [ChangeType.block, ChangeType.tile_entity, ChangeType.entity]:
            ax1.plot(x, changes[type], label=str(type))

        ax1.set_xlabel("Seconds")
        ax1.set_ylabel("Changes")

        separateLegend(ax1)
        ax1.set_title("Changes per type over time")
        datacursor()
        plt.show()


    # most fine grained information, (individual elements of a specific type) over time
    def plotChangesOverTime(self, intervalDictionary, dictionaryKey, title):
        totalChanges = 0
        keys = set()
        # run over all intervals to get all types of e.g. entities that may happen
        if dictionaryKey:
            for interval, intervalDict in intervalDictionary.items():
                for key in intervalDict[dictionaryKey]:
                    keys.add(key)
        else:
            for interval, intervalDict in intervalDictionary.items():
                for key in intervalDict.keys():
                    keys.add(key)

        y = {}
        x = list(self.intervals.keys()) # create x as list of all intervalStartTicks
        listlen = len(x)
        # create lists for every type-key (all #intervals long and initialized with zero)
        for key in keys:
            y[key] = [0] * listlen  # lists are initialized with zeros, len(list) = len(intervals)

        # update lists with actual counts of the individual intervals
        # run over all intervals, if type is present set dict[type][i] = count
        for i  in range(0, len(x)):
            if dictionaryKey:
                for key, count in intervalDictionary[x[i]][dictionaryKey].items():
                    y[key][i] = count
            else:
                for key, count in intervalDictionary[x[i]].items():
                    y[key][i] = count

            # change unit of current x value from ticks to seconds
            x[i] = (x[i]/self.ticksPerSecond)

        # draw normal "plot" where for each type x = list of intervalStartTicks, y = dict[type]->(list)
        fig, ax1 = plt.subplots()
        for key in sorted(keys):
            ax1.plot(x, y[key], label=key)

        # sum up number of changes to be returned for external information/validation purposes
        for key, changelist in y.items():
            totalChanges += sum(changelist)

        ax1.set_xlabel("Seconds")
        ax1.set_ylabel("Changes")

        separateLegend(ax1)
        ax1.set_title(title)
        datacursor()
        plt.show()

        return totalChanges


# https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
def separateLegend(ax1):
    # Shrink current axis by 20%
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    legend = ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #export_legend(legend)
    #ax1.get_legend().remove()
    #ax1.set_position([box.x0, box.y0, box.width, box.height])


# https://stackoverflow.com/questions/4534480/get-legend-as-a-separate-picture-in-matplotlib
def export_legend(legend, filename="legend.png", expand=[-5,-5,5,5]):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox)