import csv
import sys
import matplotlib.pyplot as plt
from mpldatacursor import datacursor
import pandas as pd
from change_statistics.basicUtils import *

intervals = {}

def importIntervalData(path):
    key = path.split("/")[-1].split("_")[-1].split(".txt")[0]

    if key not in intervals:
        intervals[key] = {
        'changedChunksAll': [],
        'changedChunksBlock': [],
        'changedChunksBlockEntity': [],
        'changedChunksEntity': [],
        'changedSectionsAll': [],
        'changedSectionsBlock': [],
        'changedSectionsBlockEntity': [],
        'changedSectionsEntity': [],
        'changedBlocks': [],
        'changedBlockEntities': [],
        'changedEntities': [],
        'bytesAll_min':[],
        'bytesBlock_min':[],
        'bytesBlockEntity_min':[],
        'bytesEntity_min':[],
        'bytesAll_mid': [],
        'bytesBlock_mid': [],
        'bytesBlockEntity_mid': [],
        'bytesEntity_mid': [],
        'bytesAll_max': [],
        'bytesBlock_max': [],
        'bytesBlockEntity_max': [],
        'bytesEntity_max': [],
        'changedSectionsPerChangedChunk': []
        }

    with open(path) as f:
        next(f) # skip the header
        reader = csv.reader(f, delimiter="\t")

        for row in reader:
            intervals[key]["changedChunksAll"].append(int(row[0]))
            intervals[key]["changedChunksBlock"].append(int(row[1]))
            intervals[key]["changedChunksBlockEntity"].append(int(row[2]))
            intervals[key]["changedChunksEntity"].append(int(row[3]))
            intervals[key]["changedSectionsAll"].append(int(row[4]))
            intervals[key]["changedSectionsBlock"].append(int(row[5]))
            intervals[key]["changedSectionsBlockEntity"].append(int(row[6]))
            intervals[key]["changedSectionsEntity"].append(int(row[7]))
            intervals[key]["changedBlocks"].append(int(row[8]))
            intervals[key]["changedBlockEntities"].append(int(row[9]))
            intervals[key]["changedEntities"].append(int(row[10]))
            intervals[key]["bytesAll_min"].append(int(row[11]))
            intervals[key]["bytesBlock_min"].append(int(row[12]))
            intervals[key]["bytesBlockEntity_min"].append(int(row[13]))
            intervals[key]["bytesEntity_min"].append(int(row[14]))
            intervals[key]["bytesAll_mid"].append(int(row[15]))
            intervals[key]["bytesBlock_mid"].append(int(row[16]))
            intervals[key]["bytesBlockEntity_mid"].append(int(row[17]))
            intervals[key]["bytesEntity_mid"].append(int(row[18]))
            intervals[key]["bytesAll_max"].append(int(row[19]))
            intervals[key]["bytesBlock_max"].append(int(row[20]))
            intervals[key]["bytesBlockEntity_max"].append(int(row[21]))
            intervals[key]["bytesEntity_max"].append(int(row[22]))
            intervals[key]["changedSectionsPerChangedChunk"].append(float(row[23]))


def plotIntervals(column, xLabel, yLabel, title):
    # changedChunks
    fig, ax = plt.subplots()

    for key, intervalData in intervals.items():
        intervalLength = float(key.replace("s", ""))
        y = intervalData[column]
        x = [i * intervalLength for i in range(0, len(y))]

        ax.plot(x, y, label=key)

    plt.legend()
    ax.set(xlabel=xLabel, ylabel=yLabel,title=title)
    ax.grid()
    datacursor()
    plt.show()


def showComparisonBoxplots(column):
    byteSum_x = []
    byteSum_y = []
    for key, intervalData in intervals.items():
        byteSum_x.append(column+"_"+key)
        byteSum_y.append(sum(intervalData[column]))
        print(byteSum_x[-1] + ":\t" + str(byteSum_y[-1]))

        df_dict = {column + "_" + key: intervalData[column]}
        df= pd.DataFrame.from_dict(df_dict)
        showBoxplot(df, column+"_"+key)


    fig, ax = plt.subplots(1, 1)
    ax.pie(byteSum_y, labels=byteSum_x, autopct='%1.1f%%', startangle=90)
    plt.show(block=True)





def showBoxplot(data_frame, title):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
    data_frame.boxplot(ax=ax1, return_type='axes')
    ax1.set_title('With outliers')

    data_frame.boxplot(ax=ax2, return_type='axes', showfliers=False)
    ax2.set_title('Without outliers')

    plt.suptitle(title)

    plt.show(block=True)






# main entry point of the script
if len(sys.argv)<2:
    print("usage: python3 " + sys.argv[0] + " intervalStats_0.5s.txt intervalStats_1.0s.txt")
    exit(-1)

for path in sys.argv[1:]:
    print("reading: " + path)
    importIntervalData(path)

plotIntervals('changedChunksAll', 'Time [s]', '# Changed Chunks', 'Changed Chunks over time')
plotIntervals('changedSectionsAll', 'Time [s]', '# Changed Sections', 'Changed Sections over time')
plotIntervals('changedBlocks', 'Time [s]', '# Changed Blocks', 'Changed Blocks over time')
plotIntervals('changedBlockEntities', 'Time [s]', '# Changed Block Entities', 'Changed BlockEntities over time')
plotIntervals('changedEntities', 'Time [s]', '# Changed Entities', 'Changed Entities over time')
plotIntervals('bytesAll_min', 'Time [s]', 'Change [Byte]', 'Change in bytesAll_min over time')
plotIntervals('changedSectionsPerChangedChunk', 'Time [s]', '# Changed Sections', 'Changed Sections per changed Chunk over time')


showComparisonBoxplots('bytesAll_min')