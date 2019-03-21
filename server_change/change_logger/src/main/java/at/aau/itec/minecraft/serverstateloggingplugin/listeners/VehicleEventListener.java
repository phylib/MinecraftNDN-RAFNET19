package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.block.Block;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.vehicle.*;

import java.util.HashSet;
import java.util.logging.Logger;

public class VehicleEventListener implements Listener {
    Logger logger;
    HashSet<Block> dirtyBlocks;
    HashSet<Chunk> dirtyChunks;

    public VehicleEventListener(Logger log, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
    }

    private void process(VehicleEvent event){
       process(event,"");
    }

    private void process(VehicleEvent event, String additionalString){
        Chunk ch = event.getVehicle().getLocation().getChunk();
        dirtyChunks.add(ch);
        /*logger.info(ch.getWorld().getFullTime() + "\t" + event.getEventName() + "\t"  +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t" + additionalString);
        */
    }

    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.vehicle.*

    @EventHandler(priority = EventPriority.MONITOR) // Raised when a vehicle collides with a block.
    public void onVehicleBlockCollision(VehicleBlockCollisionEvent event){ process(event); }

    // superclass
    //@EventHandler(priority = EventPriority.MONITOR) // Raised when a vehicle collides.
    //public void onVehicleCollision(VehicleCollisionEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Raised when a vehicle is created.
    public void onVehicleCreate(VehicleCreateEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Raised when a vehicle receives damage.
    public void onVehicleDamage(VehicleDamageEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Raised when a vehicle is destroyed, which could be caused by either a player or the environment. This is not raised if the boat is simply 'removed' due to other means.
    public void onVehicleDestroy(VehicleDestroyEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Raised when an entity enters a vehicle.
    public void onVehicleEnter(VehicleEnterEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Raised when a vehicle collides with an entity.
    public void onVehicleEntityCollision(VehicleEntityCollisionEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Raised when a living entity exits a vehicle.
    public void onVehicleExit(VehicleExitEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Raised when a vehicle moves.
    public void onVehicleMove(VehicleMoveEvent event){ process(event); }

    // too many events/second
    //@EventHandler(priority = EventPriority.MONITOR)   // Called when a vehicle updates
    //public void onVehicleUpdate(VehicleUpdateEvent event){ process(event, event.getVehicle().toString()); }
}
