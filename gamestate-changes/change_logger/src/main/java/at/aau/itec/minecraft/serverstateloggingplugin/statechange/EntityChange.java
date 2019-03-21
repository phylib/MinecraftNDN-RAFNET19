package at.aau.itec.minecraft.serverstateloggingplugin.statechange;

import java.util.LinkedList;
import java.util.UUID;

public class EntityChange extends Change {
    private LinkedList<String> diff;
    private UUID uuid;

    public EntityChange(long serverTime, String type, int xpos, int ypos, int zpos, String coordinates, String worldName, UUID uuid, LinkedList<String> diff){
        super(serverTime, type, xpos, ypos, zpos, coordinates, worldName);
        this.uuid = uuid;
        this.diff = diff;
    }

    @Override
    public String toString() {
        return super.toString() + "\t" + uuid + "\t" + diff.toString();
    }
}
