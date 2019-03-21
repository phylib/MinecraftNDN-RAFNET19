package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.block.Block;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.world.*;

import java.util.HashSet;
import java.util.logging.Logger;

public class WorldEventListener implements Listener {
    Logger logger;
    HashSet<Block> dirtyBlocks;
    HashSet<Chunk> dirtyChunks;

    public WorldEventListener(Logger log, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
    }

    private void process(Event event, Chunk ch){
        dirtyChunks.add(ch);
        /*logger.info(ch.getWorld().getFullTime() + "\t" + event.getEventName() + "\t"  +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\tworld: " + ch.getWorld().getName());
        */
    }

    private void process(WorldEvent event){
        //logger.info(event.getWorld().getFullTime() + ":\t" + event.getEventName() + "\tworld: " + event.getWorld().getName());
    }


    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.world.*

    // superclass of ChunkLoadEvent, ChunkPopulateEvent, and ChunkUnloadEvent
    //@EventHandler(priority = EventPriority.MONITOR) // Represents a Chunk related event
    //public void onChunk(ChunkEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a chunk is loaded
    public void onChunkLoad(ChunkLoadEvent event){ process(event, event.getChunk()); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a new chunk has finished being populated.
    public void onChunkPopulate(ChunkPopulateEvent event){ process(event, event.getChunk()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a chunk is unloaded
    public void onChunkUnload(ChunkUnloadEvent event){ if(!event.isCancelled()) process(event, event.getChunk()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a portal is created
    public void onPortalCreate(PortalCreateEvent event){ if(!event.isCancelled()) process(event, event.getBlocks().get(0).getChunk()); }

    @EventHandler(priority = EventPriority.MONITOR) // An event that is called when a world's spawn changes. The world's previous spawn location is included.
    public void onSpawnChange(SpawnChangeEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Event that is called when an organic structure attempts to grow (Sapling -> Tree), (Mushroom -> Huge Mushroom), naturally or using bonemeal.
    public void onStructureGrow(StructureGrowEvent event){ if(!event.isCancelled()) process(event, event.getLocation().getChunk()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a World is initializing
    public void onWorldInit(WorldInitEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a World is loaded
    public void onWorldLoad(WorldLoadEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a World is saved.
    public void onWorldSave(WorldSaveEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a World is unloaded
    public void onWorldUnload(WorldUnloadEvent event){ if(!event.isCancelled()) process(event); }

}
