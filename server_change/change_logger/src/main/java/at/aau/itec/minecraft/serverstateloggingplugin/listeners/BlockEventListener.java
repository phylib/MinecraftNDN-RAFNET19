package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.Location;
import org.bukkit.block.Block;
import org.bukkit.block.BlockState;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;

import java.util.List;
import java.util.logging.Logger;

public class BlockEventListener implements Listener {
    private Logger logger;
    private HashSet<Block> dirtyBlocks;
    private HashSet<Chunk> dirtyChunks;

    public BlockEventListener(Logger log, HashSet<Block> dirtyBlocks ,HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
        //logger.info("Logging Block events");
    }

    private void process(BlockEvent event){
        process(event, "");
    }

    private void process(BlockEvent event, String additionalText){
        process(event, additionalText, Arrays.asList(event.getBlock()));
    }

    private void process(BlockEvent event, String additionalText, List<Block> involvedBlocks){
       /* Block b = event.getBlock();
        Chunk ch = b.getChunk();
        Location l = b.getLocation();
        String blockCoords = "block (" + l.getBlockX() + ","+ l.getBlockY() + ","+ l.getBlockZ() + ")";
        logger.info(b.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" + blockCoords +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t" + additionalText);
        */
        for(Block bl : involvedBlocks){
            //dirtyBlocks.add(bl);
            dirtyChunks.add(bl.getChunk());
        }
    }

    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.block.*
    @EventHandler(priority = EventPriority.MONITOR) // used by EB  Called when a block is broken by a player.
    public void onBlockBreak(BlockBreakEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block is destroyed as a result of being burnt by fire.
    public void onBlockBurn(BlockBurnEvent event){ if(!event.isCancelled()) process(event); }

    // Commented out because there is no change to game state!
    //@EventHandler(priority = EventPriority.MONITOR) // Called when we try to place a block, to see if we can build it here or not.
    //public void onBlockCanBuild(BlockCanBuildEvent event){ process(event); }

    // TODO: I'm on the fence about including this one
    @EventHandler(priority = EventPriority.MONITOR) // Called when a block is damaged by a player.
    public void onBlockDamage(BlockDamageEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an item is dispensed from a block.
    public void onBlockDispense(BlockDispenseEvent event){ if(!event.isCancelled())  process(event, "dispensed item "
    + event.getItem()); }

    // Commented out because there is no change to game state!
    //@EventHandler(priority = EventPriority.MONITOR) // An event that's called when a block yields experience. (super of BlockBreak/FurnaceExtract)
    //public void onBlockExp(BlockExpEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block explodes.
    public void onBlockExplode(BlockExplodeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a blocks fades, melts or disappears based on world conditions. (Snow/Ice melt, Fire burning out)
    public void onBlockFade(BlockFadeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block is formed or spreads based on world conditions (Snow/Ice form, Obsidian/Cobblestone, Concrete) superclass
    public void onBlockForm(BlockFormEvent event){ if(!event.isCancelled()) process(event);}

    @EventHandler(priority = EventPriority.MONITOR) // Represents events with a source block and a destination block (lava and water, teleport dragon eggs
    public void onBlockFromTo(BlockFromToEvent event){
        Location l = event.getToBlock().getLocation();
        String toBlockCoords = " to block (" + l.getBlockX() + ","+ l.getBlockY() + ","+ l.getBlockZ() + ")";
        if(!event.isCancelled()) process(event, toBlockCoords, Arrays.asList(event.getBlock(), event.getToBlock()));
    }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block grows naturally in the world (Wheat, Sugar Cane, Cactus, Watermelon, Pumpkin)
    public void onBlockGrow(BlockGrowEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block is ignited.
    public void onBlockIgnite(BlockIgniteEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Fired when a single block placement action of a player triggers the creation of multiple blocks (e.g. placing bed block)
    public void onBlockMultiPlace(BlockMultiPlaceEvent event){
        if(!event.isCancelled()){
            HashSet<Block> blocks = new HashSet<>();
            blocks.add(event.getBlock());
            for(BlockState bs : event.getReplacedBlockStates()){
                blocks.add(bs.getBlock());
            }

            process(event, "", new ArrayList<Block>(blocks));
        }
    }

    // commented out because no change! / spammy
    //@EventHandler(priority = EventPriority.MONITOR) // Thrown when a block physics check is called.
    // public void onBlockPhysics(BlockPhysicsEvent event){ if(!event.isCancelled()) process(event); }

    //@EventHandler(priority = EventPriority.MONITOR)  // commented out because it has no "getHandlers()" method -> problems registering
    //public void onBlockPiston(BlockPistonEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a piston extends.
    public void onBlockPistonExtend(BlockPistonExtendEvent event){
        if(!event.isCancelled()) {
            ArrayList<Block> blocks = new ArrayList<>(event.getBlocks());
            if(!blocks.contains(event.getBlock())) blocks.add(event.getBlock());
            process(event,"", blocks);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a piston retracts.
    public void onBlockPistonRetract(BlockPistonRetractEvent event){
        if(!event.isCancelled()) {
            ArrayList<Block> blocks = new ArrayList<>(event.getBlocks());
            if(!blocks.contains(event.getBlock())) blocks.add(event.getBlock());
            process(event,"", blocks);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR)  // used by EB // Called when a block is placed by a player;
    public void onBlockPlace(BlockPlaceEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a redstone current changes.
    public void onBlockRedstone(BlockRedstoneEvent event){ process(event, "redstone current changed from " + event.getOldCurrent() + " to " + event.getNewCurrent()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block spreads based on world conditions. (Mushrooms, Fire)
    public void onBlockSpread(BlockSpreadEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // nomen est omen?
    public void onCauldronLevelChange(CauldronLevelChangeEvent event){ if(!event.isCancelled()) process(event, "cauldron level changed from " + event.getOldLevel() + " to " + event.getNewLevel()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block is formed by entities. (Show formed by snowman, Frosted Ice formed by Frost Walker enchantment)
    public void onEntityBlockFormEvent(EntityBlockFormEvent event){ if(!event.isCancelled()) process(event, " entity is " + event.getEntity()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when leaves are decaying naturally
    public void onLeavesDecay(LeavesDecayEvent event){ if(!event.isCancelled()) process(event); }

    // no change to game state
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a note block is playing through player interaction or a redstone current.
    //public void onNotePlay(NotePlayEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a sign is changed by a player
    public void onSignChange(SignChangeEvent event){if(!event.isCancelled())  process(event); }

}
