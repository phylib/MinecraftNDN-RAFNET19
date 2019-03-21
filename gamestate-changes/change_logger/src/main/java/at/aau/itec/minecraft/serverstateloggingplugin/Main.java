package at.aau.itec.minecraft.serverstateloggingplugin;

import at.aau.itec.minecraft.serverstateloggingplugin.listeners.*;
import at.aau.itec.minecraft.serverstateloggingplugin.util.LogFormatter;
import org.bukkit.Bukkit;
import org.bukkit.Chunk;
import org.bukkit.ChunkSnapshot;
import org.bukkit.World;
import org.bukkit.block.Block;
import org.bukkit.block.BlockState;
import org.bukkit.entity.Entity;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.world.ChunkLoadEvent;
import org.bukkit.event.world.ChunkUnloadEvent;
import org.bukkit.plugin.PluginManager;
import org.bukkit.plugin.java.JavaPlugin;
import at.aau.itec.minecraft.serverstateloggingplugin.statechange.ChunkDataSnapshot;

import java.io.IOException;
import java.util.*;
import java.util.logging.FileHandler;
import java.util.logging.Logger;
import at.aau.itec.minecraft.serverstateloggingplugin.statechange.EntityDataSnapshot;

public class Main extends JavaPlugin implements Listener {
    private Logger logger, fileLogger, changeLogger;
    private HashSet<Block> dirtyBlocks = new HashSet<>();
    private HashSet<Entity> dirtyEntities = new HashSet<>();
    private HashSet<Chunk> dirtyChunks = new HashSet<>();
    HashMap<String, ChunkDataSnapshot> chunkDataSnapshots = new HashMap<>();
    HashMap<UUID, EntityDataSnapshot> entitySnapshots = new HashMap<>();
    HashMap<UUID, EntityDataSnapshot> tileEntitySnapshots = new HashMap<>();
    HashSet<UUID> entityUuids = new HashSet<>();

    public void onEnable(){
        logger = getLogger();
        getServer().getPluginManager().registerEvents(this, this);

        try {
            String dateTime = new Date().toString().replace(" ","_");
            fileLogger = getFileLogger("EventTraceLog_.txt");
            changeLogger = getFileLogger("changeLog_" + dateTime + ".txt");
            changeLogger.info("time\ttype=\"block\"\txpos\typos\tzpos\tworld\tchunk\tsection\tmaterial\tskylight\temittedLight\tBlockData");
            changeLogger.info("time\ttype=\"entity\"\txpos\typos\tzpos\tworld\tchunk\tsection\tuuid\t[changed attributes]");
            changeLogger.info("time\ttype=\"status\"\t#loadedChunks\t#changedChunks\t#tileEntities\t#changedTileEntities\t#entities\t#changedEntities\t#onlinePlayers\ttotalStateDiffTime");
        }catch(IOException e){
            e.printStackTrace();
            Bukkit.getPluginManager().disablePlugin(this); // stop execution
        }
        // register event listeners to determine which Chunks have changed
        registerEventListeners();


        logger.info("Starting to log every 500ms");
        this.getServer().getScheduler().scheduleSyncRepeatingTask(this, new Runnable(){
            public void run()
            {
                long startTime = System.nanoTime(); // remember start of difference calculation
                HashSet<UUID> currentEntityUuids = new HashSet<>();
                long worldFullTime = getServer().getWorlds().get(0).getFullTime();

                // Check for changes to the entities (entities in all worlds, tile-entities in all loaded chunks)
                List<String> keysToIgnore =  Arrays.asList("Spigot.ticksLived");
                int loadedChunkCount = 0, changedChunkCount = dirtyChunks.size(), entityCount = 0, changedEntityCount = 0, tileEntityCount = 0, changedTileEntityCount = 0, onlinePlayerCount = getServer().getOnlinePlayers().size();

                for(World w : getServer().getWorlds()){ // diff entity states in ALL worlds
                    // Tile entities (block metadata)
                    Chunk[] loadedChunks = w.getLoadedChunks();
                    loadedChunkCount += loadedChunks.length;
                    for(Chunk c : loadedChunks){
                        BlockState[] tileEntities = c.getTileEntities();
                        tileEntityCount += tileEntities.length; // update total tileEntityCount
                        for(BlockState bs : tileEntities){
                            EntityDataSnapshot newEds = new EntityDataSnapshot(bs, c, keysToIgnore, changeLogger);
                            UUID key = newEds.getUniqueId();
                            currentEntityUuids.add(key);

                            if(tileEntitySnapshots.containsKey(key)){
                                if(!tileEntitySnapshots.get(key).diff(newEds, keysToIgnore).isEmpty()){ changedTileEntityCount++; }
                            }else{
                                // entity is "new" as no previous entity snapshot of it is present
                                newEds.logWithMessage(worldFullTime,"<added>" + newEds.getNbtTagString());
                            }
                            tileEntitySnapshots.put(key, newEds); // update in any case
                        }
                    }

                    // "Classic entities like mobs, players, objects"
                    List<Entity> entities = w.getEntities();
                    entityCount += entities.size(); // update total entityCount
                    for(Entity e : entities){
                        EntityDataSnapshot newEds = new EntityDataSnapshot(e, keysToIgnore, changeLogger);
                        UUID key = newEds.getUniqueId();
                        currentEntityUuids.add(key);

                        if(entitySnapshots.containsKey(key)){
                            if(!entitySnapshots.get(key).diff(newEds, keysToIgnore).isEmpty()){ changedEntityCount++; }
                        }else{
                            // entity is "new" as no previous entity snapshot of it is present
                            newEds.logWithMessage(worldFullTime,"<added>" + newEds.getNbtTagString());
                        }
                        entitySnapshots.put(key, newEds); // update in any case
                    }

                    // look for entities that were removed
                    entityUuids.removeAll(currentEntityUuids);
                    for(UUID key : entityUuids){
                        if(entitySnapshots.containsKey(key)){
                            entitySnapshots.get(key).logWithMessage(worldFullTime,"<removed>");
                            entitySnapshots.remove(key);
                        }else if(tileEntitySnapshots.containsKey(key)){
                            tileEntitySnapshots.get(key).logWithMessage(worldFullTime, "<removed>");
                            tileEntitySnapshots.remove(key);
                        }
                    }
                    entityUuids = (HashSet<UUID>)currentEntityUuids.clone();
                }

                // TODO: how do changed entities factor in this???
                // Check for changes to the blocks of chunks
                for(Chunk chk : dirtyChunks){

                    // Capture thread-safe read-only snapshot of chunk data
                    ChunkSnapshot snapshot = chk.getChunkSnapshot(false,false,false);
                    ChunkDataSnapshot cds = new ChunkDataSnapshot(snapshot, false, changeLogger);

                    if(chunkDataSnapshots.containsKey(cds.getKey())){
                        //logger.info(chunkDataSnapshots.get(cds.getKey()).diff(cds)); // diff chunkDataSnapshots if prev. snapshot available
                        // calculate + log diff of ChunkDataSnapshots
                        chunkDataSnapshots.get(cds.getKey()).diff(cds);
                    }

                    chunkDataSnapshots.put(cds.getKey(), cds); // update chunkDataSnapshots (base of comparison)

                }
                // fileLogger.info(buf.toString());  // commented out to along file-logs of eventListeners

                //dirtyBlocks.clear();
                //dirtyEntities.clear();
                dirtyChunks.clear();

                // write status line "time\ttype=\"status\"\t#loadedChunks\t#changedChunks\t#tileEntities\t#entities\t#onlinePlayers\ttotalStateDiffTime"
                String statusLine = String.format("%d\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s", worldFullTime, "status", loadedChunkCount, changedChunkCount, tileEntityCount, changedTileEntityCount, entityCount, changedEntityCount, onlinePlayerCount, (System.nanoTime() - startTime)/1000000.0 + "ms");
                logger.info(statusLine);
                changeLogger.info(statusLine);
            }
        }, 0l, 10l); // runnable, delay[ticks], period[ticks]
    }

