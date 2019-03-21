package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.Location;
import org.bukkit.block.Block;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.enchantment.*;

import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.logging.Logger;

public class EnchantmentEventListener implements Listener {
    private Logger logger;
    private HashSet<Block> dirtyBlocks;
    private HashSet<Chunk> dirtyChunks;

    public EnchantmentEventListener(Logger log, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
    }

    private void process(Event event, List<Block> involvedBlocks){

        /*Block b = involvedBlocks.get(0);
        Chunk ch = b.getChunk();
        Location l = b.getLocation();
        String blockCoords = "block (" + l.getBlockX() + ","+ l.getBlockY() + ","+ l.getBlockZ() + ")";
        logger.info(b.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" + blockCoords +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t");
        */
        for(Block bl : involvedBlocks){
            //dirtyBlocks.add(bl);
            dirtyChunks.add(bl.getChunk());
        }
    }

    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.enchantment.*
    @EventHandler(priority = EventPriority.MONITOR) // Called when an ItemStack is successfully enchanted (currently at enchantment table)
    public void onEnchantItem(EnchantItemEvent event){ if(!event.isCancelled()) process(event, Arrays.asList(event.getEnchantBlock()));}

    @EventHandler(priority = EventPriority.MONITOR) // Called when an ItemStack is inserted in an enchantment table - can be called multiple times
    public void onPrepareItemEnchant(PrepareItemEnchantEvent event){ if(!event.isCancelled()) process(event, Arrays.asList(event.getEnchantBlock()));}
}
