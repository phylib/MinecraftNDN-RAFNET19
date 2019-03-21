import matplotlib.pyplot as plt
from mpldatacursor import datacursor
import pandas as pd


class ChangeTypeStatisticPlot():

    def __init__(self):
        self.reset()


    def reset(self):
        self.intervals = {
            "changedChunksAll":[],
            "changedChunksBlock":[],
            "changedChunksBlockEntity":[],
            "changedChunksEntity":[],
            "changedSectionsAll":[],
            "changedSectionsBlock":[],
            "changedSectionsBlockEntity":[],
            "changedSectionsEntity":[],
            "changedBlocks":[],
            "changedBlockEntities":[],
            "changedEntities":[],
            "bytesAll_min":[],
            "bytesBlock_min":[],
            "bytesBlockEntity_min":[],
            "bytesEntity_min":[],
            "bytesAll_mid": [],
            "bytesBlock_mid": [],
            "bytesBlockEntity_mid": [],
            "bytesEntity_mid": [],
            "bytesAll_max": [],
            "bytesBlock_max": [],
            "bytesBlockEntity_max": [],
            "bytesEntity_max": [],
            "changedSectionsPerChangedChunk": [],
            "changedBlocksPerChangedSection": []
        }

    def importIntervalData(self, intervalStatList):
        self.reset()

        for intervalStats in intervalStatList:
            self.intervals["changedChunksAll"].append(intervalStats[0])
            self.intervals["changedChunksBlock"].append(intervalStats[1])
            self.intervals["changedChunksBlockEntity"].append(intervalStats[2])
            self.intervals["changedChunksEntity"].append(intervalStats[3])
            self.intervals["changedSectionsAll"].append(intervalStats[4])
            self.intervals["changedSectionsBlock"].append(intervalStats[5])
            self.intervals["changedSectionsBlockEntity"].append(intervalStats[6])
            self.intervals["changedSectionsEntity"].append(intervalStats[7])
            self.intervals["changedBlocks"].append(intervalStats[8])
            self.intervals["changedBlockEntities"].append(intervalStats[9])
            self.intervals["changedEntities"].append(intervalStats[10])
            self.intervals["bytesAll_min"].append(intervalStats[11])
            self.intervals["bytesBlock_min"].append(intervalStats[12])
            self.intervals["bytesBlockEntity_min"].append(intervalStats[13])
            self.intervals["bytesEntity_min"].append(intervalStats[14])
            self.intervals["bytesAll_mid"].append(intervalStats[15])
            self.intervals["bytesBlock_mid"].append(intervalStats[16])
            self.intervals["bytesBlockEntity_mid"].append(intervalStats[17])
            self.intervals["bytesEntity_mid"].append(intervalStats[18])
            self.intervals["bytesAll_max"].append(intervalStats[19])
            self.intervals["bytesBlock_max"].append(intervalStats[20])
            self.intervals["bytesBlockEntity_max"].append(intervalStats[21])
            self.intervals["bytesEntity_max"].append(intervalStats[22])

            # place to calculate additional stuff
            # number of changed sections per changed chunk
            ratio = 0 if self.intervals["changedChunksAll"][-1] == 0 else self.intervals["changedSectionsAll"][-1] / self.intervals["changedChunksAll"][-1]
            self.intervals["changedSectionsPerChangedChunk"].append(ratio)

            # number of changed blocks per changed section
            ratio = 0 if self.intervals['changedSectionsAll'][-1] == 0 else self.intervals['changedBlocks'][-1] / self.intervals['changedSectionsAll'][-1]
            self.intervals['changedBlocksPerChangedSection'].append(ratio)

        self.data_frame = pd.DataFrame(self.intervals)


    def plot(self, intervalStatList, intervalLength):
        self.importIntervalData(intervalStatList)
        self.intervalLength = str(intervalLength)

        # let pandas describe the data_frame
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(self.data_frame.describe())
            self.data_frame.describe().to_csv("plotChangeTypeStatistics_" + self.intervalLength + "s.csv")

        # changed chunks
        self.showBoxplot(self.data_frame, ["changedChunksAll"], "changedChunksAll")
        self.showBoxplot(self.data_frame, ["changedChunksBlock"], "changedChunksBlock")
        self.showBoxplot(self.data_frame, ["changedChunksBlockEntity"], "changedChunksBlockEntity")
        self.showBoxplot(self.data_frame, ["changedChunksEntity"], "changedChunksEntity")
        self.showBoxplots(self.data_frame, ["changedChunksBlock","changedChunksBlockEntity","changedChunksEntity"], "ChangedChunks", False)

        # changed sections
        self.showBoxplot(self.data_frame, ["changedSectionsAll"], "changedSectionsAll")
        self.showBoxplot(self.data_frame, ["changedSectionsBlock"], "changedSectionsBlock")
        self.showBoxplot(self.data_frame, ["changedSectionsBlockEntity"], "changedSectionsBlockEntity")
        self.showBoxplot(self.data_frame, ["changedSectionsEntity"], "changedSectionsEntity")
        self.showBoxplots(self.data_frame, ["changedSectionsBlock", "changedSectionsBlockEntity", "changedSectionsEntity"], "ChangedSections", False)

        # changed sections per changed chunk
        self.showBoxplot(self.data_frame, ["changedSectionsPerChangedChunk"], "changedSectionsPerChangedChunk")

        # changed blocks, blockEntities, Entities
        self.showBoxplot(self.data_frame, ["changedBlocks"], "changedBlocks")
        self.showBoxplot(self.data_frame, ["changedBlockEntities"], "changedBlockEntities")
        self.showBoxplot(self.data_frame, ["changedEntities"], "changedEntities")
        self.showBoxplots(self.data_frame, ["changedBlocks", "changedBlockEntities", "changedEntities"], "Changed Blocks/BlockEntities/Entities", False)

        # changed sections per changed chunk
        self.showBoxplot(self.data_frame, ["changedBlocksPerChangedSection"], "changedBlocksPerChangedSection")

        # bytes changes (min)
        self.showBoxplot(self.data_frame, ["bytesAll_min"], "bytesAll_min")
        self.showBoxplot(self.data_frame, ["bytesBlock_min"], "bytesBlock_min")
        self.showBoxplot(self.data_frame, ["bytesBlockEntity_min"], "bytesBlockEntity_min")
        self.showBoxplot(self.data_frame, ["bytesEntity_min"], "bytesEntity_min")
        self.showBoxplots(self.data_frame, ["bytesBlock_min", "bytesBlockEntity_min", "bytesEntity_min"], "#Bytes changed (min)", False)

        # bytes changes (mid)
        self.showBoxplot(self.data_frame, ["bytesAll_mid"], "bytesAll_mid")
        self.showBoxplot(self.data_frame, ["bytesBlock_mid"], "bytesBlock_mid")
        self.showBoxplot(self.data_frame, ["bytesBlockEntity_mid"], "bytesBlockEntity_mid")
        self.showBoxplot(self.data_frame, ["bytesEntity_mid"], "bytesEntity_mid")
        self.showBoxplots(self.data_frame, ["bytesBlock_mid", "bytesBlockEntity_mid", "bytesEntity_mid"], "#Bytes changed (mid)", False)

        # bytes changes (max)
        self.showBoxplot(self.data_frame, ["bytesAll_max"], "bytesAll_max")
        self.showBoxplot(self.data_frame, ["bytesBlock_max"], "bytesBlock_max")
        self.showBoxplot(self.data_frame, ["bytesBlockEntity_max"], "bytesBlockEntity_max")
        self.showBoxplot(self.data_frame, ["bytesEntity_max"], "bytesEntity_max")
        self.showBoxplots(self.data_frame, ["bytesBlock_max", "bytesBlockEntity_max", "bytesEntity_max"], "#Bytes changed (max)", False)

        self.showBoxplots(self.data_frame, ["bytesAll_min","bytesAll_mid","bytesAll_max", "bytesBlock_min","bytesBlock_mid", "bytesBlock_max"
            , "bytesBlockEntity_min","bytesBlockEntity_mid", "bytesBlockEntity_max", "bytesEntity_min","bytesEntity_mid", "bytesEntity_max"],
                          "#Bytes changed (min, mid, max)", False)

        # TODO: check bytes calculation



    def showBoxplot(self, data_frame, keys, title):
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
        data_frame.boxplot(column=keys, ax=ax1, return_type='axes')
        plt.suptitle(title + (" ("+ str(self.intervalLength) + "s interval)"))
        ax1.set_title('With outliers')

        data_frame.boxplot(column=keys, ax=ax2, return_type='axes', showfliers=False)
        ax2.set_title('Without outliers')

        plt.show(block=True)


    def showBoxplots(self, data_frame, keys, title, showFliers):
        f, ax1 = plt.subplots()
        data_frame.boxplot(column=keys, ax=ax1, return_type='axes', showfliers=showFliers)
        plt.suptitle(title + (" ("+ str(self.intervalLength) + "s interval)"))

        ax1.set_title('With outliers' if showFliers else 'Without outliers')
        plt.show(block=True)