    private void registerEventListeners(){
        PluginManager pluginManager = this.getServer().getPluginManager();

        BlockEventListener blockListener = new BlockEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        pluginManager.registerEvents(blockListener,this);

        InventoryEventListener inventoryListener = new InventoryEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        pluginManager.registerEvents(inventoryListener, this);

        // might give some information, but most might be better solved saving/comparing entitties! (e.g. no movement event exists)
        EntityEventListener entityListener = new EntityEventListener(fileLogger, dirtyEntities, dirtyBlocks, dirtyChunks);
        pluginManager.registerEvents(entityListener, this);

        EnchantmentEventListener enchantmentListener = new EnchantmentEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        pluginManager.registerEvents(enchantmentListener, this);

        HangingEventListener hangingListener = new HangingEventListener(fileLogger, dirtyEntities, dirtyBlocks, dirtyChunks);
        pluginManager.registerEvents(hangingListener, this);

        PlayerEventListener playerListener = new PlayerEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        pluginManager.registerEvents(playerListener, this);

        // currently unnecessary
        //ServerEventListener serverListener = new ServerEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        //pluginManager.registerEvents(serverListener, this);

        VehicleEventListener vehicleListener = new VehicleEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        pluginManager.registerEvents(vehicleListener, this);

        // necessary?
        //WeatherEventListener weatherListener = new WeatherEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        //pluginManager.registerEvents(weatherListener, this);

        // necessary? temporarily disabled
        //WorldEventListener worldListener = new WorldEventListener(fileLogger, dirtyBlocks, dirtyChunks);
        //pluginManager.registerEvents(worldListener, this);
    }

    // Chunk Data change specific EventHandlers
    @EventHandler(priority = EventPriority.MONITOR) // Called when a chunk is loaded
    public void onChunkLoad(ChunkLoadEvent event){
        Chunk ch = event.getChunk();
        String key = ch.getWorld().getName() + "/("+ch.getX()+","+ch.getZ()+")";
        //logger.info(key + " loaded");

        if(!chunkDataSnapshots.containsKey(key)){
            ChunkDataSnapshot cds = new ChunkDataSnapshot(ch.getChunkSnapshot(),false, changeLogger);
            chunkDataSnapshots.put(key, cds);
        }
    }

    @EventHandler(priority = EventPriority.MONITOR) // Called when a chunk is unloaded
    public void onChunkUnload(ChunkUnloadEvent event){
        if(!event.isCancelled()){
            Chunk ch = event.getChunk();
            String key = ch.getWorld().getName() + "/("+ch.getX()+","+ch.getZ()+")";
            //logger.info(key + " UNloaded");
            chunkDataSnapshots.remove(key); // remove unloaded chunk
        }
    }

    public void onDisable(){
        logger.info("Logging stopped");
    }

    private Logger getFileLogger(String fileName) throws IOException{
        Logger fileLogger = Logger.getLogger(fileName);
        fileLogger.setUseParentHandlers(false); // disable console output ( content already written to file )
        FileHandler fileHandler = new FileHandler("./" + fileName);
        fileLogger.addHandler(fileHandler);
        fileHandler.setFormatter(new LogFormatter());
        return fileLogger;
    }
}
