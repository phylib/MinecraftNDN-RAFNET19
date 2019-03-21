package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.Chunk;
import org.bukkit.block.Block;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.*;

import java.util.HashSet;
import java.util.logging.Logger;

public class PlayerEventListener implements Listener {
    Logger logger;
    HashSet<Block> dirtyBlocks;
    HashSet<Chunk> dirtyChunks;

    public PlayerEventListener(Logger log, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
    }

    private void process(PlayerEvent event){
        Chunk ch = event.getPlayer().getLocation().getChunk();
        dirtyChunks.add(ch);

        /*logger.info(ch.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t");
         */
    }


    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.player.*
    // TODO: could be used for trans-server message relaying
    @EventHandler(priority = EventPriority.MONITOR) // Fired when a player sends a chat message to recipients or a plugin compels him to do so.
    public void onAsyncPlayerChat(AsyncPlayerChatEvent event){ if(!event.isCancelled()) process(event); }

    // no change to state
    //@EventHandler(priority = EventPriority.MONITOR) // Stores details for players attempting to log in.
    //public void onAsyncPlayerPreLogin(AsyncPlayerPreLoginEvent event){ process(event); }

    // deprecated
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a player earns an achievement.
    //public void onPlayerAchievementAwarded(PlayerAchievementAwardedEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player has completed all criteria in an advancement.
    public void onPlayerAdvancementDone(PlayerAdvancementDoneEvent event){ process(event); }

