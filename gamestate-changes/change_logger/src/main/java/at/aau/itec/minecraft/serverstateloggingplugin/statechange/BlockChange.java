package at.aau.itec.minecraft.serverstateloggingplugin.statechange;

public class BlockChange extends Change {
    private String material = "";
    private String skylight = "";
    private String emittedLight = "";
    private String blockData = "";

    public BlockChange(long serverTime, String type, int xpos, int ypos, int zpos, String coordinates, String worldName){
        super(serverTime, type, xpos, ypos, zpos, coordinates, worldName);
    }

    public void setMaterial(String newMaterial){this.material = newMaterial;}
    public void setSkylight(String newSkylight){this.skylight = newSkylight;}
    public void setEmittedLight(String newEmittedLight){this.emittedLight = newEmittedLight;}
    public void setBlockData(String newBlockData){this.blockData = newBlockData;}

    @Override
    public String toString() {
        return super.toString() + String.format("\t%s\t%s\t%s\t%s", material, skylight, emittedLight, blockData);
    }
}
