package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.Location;
import org.bukkit.block.Block;
import org.bukkit.entity.Entity;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.BlockEvent;
import org.bukkit.event.hanging.*;

import java.util.HashSet;
import java.util.List;
import java.util.logging.Logger;

public class HangingEventListener implements Listener {
    private Logger logger;
    private HashSet<Block> dirtyBlocks;
    private HashSet<Chunk> dirtyChunks;
    private HashSet<Entity> dirtyEntities;

    public HangingEventListener(Logger log,  HashSet<Entity> dirtyEntities, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
        this.dirtyEntities = dirtyEntities;
    }

    private void process(HangingEvent event, Entity entity){
        Block b = event.getEntity().getLocation().getBlock();
        Chunk ch = b.getChunk();
        /*Location l = b.getLocation();
        String blockCoords = "block (" + l.getBlockX() + ","+ l.getBlockY() + ","+ l.getBlockZ() + ")";
        logger.info(b.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" + blockCoords +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t");

        dirtyEntities.add(entity);
        */
        dirtyChunks.add(ch);
    }

    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.hanging.*
    @EventHandler(priority = EventPriority.MONITOR) // Triggered when a hanging entity is removed by an entity
    public void onHangingBreakByEntity(HangingBreakByEntityEvent event){ if(!event.isCancelled()) process(event, event.getEntity()); }

    @EventHandler(priority = EventPriority.MONITOR) // Triggered when a hanging entity is removed
    public void onHangingBreak(HangingBreakEvent event){  if(!event.isCancelled()) process(event, event.getEntity()); }

    @EventHandler(priority = EventPriority.MONITOR) // Triggered when a hanging entity is created in the world
    public void onHangingPlace(HangingPlaceEvent event){ if(!event.isCancelled()) process(event, event.getEntity()); }
}