    // TODO: necessary?
    @EventHandler(priority = EventPriority.MONITOR) // Represents a player animation event
    public void onPlayerAnimation(PlayerAnimationEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player interacts with an armor stand and will either swap, retrieve or place an item.
    public void onPlayerArmorStandManipulate(PlayerArmorStandManipulateEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // This event is fired when the player is almost about to enter the bed.
    public void onPlayerBedEnter(PlayerBedEnterEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // This event is fired when the player is leaving a bed.
    public void onPlayerBedLeave(PlayerBedLeaveEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player empties a bucket
    public void onPlayerBucketEmpty(PlayerBucketEmptyEvent event){ if(!event.isCancelled()) process(event); }

    // superclass
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a player interacts with a Bucket
    //public void onPlayerBucket(PlayerBucketEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player fills a bucket
    public void onPlayerBucketFill(PlayerBucketFillEvent event){ if(!event.isCancelled()) process(event); }

    // unneccessary?
    @EventHandler(priority = EventPriority.MONITOR)  // Called when a player changes their main hand in the client settings.
    public void onPlayerChangedMainHand(PlayerChangedMainHandEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player switches to another world.
    public void onPlayerChangedWorld(PlayerChangedWorldEvent event){ process(event); }

    // superclass
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called after a player registers or unregisters a new plugin channel.
    //public void onPlayerChannel(PlayerChannelEvent event){ process(event); }

    // synchronized version of AsyncPlayerChatEvent
    //@EventHandler(priority = EventPriority.MONITOR) // This event will fire from the main thread and allows the use of all of the Bukkit API, unlike the AsyncPlayerChatEvent.
    //public void onPlayerChat(PlayerChatEvent event){ if(!event.isCancelled()) process(event); }

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR)   // Called when a player attempts to tab-complete a chat message.
    //public void onPlayerChatTabComplete(PlayerChatTabCompleteEvent event){ process(event); }

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // This event is called whenever a player runs a command (by placing a slash at the start of their message). (early in cmd handling process)
    //public void onPlayerCommandPreprocess(PlayerCommandPreprocessEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a player drops an item from their inventory
    public void onPlayerDropItem(PlayerDropItemEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player edits or signs a book and quill item. If the event is cancelled, no changes are made to the BookMeta
    public void onPlayerEditBook(PlayerEditBookEvent event){ if(!event.isCancelled()) process(event); }

    // TODO: possible "duplicate" of projectile events
    @EventHandler(priority = EventPriority.MONITOR) // Called when a player throws an egg and it might hatch
    public void onPlayerEggThrow(PlayerEggThrowEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a players experience changes naturally
    public void onPlayerExpChange(PlayerExpChangeEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a player is fishing
    public void onPlayerFish(PlayerFishEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when the GameMode of the player is changed.
    public void onPlayerGameModeChange(PlayerGameModeChangeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Represents an event that is called when a player right clicks an entity that also contains the location where the entity was clicked.
    public void onPlayerInteractAtEntity(PlayerInteractAtEntityEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Represents an event that is called when a player right clicks an entity.
    public void onPlayerInteractEntity(PlayerInteractEntityEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Represents an event that is called when a player interacts with an object or air, potentially fired once for each hand. The hand can be determined using getHand().
    public void onPlayerInteract(PlayerInteractEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Fired when a player's item breaks (such as a shovel or flint and steel).
    public void onPlayerItemBreak(PlayerItemBreakEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // This event will fire when a player is finishing consuming an item (food, potion, milk bucket).
    public void onPlayerItemConsume(PlayerItemConsumeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Fired when a player changes their currently held item
    public void onPlayerItemHeld(PlayerItemHeldEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Represents when a player has an item repaired via the Mending enchantment.
    public void onPlayerItemMend(PlayerItemMendEvent event){ if(!event.isCancelled()) process(event); }

    // acceptable for interpreting logs
    @EventHandler(priority = EventPriority.MONITOR) // Called when a player joins a server
    public void onPlayerJoin(PlayerJoinEvent event){ process(event); }

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a player gets kicked from the server
    //public void onPlayerKick(PlayerKickEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a players level changes
    public void onPlayerLevelChange(PlayerLevelChangeEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player changes their locale in the client settings.
    public void onPlayerLocaleChange(PlayerLocaleChangeEvent event){ process(event); }

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Stores details for players attempting to log in
    //public void onPlayerLogin(PlayerLoginEvent event){ process(event); }

    // TODO: spammy?
    @EventHandler(priority = EventPriority.MONITOR) // Holds information for player movement events
    public void onPlayerMove(PlayerMoveEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a player picks up an arrow from the ground.
    public void onPlayerPickupArrow(PlayerPickupArrowEvent event){ if(!event.isCancelled()) process(event); }

    // deprecated
    //@EventHandler(priority = EventPriority.MONITOR) // Thrown when a player picks an item up from the ground
    //public void onPlayerPickupItem(PlayerPickupItemEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player is about to teleport because it is in contact with a portal.
    public void onPlayerPortal(PlayerPortalEvent event){ if(!event.isCancelled()) process(event); }

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // Stores details for players attempting to log in
    //public void onPlayerPreLogin(PlayerPreLoginEvent event){ process(event); }

    // acceptable for interpreting logs
    @EventHandler(priority = EventPriority.MONITOR) // Called when a player leaves a server
    public void onPlayerQuit(PlayerQuitEvent event){ process(event); }

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // This is called immediately after a player registers for a plugin channel.
    //public void onPlayerRegisterChannel(PlayerRegisterChannelEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player takes action on a resource pack request sent via Player.setResourcePack(java.lang.String).
    public void onPlayerResourcePackStatus(PlayerResourcePackStatusEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player respawns.
    public void onPlayerRespawn(PlayerRespawnEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR)  // Called when a player shears an entity
    public void onPlayerShearEntity(PlayerShearEntityEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player statistic is incremented.
    public void onPlayerStatisticsIncrement(PlayerStatisticIncrementEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR)   // Called when a player swap items between main hand and off hand using the hotkey.
    public void onPlayerSwapHandItems(PlayerSwapHandItemsEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Holds information for player teleport events
    public void onPlayerTeleport(PlayerTeleportEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player toggles their flying state
    public void onPlayerToggleFlight(PlayerToggleFlightEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player toggles their sneaking state
    public void onPlayerToggleSneak(PlayerToggleSneakEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a player toggles their sprinting state
    public void onPlayerToggleSprint(PlayerToggleSprintEvent event){ if(!event.isCancelled()) process(event); }

    // glorified EntityUnleashEvent (EntityUnleashEvent is superclass) -> functional duplicate
    //@EventHandler(priority = EventPriority.MONITOR)   // Called prior to an entity being unleashed due to a player's action.
    //public void onPlayerUnleashEntity(PlayerUnleashEntityEvent event){ if(!event.isCancelled()) process(event, event.getPlayer().getLocation().getChunk()); }

    // unnecessary
    //@EventHandler(priority = EventPriority.MONITOR) // This is called immediately after a player unregisters for a plugin channel.
    //public void onPlayerUnregisterChannel(PlayerUnregisterChannelEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when the velocity of a player changes.
    public void onPlayerVelocity(PlayerVelocityEvent event){ if(!event.isCancelled()) process(event); }

}
