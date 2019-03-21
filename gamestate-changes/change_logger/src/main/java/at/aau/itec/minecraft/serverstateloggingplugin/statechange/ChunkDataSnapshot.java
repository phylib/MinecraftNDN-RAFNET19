package at.aau.itec.minecraft.serverstateloggingplugin.statechange;

import org.bukkit.ChunkSnapshot;
import org.bukkit.Material;
import org.bukkit.block.BlockState;

import java.util.Objects;
import java.util.logging.Logger;

public class ChunkDataSnapshot {
    private static final int SEC_COUNT = 16;

    private Integer hashcode;
    private Integer[] sectionHashCodes;
    private ChunkSnapshot chunkSnapshot;
    private boolean hashCodesCalculated = false;
    String key;
    String coordinates;
    private Logger logger;

    /*public ChunkDataSnapshot(ChunkSnapshot snapshot, boolean calculateHashCodesNow){
        this(snapshot, calculateHashCodesNow, null);
    }*/

    public ChunkDataSnapshot(ChunkSnapshot snapshot, boolean calculateHashCodesNow, Logger logger){
        this.logger = logger;
        this.chunkSnapshot = snapshot;
        key = snapshot.getWorldName() + "/("+snapshot.getX()+","+snapshot.getZ()+")";
        coordinates = snapshot.getX() + "," + snapshot.getZ();

        if(calculateHashCodesNow) {
            calculateHashCodes();
        }
    }

    // allows to calculate hashcodes at a later time
    public void calculateHashCodes(){
        if(!hashCodesCalculated){

            // calculate section hash codes
            this.sectionHashCodes = getSectionHashCodes(this.chunkSnapshot);

            // get chunk hash code as has of the section hash codes
            hashcode = Objects.hash((Object[])sectionHashCodes);
            hashCodesCalculated = true;
        }
    }

    // calculate hashcodes for individual chunk sections
    // blockEmittedLight is important as it spreads light changes in 3D space
    // Skylight seems to encompass light from "straight down" -> change can propagate downward (as general direction)
    private Integer[] getSectionHashCodes(ChunkSnapshot chks){
        Integer[] hashCodes = new Integer[SEC_COUNT];
        Integer[] values = new Integer[16*16*16*4]; // 16*16*16 blocks a 4 values (material, skyLight, emittedLight, data)
        for(int section = 0; section < SEC_COUNT; section++){
            if(chks.isSectionEmpty(section)){
                hashCodes[section] = 0;
            }else{
                int cnt=0, ybase = section << 4;
                for(int y = ybase; y < ybase + 16; y++){
                    for(int x = 0; x < 16; x++){
                        for(int z = 0; z < 16; z++){
                            values[cnt++] = chks.getBlockType(x,y,z).ordinal();
                            values[cnt++] = chks.getBlockSkyLight(x,y,z);
                            values[cnt++] = chks.getBlockEmittedLight(x,y,z);
                            values[cnt++] = chks.getBlockData(x,y,z); // TODO: deprecated!!
                        }
                    }
                }
                hashCodes[section] = Objects.hash((Object[])values);
            }
        }
        return hashCodes;
    }

    // TODO: comparison / diff method? (full, and assisted by list of dirtyBlocks)

    @Override
    public boolean equals(Object other){
        if(other == null) return false;
        if(this == other) return true;
        if(!(other instanceof ChunkDataSnapshot)) return false;
        ChunkDataSnapshot otherSnapshot = (ChunkDataSnapshot)other;

        return (this.hashcode.equals(otherSnapshot.hashcode));
    }

    // public accessors (all necessary?)
    public Integer getHashcode(){
        if(!areHashCodesCalculated()){calculateHashCodes();} // lazy eval
        return this.hashcode;
    }
    public Integer[] getSectionHashcodes(){return this.sectionHashCodes;}
    public boolean areHashCodesCalculated(){return hashCodesCalculated;}
    public ChunkSnapshot getChunkSnapshot(){return this.chunkSnapshot;}
    public String getKey(){return this.key;}
    public String getChunkCoordinates(){return this.coordinates;}
    public String getKeyPlusTime(){return this.key + " @ " + this.chunkSnapshot.getCaptureFullTime();}

