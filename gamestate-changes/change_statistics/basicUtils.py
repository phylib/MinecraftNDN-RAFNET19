from datetime import datetime
from enum import Enum
ChangeType = Enum('ChangeType', 'block tile_entity entity status')

def getType(value):
    if value == 'status':
        return ChangeType.status
    elif value == 'BLOCK':
        return ChangeType.block
    elif value.startswith('TILE_ENTITY'):
        return ChangeType.tile_entity
    else:
        return ChangeType.entity

def to_date(str):
    return datetime.strptime(str, '%d-%m-%Y_%H:%M:%S:%f')

# data structure for storing change information
# takes lines/rows as lists of string values and saves them (some values converted to more useful data types) in order
class IntervalData:
    def __init__(self):
        self.entries = [] # all change entries can be found in this list
        self.status_entries = [] # additional list only storing the status information entries

    def addLogRowItems(self, rowItems):
        logTime = to_date(rowItems[0])      # wall clock time of log entry creation
        worldFullTime = int(rowItems[1])    # MC server full time (ticks since startup)
        type = getType(rowItems[2])         # Category/Type of change (ChangeType.(status|block|tile_entity|entity)

        # store basic information (common to entries of all types)
        entry = {'logTime': logTime, 'worldFullTime': worldFullTime, 'type': type, 'typeStr': rowItems[2]}

        if type == ChangeType.status: # information specific to status entries
            # 20-10-2018_19:34:40:724	time	type="status"	#loadedChunks	#changedChunks	#tileEntities	#changedTileEntities	#entities	#changedEntities	#onlinePlayers	totalStateDiffTime
            loadedChunks = int(rowItems[3])         # total number of loaded chunks
            changedChunks = int(rowItems[4])        # number of chunks that changed (indicated by Events)
            tileEntities = int(rowItems[5])         # total number of tile/block-entities
            changedTileEntities = int(rowItems[6])  # number of tile entities that changed
            entities = int(rowItems[7])             # total number of entities
            changedEntities = int(rowItems[8])      # number of entities that changed
            onlinePlayers = int(rowItems[9])        # total number of players logged in to the server
            totalStateDiffTime = float(rowItems[10].replace('ms',''))   # time it took the measurement plugin to compare the current with the last state (comparing "dirty" chunks as indicated by Events)
            # update dictionary with type-specific information
            entry.update({"loadedChunks": loadedChunks, 'changedChunks': changedChunks, 'tileEntities': tileEntities, 'changedTileEntities': changedTileEntities, 'entities': entities
                          , 'changedEntities': changedEntities, 'onlinePlayers': onlinePlayers, 'totalStateDiffTime': totalStateDiffTime})
            # store change entry (in all lists)
            self.entries.append(entry)
            self.status_entries.append(entry)
        else:
            # change must be involving a block, tile/block-entity or entity, which all share the following properties
            xpos = rowItems[3]                      # global coordinate system (block x coordinate)
            ypos = rowItems[4]                      # global coordinate system (block y coordinate)
            zpos = rowItems[5]                      # global coordinate system (block z coordinate)
            world = rowItems[6]                     # name of the world (e.g. "world", "world_nether", "world_the_end"
            chunk = rowItems[7]                     # x,z coordinates of the chunk that the change happened in
            section = rowItems[8]                   # section number (0-15) of the section that the change happened in (inside the chunk)
            # add properties common to block and (tile) entity
            entry.update({'xpos': xpos, 'ypos': ypos, 'zpos': zpos, 'world': world, 'chunk': chunk, 'section': section})

            if type == ChangeType.entity or type == ChangeType.tile_entity:
                # change involves tile/block-entity or entity
                # 20-10-2018_19:34:40:724	time	type="entity"	xpos	ypos	zpos	world	chunk	section	uuid	[changed attributes]
                uuid = rowItems[9]                  # all entities and tileEntities have an identifier (uuid)
                changes = rowItems[10]              # the NBT diff of the previous and current state of the (tile) entity
                # update dict with (tile-)entity specific infos
                entry.update({'uuid': uuid, 'changes': changes})
                # store change entry
                self.entries.append(entry)
            elif type == ChangeType.block:
                # change involves a block
                # 20-10-2018_19:34:40:724	time	type="block"	xpos	ypos	zpos	world	chunk	section	material	skylight	emittedLight	BlockData
                material = rowItems[9]              # the material a block consists of
                skylight = rowItems[10]             # the transparency regarding light from above (sun/moon)
                emittedLight = rowItems[11]         # light emitted/reflected by/from the block itself
                blockData = rowItems[12]            # additional data (<= one byte)
                # update dictionary with block specific information
                entry.update({'material' : material, 'skylight': skylight, 'emittedLight': emittedLight, 'blockData': blockData})
                # store change entry
                self.entries.append(entry)
            else:
                raise ValueError("type '" + type  + "' is not handled!")  # handle type that is not handled otherwise


    def clearEntries(self):
        del(self.entries)
        self.entries=[]


    def getNumStatusEntries(self):
        return len(self.status_entries)


    def append(self, other):
        if type(other) != type(self):
            raise ValueError("Object types do not match up!")
        self.entries += other.entries
        self.status_entries += other.status_entries