package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.Location;
import org.bukkit.block.Block;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.*;
import org.bukkit.event.block.BlockEvent;
import org.bukkit.event.inventory.BrewEvent;
import org.bukkit.event.inventory.FurnaceBurnEvent;
import org.bukkit.event.inventory.FurnaceSmeltEvent;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.logging.Logger;

public class InventoryEventListener implements Listener {
    Logger logger;
    HashSet<Block> dirtyBlocks;
    HashSet<Chunk> dirtyChunks;

    public InventoryEventListener(Logger log, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
    }

    // general inventory changes
    private void process(InventoryEvent event){
        Block b = event.getInventory().getLocation().getBlock();
        Chunk ch = b.getChunk();
        dirtyChunks.add(ch);

        /*Location l = b.getLocation();
        String blockCoords = "block (" + l.getBlockX() + ","+ l.getBlockY() + ","+ l.getBlockZ() + ")";
        logger.info(b.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" + blockCoords +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t");
        */
    }

    // changes to block
    private void process(BlockEvent event){
        process(event, "", new ArrayList<>());
    }

    // changes to block
    private void process(BlockEvent event, String additionalText, List<Block> involvedBlocks){
        Block b = event.getBlock();
        if(!involvedBlocks.contains(b)) involvedBlocks.add(b); // ensure block is in involvedBlocks
        process(event, event.getBlock(), additionalText, involvedBlocks);
    }

    private void process(Event event, Block b, String additionalText, List<Block> involvedBlocks){
        /*Chunk ch = b.getChunk();
        Location l = b.getLocation();
        String blockCoords = "block (" + l.getBlockX() + ","+ l.getBlockY() + ","+ l.getBlockZ() + ")";
        logger.info(b.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" + blockCoords +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t" + additionalText);
        */
        if(!involvedBlocks.contains(b)) involvedBlocks.add(b); // ensure block is in involvedBlocks
        for(Block bl : involvedBlocks){
            //dirtyBlocks.add(bl);
            dirtyChunks.add(bl.getChunk());
        }
    }

    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.inventory.*
    // BlockEvent is superclass
    @EventHandler(priority = EventPriority.MONITOR) // Called when the brewing of the contents inside the Brewing Stand is complete.
    public void onBrew(BrewEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an ItemStack is about to increase the fuel level of a brewing stand.
    public void onBrewingStandFuel(BrewingStandFuelEvent event){ if(!event.isCancelled()) process(event); }

    // TODO: what to do with that?
    @EventHandler(priority = EventPriority.MONITOR) // Called when the recipe of an Item is completed inside a crafting matrix.
    public void onCraftItem(CraftItemEvent event){ if(!event.isCancelled()) process(event);}

    @EventHandler(priority = EventPriority.MONITOR)  // BlockEvent is superclass, fuel consumed by furnace
    public void onFurnaceBurn(FurnaceBurnEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an ItemStack is successfully burned as fuel in a furnace.
    public void onFurnaceExtract(FurnaceExtractEvent event){ process(event); }

    // BlockEvent is superclass, material processed by furnace
    @EventHandler(priority = EventPriority.MONITOR) // Called when an ItemStack is successfully smelted in a furnace.
    public void onFurnaceSmelt(FurnaceSmeltEvent event){ if(!event.isCancelled()) process(event); }

    // no change to state
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called when a player clicks a slot in an inventory.
    //public void onInventoryClick(InventoryClickEvent event){ if(!event.isCancelled()) process(event); }

    // no change to state
    //@EventHandler(priority = EventPriority.MONITOR) // Represents a player related inventory event
    //public void onInventoryClose(InventoryCloseEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // This event is called when a player in creative mode puts down or picks up an item in their inventory / hotbar and when they drop items from their Inventory while in creative mode.
    public void onInventoryCreative(InventoryCreativeEvent event){ if(!event.isCancelled()) process(event); }

    // no change to state
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called when the player drags an item in their cursor across the inventory.
    //public void onInventoryDragEvent(InventoryDragEvent event){ if(!event.isCancelled()) process(event); }

    // super of InventoryClickEvent and InventoryDragEvent  // both not directly cause changes to the game state?
    //@EventHandler(priority = EventPriority.MONITOR) // An abstract base class for events that describe an interaction between a HumanEntity and the contents of an Inventory.
    //public void onInventoryInteract(InventoryInteractEvent event){ if(!event.isCancelled()) process(event); }

    // problematic  java.lang.UnsupportedOperationException
    /*@EventHandler(priority = EventPriority.MONITOR) // Called when some entity or block (e.g. hopper) tries to move items directly from one inventory to another.
    public void onInventoryMoveItem(InventoryMoveItemEvent event){
        if(!event.isCancelled()){
            process(event, event.getSource().getLocation().getBlock(), "", Arrays.asList(event.getDestination().getLocation().getBlock()));
        }
    }*/

    // no change to game state
    //@EventHandler(priority = EventPriority.MONITOR) // Represents a player related inventory event
    //public void onInventoryOpen(InventoryOpenEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a hopper or hopper minecart picks up a dropped item.
    public void onInventoryPickupItem(InventoryPickupItemEvent event){ if(!event.isCancelled()) process(event, event.getInventory().getLocation().getBlock(), "", new ArrayList<>()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an item is put in a slot for repair by an anvil.
    public void onPrepareAnvil(PrepareAnvilEvent event){ process(event); }

    // no change to state
    //@EventHandler(priority = EventPriority.MONITOR) // nomen est omen
    //public void onPrepareItemCraft(PrepareItemCraftEvent event){ process(event); }

}
