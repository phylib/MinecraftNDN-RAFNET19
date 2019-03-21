from change_statistics import IntervalDataSink
from change_statistics.basicUtils import ChangeType
from change_statistics.other.plotChangeTypes import ChangeTypePlot
from change_statistics.other.plotChangeTypeStatistics import ChangeTypeStatisticPlot

from math import ceil
import re
import copy


class IntervalStatPrinter(IntervalDataSink.IntervalDataSink):

    def __init__(self, intervalLength):
        super(IntervalStatPrinter, self).__init__()
        self.intervalLength = intervalLength
        self.intervalStatistics = []
        self.BlockEntities = {} # continuously update to get idea of max_bytes as "complete NBT string transmitted @ every interval", not affected by reset()!
        self.Entities = {} # see above
        self.reset()
        # print header
        print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format('#chunks_all', ' #chunks_block',
        ' #chunks_block_entity', '  #chunks_entity', '#sections_all', '#sections_block', '#sections_block_entity',
        '#sections_entity', '#blocks', ' #block_entity', '#entity', '#bytes_all_min', '#bytes_block_min', '#bytes_block_entity_min', '#bytes_entity_min'
                                    , '#bytes_all_mid', '#bytes_block_mid', '#bytes_block_entity_mid', '#bytes_entity_mid',
                                     '#bytes_all_max', '#bytes_block_max', '#bytes_block_entity_max', '#bytes_entity_max'))


    def reset(self):
        self.changedChunksAll = set()
        self.changedChunksBlock = set()
        self.changedChunksBlockEntity = set()
        self.changedChunksEntity = set()
        self.changedSectionsAll = set()
        self.changedSectionsBlock = set()
        self.changedSectionsBlockEntity = set()
        self.changedSectionsEntity = set()
        self.changedBlocks = {}
        self.changedBlockEntities = {}
        self.changedEntities = {}
        self.bytesAll_min = 0
        self.bytesBlock_min = 0
        self.bytesBlockEntity_min = 0
        self.bytesEntity_min = 0
        self.bytesAll_mid = 0
        self.bytesBlock_mid = 0
        self.bytesBlockEntity_mid = 0
        self.bytesEntity_mid = 0
        self.bytesAll_max = 0
        self.bytesBlock_max = 0
        self.bytesBlockEntity_max = 0
        self.bytesEntity_max = 0


    def receiveIntervalData(self, intervalData):
        for entry in intervalData.entries:
            type = entry["type"]
            if type == ChangeType.entity:
                self.processEntityChange(entry)
            elif type == ChangeType.tile_entity:
                self.processBlockEntityChange(entry)
            elif type == ChangeType.block:
                self.processBlockChange(entry)
            # do not handle status lines

        # calculate statistics, print line and reset
        self.finalizeSection()
        self.reset()


    def getChangeCoordinates(self, change):
        chunkCoord = change['world'] + '/' + change['chunk']
        sectionCoord = chunkCoord + '/' + change['section']
        blockCoord = chunkCoord + '/(' + change['xpos'] + ',' + change['ypos'] + ',' + change['zpos'] + ')'

        return chunkCoord, sectionCoord, blockCoord


    def getDictFromNbtChanges(self, nbtChanges):
        result = {}
        if nbtChanges.startswith('['):
            nbtChanges = nbtChanges[1:]
        if nbtChanges.endswith(']'):
            nbtChanges = nbtChanges[:-1]
        nbtChanges = nbtChanges.replace("<added>","")
        if "<removed>" in nbtChanges:
            return result # nothing to be done here
        nbtChanges = nbtChanges.replace("[","(")
        nbtChanges = nbtChanges.replace("]", ")")

        #parts = nbtChanges.split(",")
        parts = re.split(r',\s*(?![^()]*\))', nbtChanges)

        for item in parts:
            item = item.replace("(","")
            item = item.replace(")", "")
            item = item.replace("{", "")
            item = item.replace("}", "")
            item = item.replace("+", "")
            item = item.replace("-", "")
            segments = item.split(":")
            key = segments[0].strip()
            list = ":".join(segments[1:])

            listParts = list.split(",")
            if len(listParts) <= 1:
                result[key] = list.strip()
            else:
                cnt = 0
                for item in listParts:
                    result[key+"/" + str(cnt)] = item.strip()
                    cnt += 1

        return result


    def mergeNbtChangeDicts(self, prev, new):
        result = new

        for prevKey, prevValue in prev.items():
            # preserve possible previous (bigger) magnitude of change
            if prevKey in result:
                if len(prevValue) > len(result[prevKey]):
                    result[prevKey] = prevValue
            else: # don't "forget" about previous changes
                result[prevKey] = prevValue
        return result


    # integrates change of block into overall statistics
    def processBlockChange(self, change):
        chunkCoord, sectionCoord, blockCoord = self.getChangeCoordinates(change)

        self.changedChunksAll.add(chunkCoord)
        self.changedChunksBlock.add(chunkCoord)
        self.changedSectionsAll.add(sectionCoord)
        self.changedSectionsBlock.add(sectionCoord)

        if blockCoord in self.changedBlocks:
            prevChange = self.changedBlocks[blockCoord]
            for key in ['material', 'skylight', 'emittedLight', 'blockData']:
                if prevChange[key] and not change[key]:  # do not "forget" about changes
                    change[key] = prevChange[key]

        # store "new" block change
        self.changedBlocks[blockCoord] = change

        # update mid/max number of bytes changed for this type
        bytes_mid = 4 + 8  # ceil((16+3*4)/8) + block position (8byte) # https://wiki.vg/index.php?title=Protocol&oldid=14204#Data_types
        bytes_max = bytes_mid
        self.bytesBlock_mid += bytes_mid
        self.bytesAll_mid += bytes_mid
        self.bytesBlock_max += bytes_max
        self.bytesAll_max += bytes_max


    # integrates change of block/tile entity into overall statistics
    def processBlockEntityChange(self, change):
        chunkCoord, sectionCoord, blockCoord = self.getChangeCoordinates(change)

        self.changedChunksAll.add(chunkCoord)
        self.changedChunksBlockEntity.add(chunkCoord)
        self.changedSectionsAll.add(sectionCoord)
        self.changedSectionsBlockEntity.add(sectionCoord)

        uuid = change['uuid']
        currentChanges = self.getDictFromNbtChanges(change['changes'])

        if uuid in self.changedBlockEntities:
            # update change
            prevChange = self.changedBlockEntities[uuid]
            currentChanges = self.mergeNbtChangeDicts(prevChange, currentChanges)

        # store up to date block entity change (for bytes_min calculation)
        self.changedBlockEntities[uuid] = copy.deepcopy(currentChanges)

        # continuously update tracked block entities
        if uuid in self.BlockEntities:
            # update change
            blockEntity = self.BlockEntities[uuid]
            updatedBlockEntity = self.mergeNbtChangeDicts(blockEntity, currentChanges)
            self.BlockEntities[uuid] = updatedBlockEntity
        else:
            self.BlockEntities[uuid] = currentChanges

        # update mid number of bytes changed for this type # https://wiki.vg/index.php?title=Protocol&oldid=14204#Data_types
        bytes_mid = 16 + len(
            change['changes'])  # transmit whole NBT-diff (UUID (16 bytes) + keys/paths and respective new values)
        self.bytesAll_mid += bytes_mid
        self.bytesBlockEntity_mid += bytes_mid

        # update max number of bytes changed
        dstr = str(self.BlockEntities[uuid])
        bytes_max = len(dstr)
        self.bytesAll_max += bytes_max
        self.bytesBlockEntity_max += bytes_max


    # integrates change of entity into overall statistics
    def processEntityChange(self, change):
        chunkCoord, sectionCoord, blockCoord = self.getChangeCoordinates(change)

        self.changedChunksAll.add(chunkCoord)
        self.changedChunksEntity.add(chunkCoord)
        self.changedSectionsAll.add(sectionCoord)
        self.changedSectionsEntity.add(sectionCoord)

        uuid = change['uuid']
        currentChanges = self.getDictFromNbtChanges(change['changes'])

        if uuid in self.changedEntities:
            # update change
            prevChange = self.changedEntities[uuid]
            currentChanges = self.mergeNbtChangeDicts(prevChange, currentChanges)

        # store up to date block entity change (for bytes_min calculation)
        self.changedEntities[uuid] = copy.deepcopy(currentChanges)

        # continuously update tracked entities
        if uuid in self.Entities:
            # update change
            entity = self.Entities[uuid]
            updatedentity = self.mergeNbtChangeDicts(entity, currentChanges)
            self.Entities[uuid] = updatedentity
        else:
            self.Entities[uuid] = currentChanges

        # update mid number of bytes changed for this type # https://wiki.vg/index.php?title=Protocol&oldid=14204#Data_types
        bytes_mid = 16 + len(change['changes'])  # transmit whole NBT-diff (UUID (16 bytes) + keys/paths and respective new values)
        self.bytesAll_mid += bytes_mid
        self.bytesEntity_mid += bytes_mid

        # update max number of bytes changed
        dstr = str(self.Entities[uuid])
        bytes_max = len(dstr)
        self.bytesAll_max += bytes_max
        self.bytesEntity_max += bytes_max


    def finalizeSection(self):
        # calculate changed bytes going through all (possibly updated, final versions of) change objects (blocks, blockEntities, entities)
        # block changes
        for blockCoord, change in self.changedBlocks.items():
            bits = 0
            # https://minecraft.gamepedia.com/Chunk_format (BlockID==material: 12bits, BlockData,BlockLight and SkyLight: 4bits)
            for key in ['material', 'skylight', 'emittedLight', 'blockData']:
                if change[key]:
                    if key == 'material':
                        bits += 16 # 12 but "rounded up" to 16 to be sure
                    else:
                        bits += 4
            bytes_min = ceil(bits / 8)
            self.bytesBlock_min += bytes_min
            self.bytesAll_min += bytes_min

        # block entity changes
        integerSizeList = ["x","y","z"]
        byteSizeList = ["Lock"]
        ignoreList = ["Items", "Items/Slot"]
        for uuid, change in self.changedBlockEntities.items():
            bytes_min = 0
            for key, value in change.items():
                if ":" in value and not "id:" in value and not "minecraft:" in value:
                    parts = value.split(":")
                    if len(parts) >= 2:
                        value = parts[1]
                if key in ignoreList:
                    pass
                elif value.isdigit():
                    bytes_min += 4 # assume the worst
                elif value.endswith("s") and value[:-1].isdigit():
                    bytes_min += 2 # assuming s stands for "short", which usually is 2 bytes
                elif value.endswith("b") and value[:-1].isdigit():
                    bytes_min += 1 # assuming b stands for "byte"
                elif value.endswith("L") and value[:-1].isdigit():
                    bytes_min += 8  # assuming L stands for "long", which is usually 8+ bytes
                elif "id" in key or "id:" in value or "minecraft:" in value:
                    bytes_min += 2  # assuming minecraft ids fit into a short
                elif key in integerSizeList:
                    bytes_min += 4
                elif key in byteSizeList:
                    bytes_min += 1
                elif "Weight" in value:
                    bytes_min += 1
                else:
                    raise ValueError("key: " + key +"\tvalue: " + value)
            self.bytesAll_min += bytes_min
            self.bytesBlockEntity_min += bytes_min

        # entity changes
        integerSizeList = ["x", "y", "z"]
        byteSizeList = ["Lock"]
        stringList = ["lastKnownName", "SpawnWorld", "Thrower", "ownerName", "Type"]
        prefixStringList = ["recipeBook/recipes/minecraft","recipeBook/toBeDisplayed/minecraft"]
        ignoreList = ["Items", "Items/Slot", "Name", "recipeBook", "toBeDisplayed", "EnderItems", "Inventory"]
        prefixIgnoreList = ["Modifiers", "HandItems", "ArmorItems", "Attributes", "Inventory/Slot", 'RootVehicle']
        for uuid, change in self.changedEntities.items():
            bytes_min = 0
            for key, value in change.items():
                cont = True
                for prefix in prefixIgnoreList:
                    if key.startswith(prefix):
                        cont = False
                        break
                if not cont:
                    continue

                cont = True
                for prefix in prefixStringList:
                    if key.startswith(prefix):
                        bytes_min += len(value)
                        cont = False
                        break
                if not cont:
                    continue

                if ":" in value and not "id:" in value and not "minecraft:" in value:
                    parts = value.split(":")
                    if len(parts) >= 2:
                        value = parts[1]
                if key in ignoreList:
                    pass
                elif value == '""':
                    pass
                elif value.isdigit():
                    bytes_min += 4  # assume the worst
                elif value.endswith("s") and value[:-1].isdigit():
                    bytes_min += 2  # assuming s stands for "short", which usually is 2 bytes
                elif value.endswith("b") and value[:-1].isdigit():
                    bytes_min += 1  # assuming b stands for "byte"
                elif value.endswith("f") and value[:-1].replace('.','',1).replace("E","",1).isdigit():
                    bytes_min += 4  # assuming f stands for "float"
                elif value.endswith("d") and value[:-1].replace('.', '', 1).replace("E","",1).isdigit():
                    bytes_min += 8  # assuming d stands for "double"
                elif value.endswith("L") and value[:-1].isdigit():
                    bytes_min += 8  # assuming L stands for "long", which is usually 8+ bytes
                elif "id" in key or "id:" in value or "minecraft:" in value:
                    bytes_min += 2  # assuming minecraft ids fit into a short
                elif key in integerSizeList:
                    bytes_min += 4
                elif key in byteSizeList:
                    bytes_min += 1
                elif key in stringList:
                    bytes_min += len(value) # assume one byte per character
                elif "Weight" in value:
                    bytes_min += 1
                else:
                    raise ValueError("key: " + key + "\tvalue: " + value)
            self.bytesAll_min += bytes_min
            self.bytesEntity_min += bytes_min

        # print statistics
        print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(len(self.changedChunksAll),
                                                                                                  len(self.changedChunksBlock),
                                                                                                  len(self.changedChunksBlockEntity),
                                                                                                  len(self.changedChunksEntity),
                                                                                                  len(self.changedSectionsAll),
                                                                                                  len(self.changedSectionsBlock),
                                                                                                  len(self.changedSectionsBlockEntity),
                                                                                                  len(self.changedSectionsEntity),
                                                                                                  len(self.changedBlocks.keys()),
                                                                                                  len(self.changedBlockEntities.keys()),
                                                                                                  len(self.changedEntities.keys()),
                                                                                                  self.bytesAll_min,
                                                                                                  self.bytesBlock_min,
                                                                                                  self.bytesBlockEntity_min,
                                                                                                  self.bytesEntity_min,
                                                                                                  self.bytesAll_mid,
                                                                                                  self.bytesBlock_mid,
                                                                                                  self.bytesBlockEntity_mid,
                                                                                                  self.bytesEntity_mid,
                                                                                                  self.bytesAll_max,
                                                                                                  self.bytesBlock_max,
                                                                                                  self.bytesBlockEntity_max,
                                                                                                  self.bytesEntity_max))

        self.intervalStatistics.append([len(self.changedChunksAll),
                                        len(self.changedChunksBlock),
                                        len(self.changedChunksBlockEntity),
                                        len(self.changedChunksEntity),
                                        len(self.changedSectionsAll),
                                        len(self.changedSectionsBlock),
                                        len(self.changedSectionsBlockEntity),
                                        len(self.changedSectionsEntity),
                                        len(self.changedBlocks.keys()),
                                        len(self.changedBlockEntities.keys()),
                                        len(self.changedEntities.keys()),
                                        self.bytesAll_min,
                                        self.bytesBlock_min,
                                        self.bytesBlockEntity_min,
                                        self.bytesEntity_min,
                                        self.bytesAll_mid,
                                        self.bytesBlock_mid,
                                        self.bytesBlockEntity_mid,
                                        self.bytesEntity_mid,
                                        self.bytesAll_max,
                                        self.bytesBlock_max,
                                        self.bytesBlockEntity_max,
                                        self.bytesEntity_max
                                        ])


    def noMoreIntervals(self):
        # plot results
        changeTypeStatisticPlot = ChangeTypeStatisticPlot()
        changeTypeStatisticPlot.plot(self.intervalStatistics, self.intervalLength)

        changeTypePlot = ChangeTypePlot()
        changeTypePlot.plot(self.intervalStatistics, self.intervalLength)