    // calculate difference between chunkDataSnapshots
    public String diff(ChunkDataSnapshot other){
        //StringBuilder tmp = new StringBuilder("Comparing: " + this.getKeyPlusTime() + " with " + other.getKeyPlusTime() + "\n");
        //long startTime = System.nanoTime();

        // ensure both hashcodes are calculated (if not already done, do it now!)
        if(!this.areHashCodesCalculated()) this.calculateHashCodes();
        if(!other.areHashCodesCalculated()) other.calculateHashCodes();

        if(!this.getHashcode().equals(other.getHashcode())){ // mismatch of chunk hashcode

            // check sections for hashcode mismatch
            for(int ylevel=0; ylevel < this.sectionHashCodes.length; ylevel++){
                if(!this.sectionHashCodes[ylevel].equals(other.sectionHashCodes[ylevel])){
                    //tmp.append("\tsection ").append(ylevel).append(" changed: \n");
                    // change to one block may cause changes to blockSkyLight of multiple blocks (beneath it [as general direction])
                    // change to one block may cause changes to blockEmittedLight in multple blocks around it (3D)
                    // block(s) in this section have changed -> maybe there are changes in blockSkyLight/blockEmittedLight too (Do those have to be communicated too?)
                    Material m1, m2;
                    BlockChange blockChange;
                    int sl1, sl2, el1, el2, bd1, bd2;
                    int ybase = ylevel << 4;
                    for(int y = ybase; y < ybase + 16; y++){
                        for(int x = 0; x < 16; x++){
                            for(int z = 0; z < 16; z++){
                                blockChange = null;
                                // block material
                                m1 = this.chunkSnapshot.getBlockType(x,y,z);
                                m2 = other.chunkSnapshot.getBlockType(x,y,z);
                                if(!m1.equals(m2)){
                                    if(blockChange == null) blockChange = new BlockChange(other.getChunkSnapshot().getCaptureFullTime(),"BLOCK",x,y,z, other.getChunkCoordinates(), other.getChunkSnapshot().getWorldName());
                                    blockChange.setMaterial(m2.toString());
                                    //tmp.append("\t\tblock (" + x + "," + y + "," + z + ") material changed from " + m1.toString() + " to " + m2.toString() + "\n");
                                }

                                // blockSkyLight
                                sl1 = this.chunkSnapshot.getBlockSkyLight(x,y,z);
                                sl2 = other.chunkSnapshot.getBlockSkyLight(x,y,z);
                                if(sl1 != sl2){
                                    if(blockChange == null) blockChange = new BlockChange(other.getChunkSnapshot().getCaptureFullTime(),"BLOCK",x,y,z, other.getChunkCoordinates(), other.getChunkSnapshot().getWorldName());
                                    blockChange.setSkylight(String.valueOf(sl2));
                                    //tmp.append("\t\tblock (" + x + "," + y + "," + z + ") skylight changed from " + sl1 + " to " + sl2 + "\n");
                                }

                                // blockEmittedLight
                                el1 = this.chunkSnapshot.getBlockEmittedLight(x,y,z);
                                el2 = other.chunkSnapshot.getBlockEmittedLight(x,y,z);
                                if(el1 != el2){
                                    if(blockChange == null) blockChange = new BlockChange(other.getChunkSnapshot().getCaptureFullTime(),"BLOCK",x,y,z, other.getChunkCoordinates(), other.getChunkSnapshot().getWorldName());
                                    blockChange.setEmittedLight(String.valueOf(el2));
                                    //tmp.append("\t\tblock (" + x + "," + y + "," + z + ") emitted light changed from " + el1 + " to " + el2 + "\n");
                                }

                                // blockData (legacy)
                                bd1 = this.chunkSnapshot.getBlockData(x,y,z);
                                bd2 = other.chunkSnapshot.getBlockData(x,y,z);
                                if(bd1 != bd2){
                                    if(blockChange == null) blockChange = new BlockChange(other.getChunkSnapshot().getCaptureFullTime(),"BLOCK",x,y,z, other.getChunkCoordinates(), other.getChunkSnapshot().getWorldName());
                                    blockChange.setBlockData(String.valueOf(bd2));
                                    //tmp.append("\t\tblock (" + x + "," + y + "," + z + ") data changed from " + bd1 + " to " + bd2 + "\n");
                                }

                                if(blockChange!=null) logger.info(blockChange.toString());

                            }
                        }
                    }
                }
            }
        }

        //tmp.append("\tFinished comparison, elapsed time = " + (System.nanoTime() - startTime)/1000000.0 + "ms\n");
        //return tmp.toString();
        return "";
    }
}

/*
    Handled Properties of ChunkSnapshot (bukkit-1.12.2-R0.1-SNAPSHOT:
    // Handled by "key"
    // Gets the X-coordinate of this chunk
        int getX();
    // Gets the Z-coordinate of this chunk
        int getZ();
    // Gets name of the world containing this chunk
        String getWorldName();

    // Handled by incorporation into "getSectionHashCodes(...)" and "diff(...)"
    //Get block type for block at corresponding coordinate in the chunk
        Material getBlockType(int x, int y, int z);
    // Get sky light level for block at corresponding coordinate in the chunk
        int getBlockSkyLight(int x, int y, int z);
    // Get light level emitted by block at corresponding coordinate in the chunk
        int getBlockEmittedLight(int x, int y, int z);
    // Get block data for block at corresponding coordinate in the chunk
        @Deprecated
        int getBlockData(int x, int y, int z);

    // For informational purposes, part of output of diff(...), part of getKeyPlusTime(...)
    // Get world full time when chunk snapshot was captured (time in ticks)
        long getCaptureFullTime();
###############################################################################
    Properties of CunkSnapshot that are NOT handled:

    // Not handled due to deprication
    // Get block type for block at corresponding coordinate in the chunk
        @Deprecated
        int getBlockTypeId(int x, int y, int z);

    // Not handled because this seems to be a calculated property // TODO is getHighestBlocYAt() really calculated?
    // Gets the highest non-air coordinate at the given coordinates
        int getHighestBlockYAt(int x, int z);
    // Test if section is empty
        boolean isSectionEmpty(int sy);

    // Not handled because it cannot change
    // Biomes do not change, they are generated by/using the world seed and current (MC-version) generation rules.
    // Currently, there is no apparent/(parctical) way to change biomes (just batch-change materials of blocks as "hack")
    // https://gaming.stackexchange.com/questions/267281/is-there-a-minecraft-command-for-changing-biomes
    // Get biome at given coordinates
        Biome getBiome(int x, int z);
    // Get raw biome temperature (0.0-1.0) at given coordinate
        double getRawBiomeTemperature(int x, int z);
    // Get raw biome rainfall (0.0-1.0) at given coordinate
        @Deprecated
        double getRawBiomeRainfall(int x, int z);
*/