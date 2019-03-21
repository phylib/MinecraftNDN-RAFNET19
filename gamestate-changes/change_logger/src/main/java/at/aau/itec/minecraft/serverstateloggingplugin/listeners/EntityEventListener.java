package at.aau.itec.minecraft.serverstateloggingplugin.listeners;

import org.bukkit.block.Block;
import org.bukkit.Chunk;
import org.bukkit.Location;
import org.bukkit.block.BlockState;
import org.bukkit.entity.Entity;
import org.bukkit.event.Event;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.*;
import org.bukkit.event.entity.EntityEvent;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.logging.Logger;

public class EntityEventListener implements Listener {
    private Logger logger;
    private HashSet<Entity> dirtyEntities;
    private HashSet<Block> dirtyBlocks;
    private HashSet<Chunk> dirtyChunks;

    public EntityEventListener(Logger log, HashSet<Entity> dirtyEntites, HashSet<Block> dirtyBlocks, HashSet<Chunk> dirtyChunks){
        logger = log;
        this.dirtyEntities = dirtyEntites;
        this.dirtyBlocks = dirtyBlocks;
        this.dirtyChunks = dirtyChunks;
    }

    private void process(EntityEvent event){
        process(event,"",new ArrayList<>());
    }

    private void process(Event event, Entity firstEntity, Entity otherEntity){
        for(Entity e : Arrays.asList(firstEntity, otherEntity)){
            //dirtyEntities.add(e);
            dirtyChunks.add(e.getLocation().getChunk());
        }

        /*Location entityLoc = firstEntity.getLocation();
        Chunk ch = entityLoc.getChunk();

        logger.info(firstEntity.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" + entityLoc +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t");
         */

    }

    private void process(EntityEvent event, List<Block> involvedBlocks){
        process(event, "", involvedBlocks, Arrays.asList(event.getEntity()));
    }

    private void process(EntityEvent event, String additionalText, List<Block> involvedBlocks){
        process(event, additionalText, involvedBlocks, Arrays.asList(event.getEntity()));
    }

    private void process(EntityEvent event, String additionalText, List<Block> involvedBlocks, List<Entity> involvedEntities){
        Entity e = event.getEntity();
        Location entityLoc = e.getLocation();
        Chunk ch = entityLoc.getChunk();
        dirtyChunks.add(ch);

        // especially involved blocks e.g. a door block broken by the entity
        for(Block b : involvedBlocks){
            //dirtyBlocks.add(b);
            dirtyChunks.add(b.getChunk());
        }

        for(Entity en : involvedEntities){
            //dirtyEntities.add(en);
            dirtyChunks.add(en.getLocation().getChunk());
        }

        /*logger.info(e.getWorld().getFullTime() + "\t" + event.getEventName() + "\t" + entityLoc +
                "\t@ chunk (" + ch.getX() + "," + ch.getZ() + ")\t" + additionalText);
        */
    }

    //org.bukkit.event.entity.EntityChangeBlockEvent
    // bukkit-1.12.2-R0.1-SNAPSHOT.jar - Handles events from org.bukkit.event.entity.*

