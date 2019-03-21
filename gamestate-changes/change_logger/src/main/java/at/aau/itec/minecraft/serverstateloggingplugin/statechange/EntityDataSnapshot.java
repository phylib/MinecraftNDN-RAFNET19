package at.aau.itec.minecraft.serverstateloggingplugin.statechange;

// TODO: notice the use of non-bukkit imports -> may require changes if changing the server-type (craftbukkit, spigot, glowstone)
import org.bukkit.Location;
import org.bukkit.block.BlockState;
import net.minecraft.server.v1_12_R1.NBTTagCompound;
import net.minecraft.server.v1_12_R1.TileEntity;
import org.bukkit.Chunk;
import org.bukkit.craftbukkit.v1_12_R1.CraftWorld;
import org.bukkit.craftbukkit.v1_12_R1.entity.CraftEntity;
import org.bukkit.entity.Entity;
import org.bukkit.entity.EntityType;

import java.util.*;
import java.util.logging.Logger;

public class EntityDataSnapshot {
    UUID uniqueId;
    String entityType;
    String chunkKey;
    String chunkCoordinates;
    NBTTagCompound nbtTag;
    long worldFullTime;
    String worldName;
    private Logger logger;
    Location location;


    public EntityDataSnapshot(Entity entity){
        this(entity, new LinkedList<>(), null);
    }

    public EntityDataSnapshot(Entity entity, List<String> keysToRemove, Logger logger){
        this.logger = logger;
        location = entity.getLocation();
        entityType = entity.getType().toString();
        if(entity.getType() == EntityType.DROPPED_ITEM){
            entityType += "/" + entity.getName();
        }
        uniqueId = entity.getUniqueId();
        worldFullTime = entity.getWorld().getFullTime();
        worldName = entity.getWorld().getName();
        Chunk chunk = entity.getLocation().getChunk();
        chunkKey = entity.getWorld().getName() + "/("+chunk.getX()+","+chunk.getZ()+")";
        chunkCoordinates = chunk.getX() + "," + chunk.getZ();
        net.minecraft.server.v1_12_R1.Entity e = ((CraftEntity) entity).getHandle();

        nbtTag = new NBTTagCompound();
        e.save(nbtTag);

        for(String key : keysToRemove){
            nbtTag.remove(key); // Top level keys should work
        }
    }

    public EntityDataSnapshot(BlockState blockState, Chunk chunk, List<String> keysToRemove, Logger logger){
        this.logger = logger;
        location = blockState.getLocation();
        entityType = "TILE_ENTITY/" + blockState.getData().getItemType().toString();
        // most significant bits as most significant bits of world-UID and least significant bits as hash value of the x,y,z coordinates (distinct tile entites at same locations in different worlds)
        uniqueId = new UUID(chunk.getWorld().getUID().getMostSignificantBits(),Objects.hash((Object[])new Integer[]{blockState.getX(), blockState.getY(), blockState.getZ()}));
        worldFullTime = chunk.getWorld().getFullTime();
        worldName = chunk.getWorld().getName();
        chunkKey = chunk.getWorld().getName() + "/("+chunk.getX()+","+chunk.getZ()+")";
        chunkCoordinates = chunk.getX() + "," + chunk.getZ();

        TileEntity te = ((CraftWorld)blockState.getWorld()).getTileEntityAt(blockState.getX(),blockState.getY(),blockState.getZ());
        nbtTag = new NBTTagCompound();
        te.save(nbtTag);

        for(String key : keysToRemove){
            nbtTag.remove(key); // Top level keys should work
        }
    }


    public UUID getUniqueId(){return uniqueId;}
    public String getUniqueIdPlusTime(){return this.uniqueId + " @ " + this.worldFullTime;}
    public String getNbtTagString(){return this.nbtTag.toString();}
    public String getChunkCoordinates(){return this.chunkCoordinates;}
    public String getWorldName(){return worldName;}

    public String diff(EntityDataSnapshot other, List<String> keysToIgnore){

        if(this.nbtTag.equals(other.nbtTag)) return "";
        else{
            LinkedList<String> diff = NbtDiffIterInventorySlotAndRecipeMod.diff(this.nbtTag, other.nbtTag, keysToIgnore);

            // sanity check, diff says no change but nbtTags are not equal -> diff has overlooked something!
            if(diff.isEmpty()){
                throw new RuntimeException("Change not detected: \n" + this.getNbtTagString() + "\n" + other.getNbtTagString() + "\n");
            }
            // location.getBlockX() vs location.getX():   getBlockX() is floored version of location.getX()!!   ">>" -> get chunk , "& 15" get pos in chunk (alt for %16)
            //      leave Y coordinate "as is", because of the further processing in "EntityChange" (e.g. calculation of section from ypos), BlockY() can only be in valid range (0-255)
            logger.info(new EntityChange(other.worldFullTime, entityType, location.getBlockX() & 15, location.getBlockY(), location.getBlockZ() & 15, other.getChunkCoordinates(), other.getWorldName(), other.getUniqueId(), diff).toString());
            return diff.toString();
        }
    }

    public void logWithMessage(long worldFullTime, String message){
        // leave Y coordinate "as is", because of the further processing in "EntityChange" (e.g. calculation of section from ypos), BlockY() can only be in valid range (0-255)
        logger.info(new EntityChange(worldFullTime, entityType, location.getBlockX() & 15, location.getBlockY(), location.getBlockZ() & 15, this.getChunkCoordinates(), this.getWorldName(), this.getUniqueId(), new LinkedList<>(Arrays.asList(message))).toString());
    }
}
