package at.aau.itec.minecraft.serverstateloggingplugin.statechange;


public class Change {
    private long serverTime; // ms
    private String type = "genericChange";
    private int xpos, ypos, zpos;
    private String world;
    private String chunkCoordinates;
    private int section;

    public Change(long serverTime, String type, int xpos, int ypos, int zpos, String coordinates, String worldName){
        this.serverTime = serverTime;
        this.type = type;
        this.xpos = xpos;
        this.ypos = ypos;
        this.zpos = zpos;
        this.chunkCoordinates = coordinates;
        this.world = worldName;
        this.section = (int)ypos >> 4;
    }

    @Override
    public String toString() {
        return String.format("%d\t%s\t%d\t%d\t%d\t%s\t%s\t%d", serverTime, type, xpos, ypos, zpos, world, chunkCoordinates, section);
    }
}