    @EventHandler(priority = EventPriority.MONITOR) // Called when a lingering potion applies it's effects. Happens once every 5 ticks
    public void onAreaEffectCloudApply(AreaEffectCloudApplyEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a creature is spawned into a world.
    public void onCreatureSpawn(CreatureSpawnEvent event){ if(!event.isCancelled()) process(event, "", Arrays.asList(event.getLocation().getBlock())); }

    // TODO: necessary?
    @EventHandler(priority = EventPriority.MONITOR) // Called when a Creeper is struck by lightning.
    public void onCreeperPower(CreeperPowerEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an EnderDragon switches controller phase.
    public void onEnderDragonChangePhase(EnderDragonChangePhaseEvent event){ if(!event.isCancelled()) process(event); }

    // too many events per second!
    //@EventHandler(priority = EventPriority.MONITOR)  // Called when the amount of air an entity has remaining changes.
    //public void onEntityAirChange(EntityAirChangeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an Entity breaks a door
    public void onEntityBreakDoor(EntityBreakDoorEvent event){ if(!event.isCancelled()) process(event, Arrays.asList(event.getBlock())); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when one Entity breeds with another Entity.
    public void onEntityBreed(EntityBreedEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when any Entity, excluding players, changes a block.
    public void onEntityChangeBlock(EntityChangeBlockEvent event){ if(!event.isCancelled()) process(event, Arrays.asList(event.getBlock())); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a block causes an entity to combust.
    public void onEntityCombustByBlock(EntityCombustByBlockEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an entity causes another entity to combust.
    public void onEntityCombustByEntity(EntityCombustByEntityEvent event){ if(!event.isCancelled()) process(event); }

    // omitted because it is the superclass of (EntityCombustBy Block/Entity...)
    //@EventHandler(priority = EventPriority.MONITOR) // Called when an entity combusts.
    //public void onEntityCombust(EntityCombustEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a Living Entity creates a portal in a world.
    public void onEntityCreatePortal(EntityCreatePortalEvent event){
        if(!event.isCancelled()){
            ArrayList<Block>blocks = new ArrayList<>();
            for(BlockState bs : event.getBlocks()){
                blocks.add(bs.getBlock());
            }
            process(event, blocks);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an entity is damaged by a block
    public void onEntityDamageByBlock(EntityDamageByBlockEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an entity is damaged by an entity
    public void onEntityDamageByEntity(EntityDamageByEntityEvent event){ if(!event.isCancelled()) process(event); }

    // superclass of previous two (damage) events
    //@EventHandler(priority = EventPriority.MONITOR) // Stores data for damage events
    //public void onEntityDamage(EntityDamageEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown whenever a LivingEntity dies
    public void onEntityDeath(EntityDeathEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an entity explodes
    public void onEntityExplode(EntityExplodeEvent event){ if(!event.isCancelled()) process(event, event.blockList()); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an entity interacts with an object
    public void onEntityInteract(EntityInteractEvent event){ if(!event.isCancelled()) process(event, Arrays.asList(event.getBlock())); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a entity picks an item up from the ground
    public void onEntityPickupItem(EntityPickupItemEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an entity comes into contact with a portal
    public void onEntityPortalEnter(EntityPortalEnterEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a non-player entity is about to teleport because it is in contact with a portal.
    public void onEntityPortal(EntityPortalEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called before an entity exits a portal.
    public void onEntityPortalExit(EntityPortalExitEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Stores data for health-regain events
    public void onEntityRegainHealth(EntityRegainHealthEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an entity dies and may have the opportunity to be resurrected.
    public void onEntityResurrect(EntityResurrectEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a LivingEntity shoots a bow firing an arrow
    public void onEntityShootBow(EntityShootBowEvent event){ if(!event.isCancelled()) process(event, "", new ArrayList<Block>(), Arrays.asList(event.getProjectile())); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a LivingEntity is tamed
    public void onEntityTame(EntityTameEvent event){ if(!event.isCancelled()) process(event); }

    // too many events
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a creature targets or untargets another entity
    //public void onEntityTarget(EntityTargetEvent event){ if(!event.isCancelled()) process(event); }

    // too many events
    //@EventHandler(priority = EventPriority.MONITOR)  // Called when an Entity targets a LivingEntity and can only target LivingEntity's.
    //public void onEntityTargetLivingEntity(EntityTargetLivingEntityEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown when a non-player entity (such as an Enderman) tries to teleport from one location to another.
    public void onEntityTeleport(EntityTeleportEvent event){ if(!event.isCancelled()) process(event, Arrays.asList(event.getFrom().getBlock(), event.getTo().getBlock())); }

    @EventHandler(priority = EventPriority.MONITOR) // Sent when an entity's gliding status is toggled with an Elytra.
    public void onEntityToggleGlide(EntityToggleGlideEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called immediately prior to an entity being unleashed.
    public void onEntityUnleash(EntityUnleashEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a ThrownExpBottle hits and releases experience.
    public void onExpBottle(ExpBottleEvent event){ process(event); }

    // no actual change to game state (not yet)
    //@EventHandler(priority = EventPriority.MONITOR) // Called when an entity has made a decision to explode.
    //public void onExplosionPrime(ExplosionPrimeEvent event){ if(!event.isCancelled()) process(event); }

    // no actual change to game state
    //@EventHandler(priority = EventPriority.MONITOR) //Called when a firework explodes.
    //public void onFireworkExplode(FireworkExplodeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a human entity's food level changes
    public void onFoodLevelChange(FoodLevelChangeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a horse jumps.
    public void onHorseJump(HorseJumpEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // This event is called when a Item is removed from the world because it has existed for 5 minutes.
    public void onItemDespawn(ItemDespawnEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // ??
    public void onItemMerge(ItemMergeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when an item is spawned into a world
    public void onItemSpawn(ItemSpawnEvent event){ if(!event.isCancelled()) process(event); }

    // no actual change to game state
    //@EventHandler(priority = EventPriority.MONITOR) // Called when a splash potion hits an area
    //public void onLingeringPotionSplash(LingeringPotionSplashEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Stores data for pigs being zapped
    public void onPigZap(PigZapEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Thrown whenever a Player dies
    public void onPlayerDeath(PlayerDeathEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called immediately prior to a creature being leashed by a player.
    public void onPlayerLeashEntity(PlayerLeashEntityEvent event){
        if(!event.isCancelled()){ process(event, event.getLeashHolder(), event.getEntity()); }
    }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a splash potion hits an area
    public void onPotionSplash(PotionSplashEvent event){ if(!event.isCancelled()) process(event); }

    // superclass
    @EventHandler(priority = EventPriority.MONITOR) // Called when a projectile hits an object
    public void onProjectileHit(ProjectileHitEvent event){ process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a projectile is launched.
    public void onProjectileLaunch(ProjectileLaunchEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a sheep's wool is dyed
    public void onSheepDyeWool(SheepDyeWoolEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a sheep regrows its wool
    public void onSheepRegrowWool(SheepRegrowWoolEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a Slime splits into smaller Slimes upon death
    public void onSlimeSplit(SlimeSplitEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called whenever a villager acquires a new trade.
    public void onVillagerAcquireTrade(VillagerAcquireTradeEvent event){ if(!event.isCancelled()) process(event); }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a villager's trade's maximum uses is increased, due to a player's trade.
    public void onVillagerReplentishTrade(VillagerReplenishTradeEvent event){ if(!event.isCancelled()) process(event); }

}
