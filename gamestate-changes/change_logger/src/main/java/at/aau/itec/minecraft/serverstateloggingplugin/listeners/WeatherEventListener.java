package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.block.Block;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.weather.*;

import java.util.HashSet;
import java.util.logging.Logger;

public class WeatherEventListener implements Listener {
    Logger logger;
    HashSet<Block> dirtyBlocks;
    HashSet<Chunk> dirtyChunks;

    public WeatherEventListener(Logger log, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
    }

    private void process(Event event, Chunk ch){
        dirtyChunks.add(ch);
        /*logger.info(ch.getWorld().getFullTime() + "\t" + event.getEventName() + "\t"  +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t");
         */
    }


    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.weather.*

    @EventHandler(priority = EventPriority.MONITOR) // Stores data for lightning striking
    public void onLightningStrike(LightningStrikeEvent event){ if(!event.isCancelled()) process(event, event.getLightning().getLocation().getChunk()); }


    @EventHandler(priority = EventPriority.MONITOR) // Stores data for thunder state changing in a world
    public void onThunderChange(ThunderChangeEvent event){}


    @EventHandler(priority = EventPriority.MONITOR) // Stores data for weather changing in a world
    public void onWeatherChange(WeatherChangeEvent event){}
}
