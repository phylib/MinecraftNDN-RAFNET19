package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.block.Block;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.server.*;

import java.util.HashSet;
import java.util.logging.Logger;

public class ServerEventListener implements Listener {
    Logger logger;
    HashSet<Block> dirtyBlocks;
    HashSet<Chunk> dirtyChunks;

    public ServerEventListener(Logger log, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
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

    private void process(ServerEvent event){
        logger.info(event.getEventName());
    }


    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.server.*

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Event triggered for server broadcast messages such as from Server.broadcast(String, String).
    //public void onBroadcastMessage(BroadcastMessageEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a map is initialized.
    //public void onMapInitialize(MapInitializeEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a plugin is disabled.
    //public void onPluginDisable(PluginDisableEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a plugin is enabled.
    //public void onPluginEnable(PluginEnableEvent event){}

    // unnecessary + superclass
    //@EventHandler(priority = EventPriority.MONITOR) // Used for plugin enable and disable events
    //public void onPlugin(PluginEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called when a command is received over RCON. See the javadocs of ServerCommandEvent for more information.
    //public void onRemoteServerCommand(RemoteServerCommandEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called when a command is run by a non-player. I
    //public void onServerCommand(ServerCommandEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a server list ping is coming in. Displayed players can be checked and removed by iterating over this event.
    //public void onServerListPing(ServerListPingEvent event){}

    // unnecessary + superclass
    //@EventHandler(priority = EventPriority.MONITOR) // An event relating to a registered service. This is called in a ServicesManager
    //public void onService(ServiceEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called when a service is registered.
    //public void onServiceRegister(ServiceRegisterEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called when a service is unregistered.
    //public void onServiceUnregister(ServiceUnregisterEvent event){}

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a CommandSender of any description (ie: player or console) attempts to tab complete.
    //public void onTabComplete(TabCompleteEvent event){}

}
