import matplotlib.pyplot as plt
from mpldatacursor import datacursor
from operator import add
from matplotlib.font_manager import FontProperties


class ChangeTypePlot():

    def __init__(self):
        self.reset()


    def reset(self):
        self.changedChunksAll = []
        self.changedChunksBlock = []
        self.changedChunksBlockEntity = []
        self.changedChunksEntity = []
        self.changedSectionsAll = []
        self.changedSectionsBlock = []
        self.changedSectionsBlockEntity = []
        self.changedSectionsEntity = []
        self.changedBlocks = []
        self.changedBlockEntities = []
        self.changedEntities = []
        self.bytesAll_min = []
        self.bytesBlock_min = []
        self.bytesBlockEntity_min = []
        self.bytesEntity_min = []
        self.bytesAll_mid = []
        self.bytesBlock_mid = []
        self.bytesBlockEntity_mid = []
        self.bytesEntity_mid = []
        self.bytesAll_max = []
        self.bytesBlock_max = []
        self.bytesBlockEntity_max = []
        self.bytesEntity_max = []

        # additional stuff
        self.changedSectionsPerChangedChunk = []
        self.changedBlocksPerChangedSection = []
        self.chunkChangeOverlap = []
        self.sectionChangeOverlap = []
        self.blockChangeSum = 0
        self.blockEntityChangeSum = 0
        self.entityChangeSum = 0
        self.bytesAllSum_min = 0
        self.bytesAllSum_mid = 0
        self.bytesAllSum_max = 0
        self.bytesBlockSum_min = 0
        self.bytesBlockSum_mid = 0
        self.bytesBlockSum_max = 0
        self.bytesBlockEntitySum_min = 0
        self.bytesBlockEntitySum_mid = 0
        self.bytesBlockEntitySum_max = 0
        self.bytesEntitySum_min = 0
        self.bytesEntitySum_mid = 0
        self.bytesEntitySum_max = 0

    def importIntervalData(self, intervalStatList):
        self.reset()

        for intervalStats in intervalStatList:
            self.changedChunksAll.append(intervalStats[0])
            self.changedChunksBlock.append(intervalStats[1])
            self.changedChunksBlockEntity.append(intervalStats[2])
            self.changedChunksEntity.append(intervalStats[3])
            self.changedSectionsAll.append(intervalStats[4])
            self.changedSectionsBlock.append(intervalStats[5])
            self.changedSectionsBlockEntity.append(intervalStats[6])
            self.changedSectionsEntity.append(intervalStats[7])
            self.changedBlocks.append(intervalStats[8])
            self.changedBlockEntities.append(intervalStats[9])
            self.changedEntities.append(intervalStats[10])
            self.bytesAll_min.append(intervalStats[11])
            self.bytesBlock_min.append(intervalStats[12])
            self.bytesBlockEntity_min.append(intervalStats[13])
            self.bytesEntity_min.append(intervalStats[14])
            self.bytesAll_mid.append(intervalStats[15])
            self.bytesBlock_mid.append(intervalStats[16])
            self.bytesBlockEntity_mid.append(intervalStats[17])
            self.bytesEntity_mid.append(intervalStats[18])
            self.bytesAll_max.append(intervalStats[19])
            self.bytesBlock_max.append(intervalStats[20])
            self.bytesBlockEntity_max.append(intervalStats[21])
            self.bytesEntity_max.append(intervalStats[22])

            # place to calculate additional stuff
            # number of changed sections per changed chunk
            ratio = 0 if self.changedChunksAll[-1] == 0 else self.changedSectionsAll[-1] / self.changedChunksAll[-1]
            self.changedSectionsPerChangedChunk.append(ratio)

            # number of changed blocks per changed section
            ratio = 0 if self.changedSectionsAll[-1] == 0 else self.changedBlocks[-1] / self.changedSectionsAll[-1]
            self.changedBlocksPerChangedSection.append(ratio)

            # change overlap
            self.chunkChangeOverlap.append(((self.changedChunksBlock[-1] + self.changedChunksBlockEntity[-1] + self.changedChunksEntity[-1]) - self.changedChunksAll[-1]))
            self.sectionChangeOverlap.append(((self.changedSectionsBlock[-1] + self.changedSectionsBlockEntity[-1] +
                                             self.changedSectionsEntity[-1]) - self.changedSectionsAll[-1]))
            # sum of changes per type
            self.blockChangeSum += self.changedBlocks[-1]
            self.blockEntityChangeSum += self.changedBlockEntities[-1]
            self.entityChangeSum += self.changedEntities[-1]
            # sum of changes (byte) per type
            self.bytesAllSum_min += self.bytesAll_min[-1]
            self.bytesAllSum_mid += self.bytesAll_mid[-1]
            self.bytesAllSum_max += self.bytesAll_max[-1]
            self.bytesBlockSum_min += self.bytesBlock_min[-1]
            self.bytesBlockSum_mid += self.bytesBlock_mid[-1]
            self.bytesBlockSum_max += self.bytesBlock_max[-1]
            self.bytesBlockEntitySum_min += self.bytesBlockEntity_min[-1]
            self.bytesBlockEntitySum_mid += self.bytesBlockEntity_mid[-1]
            self.bytesBlockEntitySum_max += self.bytesBlockEntity_max[-1]
            self.bytesEntitySum_min += self.bytesEntity_min[-1]
            self.bytesEntitySum_mid += self.bytesEntity_mid[-1]
            self.bytesEntitySum_max += self.bytesEntity_max[-1]


    def plot(self, intervalStatList, intervalLength):
        self.importIntervalData(intervalStatList)
        self.intervalLength = str(intervalLength)

        self.drawChunkChangePlot()
        self.drawSectionChangePlot()
        self.drawChangedSectionsPerChunkPlot()
        self.drawChangedBlocksPerSectionPlot()
        self.drawOverlap()
        self.drawAbsoluteChangePlot()
        self.drawChangedBytes()
        self.drawChangeBounds()
        self.drawTotalChangesPerType()

        self.logIntervalStatsToFile("intervalStats_" + self.intervalLength + "s.txt")


    def drawChunkChangePlot(self):
        x = range(0, len(self.changedChunksAll))
        fig, ax = plt.subplots()

        ax.plot(x, self.changedChunksBlock, label='changedChunksBlock')
        ax.plot(x, self.changedChunksBlockEntity, label='changedChunksBlockEntity')
        ax.plot(x, self.changedChunksEntity, label='changedChunksEntity')
        ax.plot(x, self.changedChunksAll, label='changedChunksAll')

        # ax.plot(self.serverWorldTimeTicks, self.changedEntities, label='# changed entities', linestyle="-", color='g')

        # ax.plot(self.serverWorldTimeTicks, self.changedTileEntities, label='# changed tile entities', color='orange')
        # ax.plot(self.serverWorldTimeTicks, self.changedBlocks, label='# changed blocks', color='red')
        # ax.plot(self.serverWorldTimeTicks, self.changedSections, label='# changed sections', linestyle='-',
        #        color='blue')
        # ax.plot(self.serverWorldTimeTicks, self.changedChunks, label='# changed chunks', color='black')

        plt.legend()
        ax.set(xlabel='Interval number (' + self.intervalLength + "s per Interval)", ylabel='Changed Chunks', title='Changed Chunks over time')
        ax.grid()
        datacursor()
        plt.show()

    def drawOverlap(self):
        x = range(0, len(self.changedChunksAll))
        fig, ax = plt.subplots()

        ax.plot(x, self.sectionChangeOverlap, label='sectionChangeOverlap', color="red")
        ax.plot(x, self.chunkChangeOverlap, label='chunkChangeOverlap', color="green")
        # inverted
        ax.plot(x, [i * -1 for i in self.chunkChangeOverlap], label='chunkChangeOverlap * (-1)', color="green")
        ax.plot(x, [i * -1 for i in self.sectionChangeOverlap], label='sectionChangeOverlap  * (-1)', color="red")

        plt.legend()
        ax.set(xlabel='Interval number (' + self.intervalLength + "s per Interval)", ylabel='Overlap (0 ... no overlap, \n 1 ... 2 objects changed because of different reasons)',
               title='Overlap over time')
        ax.grid()
        datacursor()
        plt.show()


    def drawSectionChangePlot(self):
        x = range(0, len(self.changedChunksAll))
        fig, ax = plt.subplots()

        ax.plot(x, self.changedSectionsBlock, label='changedSectionsBlock')
        ax.plot(x, self.changedSectionsBlockEntity, label='changedSectionsBlockEntity')
        ax.plot(x, self.changedSectionsEntity, label='changedSectionsEntity')
        ax.plot(x, self.changedSectionsAll, label='changedSectionsAll')

        plt.legend()
        ax.set(xlabel='Interval number ('  + self.intervalLength + "s per Interval)", ylabel='Changed Sections', title='Changed Sections over time')
        ax.grid()
        datacursor()
        plt.show()


    def drawAbsoluteChangePlot(self):
        x = range(0, len(self.changedChunksAll))
        fig, ax = plt.subplots()

        ax.plot(x, self.changedBlocks, label='changedBlocks')
        ax.plot(x, self.changedBlockEntities, label='changedBlockEntities')
        ax.plot(x, self.changedEntities, label='changedEntities')

        plt.legend()
        ax.set(xlabel='Interval number (' + self.intervalLength + "s per Interval)", ylabel='Changes', title='Changes over time')
        ax.grid()
        datacursor()
        plt.show()


    def drawChangedSectionsPerChunkPlot(self):
        x = range(0, len(self.changedSectionsPerChangedChunk))
        fig, ax = plt.subplots()

        ax.plot(x, self.changedSectionsPerChangedChunk, label='changedSectionsPerChangedChunk')

        plt.legend()
        ax.set(xlabel='Interval number (' + self.intervalLength + "s per Interval)", ylabel='Changes', title='Changed sections / changed chunks over time')
        ax.grid()
        datacursor()
        plt.show()


    def drawChangedBlocksPerSectionPlot(self):
        x = range(0, len(self.changedBlocksPerChangedSection))
        fig, ax = plt.subplots()

        ax.plot(x, self.changedBlocksPerChangedSection, label='changedBlocksPerChangedSection')

        plt.legend()
        ax.set(xlabel='Interval number (' + self.intervalLength + "s per Interval)", ylabel='Changes', title='Changed blocks / changed sections over time')
        ax.grid()
        datacursor()
        plt.show()


    def drawChangedBytes(self):
        x = range(0, len(self.changedChunksAll))
        fig, ax = plt.subplots()

        # min bytes
        ax.plot(x, self.bytesBlock_min, label='bytesBlock_min')
        ax.plot(x, self.bytesBlockEntity_min, label='bytesBlockEntity_min')
        ax.plot(x, self.bytesEntity_min, label='bytesEntity_min')
        ax.plot(x, self.bytesAll_min, label='bytesAll_min')
        bytesAll_min_avg = 0 if len(self.bytesAll_min) == 0 else sum(self.bytesAll_min)/len(self.bytesAll_min)
        ax.axhline(y=bytesAll_min_avg, label='bytesAll_min_avg', linestyle="--")

        # mid bytes
        ax.plot(x, self.bytesBlock_mid, label='bytesBlock_mid')
        ax.plot(x, self.bytesBlockEntity_mid, label='bytesBlockEntity_mid')
        ax.plot(x, self.bytesEntity_mid, label='bytesEntity_mid')
        ax.plot(x, self.bytesAll_mid, label='bytesAll_mid')
        bytesAll_mid_avg = 0 if len(self.bytesAll_mid) == 0 else sum(self.bytesAll_mid) / len(self.bytesAll_mid)
        ax.axhline(y=bytesAll_mid_avg, label='bytesAll_mid_avg', linestyle="--")

        # max bytes
        ax.plot(x, self.bytesBlock_max, label='bytesBlock_max')
        ax.plot(x, self.bytesBlockEntity_max, label='bytesBlockEntity_max')
        ax.plot(x, self.bytesEntity_max, label='bytesEntity_max')
        ax.plot(x, self.bytesAll_max, label='bytesAll_max')
        bytesAll_max_avg = 0 if len(self.bytesAll_max) == 0 else sum(self.bytesAll_max)/len(self.bytesAll_max)
        ax.axhline(y=bytesAll_max_avg, label='bytesAll_max_avg', linestyle="--")

        plt.legend()
        ax.set(xlabel='Interval number ('  + self.intervalLength + "s per Interval)", ylabel='Change in Byte', title='Changes (Byte) over time')
        ax.grid()
        datacursor()
        plt.show()


    def drawChangeBounds(self):
        x = range(0, len(self.changedChunksAll))
        fig, axs = plt.subplots(3,1)

        fontP = FontProperties()
        fontP.set_size("14")

        # upper graph (upper and lower bounds of sum of changes)
        kbyte_min = [bytes / 1000 for bytes in self.bytesAll_min]
        kbyte_max = [bytes / 1000 for bytes in self.bytesAll_max]

        # max bytes
        axs[0].plot(x, kbyte_max, label='upper bound', color="red")
        bytesAll_max_avg = 0 if len(self.bytesAll_max) == 0 else sum(kbyte_max) / len(kbyte_max)
        axs[0].axhline(y=bytesAll_max_avg, label='upper bound (avg)', color="red", linestyle="--")

        # min bytes
        axs[0].plot(x, kbyte_min, label='lower bound', color="green")
        bytesAll_min_avg = 0 if len(self.bytesAll_min) == 0 else sum(kbyte_min) / len(kbyte_min)
        axs[0].axhline(y=bytesAll_min_avg, label='lower bound (avg)', color="green", linestyle="--")


        axs[0].legend(loc='upper right')
        axs[0].set(xlabel='Time [s]', ylabel='Size [kB]',
               title='Sum of all changes over time')
        axs[0].grid()
        axs[0].set_xlim(left=0, right=6000)
        #axs[0].set_ylim(bottom=-5)
        axs[0].set_ylim(top=1000)


        # middle graph (upper and lower bounds of entity changes)
        kbyte_min = [bytes / 1000 for bytes in self.bytesEntity_min]
        kbyte_max = [bytes / 1000 for bytes in self.bytesEntity_max]

        # max bytes
        axs[1].plot(x, kbyte_max, label='upper bound', color="red")
        bytesAll_max_avg = 0 if len(self.bytesAll_max) == 0 else sum(kbyte_max) / len(kbyte_max)
        axs[1].axhline(y=bytesAll_max_avg, label='upper bound (avg)', color="red", linestyle="--")

        # min bytes
        axs[1].plot(x, kbyte_min, label='lower bound', color="green")
        bytesAll_min_avg = 0 if len(self.bytesAll_min) == 0 else sum(kbyte_min) / len(kbyte_min)
        axs[1].axhline(y=bytesAll_min_avg, label='lower bound (avg)', color="green", linestyle="--")

        axs[1].legend(loc='upper right')
        axs[1].set(xlabel='Time [s]', ylabel='Size [kB]',
                   title='Entity changes over time')
        axs[1].grid()
        axs[1].set_xlim(left=0, right=6000)
        #axs[1].set_ylim(bottom=-5)
        axs[1].set_ylim(top=1000)


        # lower graph (upper and lower bounds of block and blockEntity changes)
        kbyte_block_min = [bytes / 1000 for bytes in self.bytesBlock_min]
        kbyte_block_max = [bytes / 1000 for bytes in self.bytesBlock_max]
        kbyte_block_entity_min = [bytes / 1000 for bytes in self.bytesBlockEntity_min]
        kbyte_block_entity_max = [bytes / 1000 for bytes in self.bytesBlockEntity_max]

        kbyte_blockentity_min = list(map(add, kbyte_block_min, kbyte_block_entity_min))
        kbyte_blockentity_max = list(map(add, kbyte_block_max, kbyte_block_entity_max))

        axs[2].plot(x, kbyte_blockentity_max, label='upper bound', color="red")
        kbyte_block_entity_max_avg = 0 if len(kbyte_blockentity_max) == 0 else sum(kbyte_blockentity_max) / len(kbyte_blockentity_max)
        axs[2].axhline(y=kbyte_block_entity_max_avg, label='upper bound (avg)', color="red", linestyle="--")

        # block and block_entity min/max bytes
        axs[2].plot(x, kbyte_blockentity_min, label='lower bound', color="green")
        kbyte_block_entity_min_avg = 0 if len(kbyte_blockentity_min) == 0 else sum(kbyte_blockentity_min) / len(kbyte_blockentity_min)
        axs[2].axhline(y=kbyte_block_entity_min_avg, label='lower bound (avg)', color="green", linestyle="--")

        axs[2].legend(loc='upper right')
        axs[2].set(xlabel='Time [s]', ylabel='Size [kB]',
                   title='Block changes over time')
        axs[2].grid()
        axs[2].set_xlim(left=0, right=6000)
        #axs[2].set_yticks([0,200,400,600])
        axs[2].set_ylim(top=1000)


        #datacursor()
        plt.tight_layout(pad=0.0, h_pad=0.0, w_pad=0.0)
        plt.subplots_adjust(hspace=0.4)
        plt.show()


    def drawTotalChangesPerType(self):

        explode = (0, 0, 0)
        labels = ['Blocks', 'BlockEntities', 'Entities']
        countSums = [self.blockChangeSum, self.blockEntityChangeSum, self.entityChangeSum]
        byteSums_min = [self.bytesBlockSum_min, self.bytesBlockEntitySum_min, self.bytesEntitySum_min]
        byteSums_mid = [self.bytesBlockSum_mid, self.bytesBlockEntitySum_mid, self.bytesEntitySum_mid]
        byteSums_max = [self.bytesBlockSum_max, self.bytesBlockEntitySum_max, self.bytesEntitySum_max]

        print("Counts (Blocks, BlockEntities, Entities)")
        print(countSums)
        print("Size-sums min: (Blocks, BlockEntites, Entities)")
        print(byteSums_min)
        print("Size-sums mid: (Blocks, BlockEntites, Entities)")
        print(byteSums_mid)
        print("Size-sums max: (Blocks, BlockEntites, Entities)")
        print(byteSums_max)

        # sanity check
        if sum(byteSums_min) != self.bytesAllSum_min:
            raise ValueError(str(byteSums_min) != self.bytesAllSum_min)
        if sum(byteSums_mid) != self.bytesAllSum_mid:
            raise ValueError(str(byteSums_mid) != self.bytesAllSum_mid)
        if sum(byteSums_max) != self.bytesAllSum_max:
            raise ValueError(str(byteSums_max) != self.bytesAllSum_max)

        fig, axes = plt.subplots(2, 2)
        axes[0,0].pie(countSums, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        axes[0, 0].set_title("Total # of Changes:\n" + str(sum(countSums)))

        axes[0, 1].pie(byteSums_min, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        axes[0, 1].set_title("Total Bytes changed (min):\n" + str(sum(byteSums_min)))

        axes[1, 0].pie(byteSums_mid, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        axes[1, 0].set_title("Total Bytes changed (mid):\n" + str(sum(byteSums_mid)))

        axes[1, 1].pie(byteSums_max, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        axes[1, 1].set_title("Total Bytes changed (max):\n" + str(sum(byteSums_max)))

        axes[0, 0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        axes[0, 1].axis('equal')
        axes[1, 0].axis('equal')
        axes[1, 1].axis('equal')

        axes[0, 0].legend()
        #ax2.legend()
        #ax3.legend()
        #ax4.legend()

        plt.show()

    def logIntervalStatsToFile(self, path):
        with open(path, "w") as logfile:
            logfile.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                '#chunks_all', ' #chunks_block',
                ' #chunks_block_entity', '  #chunks_entity', '#sections_all', '#sections_block',
                '#sections_block_entity',
                '#sections_entity', '#blocks', ' #block_entity', '#entity', '#bytes_all_min', '#bytes_block_min',
                '#bytes_block_entity_min', '#bytes_entity_min'
                , '#bytes_all_mid', '#bytes_block_mid', '#bytes_block_entity_mid', '#bytes_entity_mid',
                '#bytes_all_max', '#bytes_block_max', '#bytes_block_entity_max', '#bytes_entity_max', '#changedSections/#changedChunks', '#changedBlocks/#changedSections'))

            for i in range (0, len(self.changedChunksAll)):
                logfile.write(
                    '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                        self.changedChunksAll[i],
                        self.changedChunksBlock[i],
                        self.changedChunksBlockEntity[i],
                        self.changedChunksEntity[i],
                        self.changedSectionsAll[i],
                        self.changedSectionsBlock[i],
                        self.changedSectionsBlockEntity[i],
                        self.changedSectionsEntity[i],
                        self.changedBlocks[i],
                        self.changedBlockEntities[i],
                        self.changedEntities[i],
                        self.bytesAll_min[i],
                        self.bytesBlock_min[i],
                        self.bytesBlockEntity_min[i],
                        self.bytesEntity_min[i],
                        self.bytesAll_mid[i],
                        self.bytesBlock_mid[i],
                        self.bytesBlockEntity_mid[i],
                        self.bytesEntity_mid[i],
                        self.bytesAll_max[i],
                        self.bytesBlock_max[i],
                        self.bytesBlockEntity_max[i],
                        self.bytesEntity_max[i],
                        self.changedSectionsPerChangedChunk[i],
                        self.changedBlocksPerChangedSection[i]))
