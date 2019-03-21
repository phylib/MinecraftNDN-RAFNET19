package at.aau.itec.minecraft.serverstateloggingplugin.statechange;

import net.minecraft.server.v1_12_R1.*;
import sun.awt.image.ImageWatched;

import java.util.HashSet;
import java.util.LinkedList;

class NBTDiffTest {
    // https://www.spigotmc.org/threads/solved-mcp-string-to-nbt-data.269055/

    // Strings obtained by NBTTagCompond.toString()
    private static String nbtprev = "{AgeLocked:0b,HurtByTimestamp:0,Angry:0b,Sitting:0b,Attributes:[{Base:8.0d,Name:\"generic.maxHealth\"},{Base:0.0d,Name:\"generic.knockbackResistance\"},{Base:0.30000001192092896d,Name:\"generic.movementSpeed\"},{Base:0.0d,Name:\"generic.armor\"},{Base:0.0d,Name:\"generic.armorToughness\"},{Base:16.0d,Modifiers:[{UUIDMost:-3095412869162188454L,UUIDLeast:-6283034937680631004L,Amount:0.055668478091697275d,Operation:1,Name:\"Random spawn bonus\"}],Name:\"generic.followRange\"},{Base:4.0d,Name:\"generic.attackDamage\"}],Invulnerable:0b,FallFlying:0b,ForcedAge:0,PortalCooldown:0,AbsorptionAmount:0.0f,FallDistance:0.0f,InLove:0,DeathTime:0s,WorldUUIDMost:4274445143610573293L,HandDropChances:[0.085f,0.085f],PersistenceRequired:1b,Spigot.ticksLived:42147,Age:0,CollarColor:1b,Motion:[0.0d,-0.0784000015258789d,0.0d],Leashed:0b,UUIDLeast:-7796496611822457784L,Health:8.0f,Bukkit.updateLevel:2,LeftHanded:0b,Air:300s,OnGround:1b,Dimension:0,Rotation:[101.37413f,0.0f],HandItems:[{},{}],ArmorDropChances:[0.085f,0.085f,0.085f,0.085f],OwnerUUID:\"\",UUIDMost:4443869730051737981L,Pos:[446.5d,69.0d,421.5d],Fire:-1s,ArmorItems:[{},{},{},{}],CanPickUpLoot:0b,HurtTime:0s,WorldUUIDLeast:-8073140550504750389L}";
    private static String nbtnext = "{AgeLocked:0b,HurtByTimestamp:0,Angry:0b,Sitting:0b,Attributes:[{Base:8.0d,Name:\"generic.maxHealth\"},{Base:0.0d,Name:\"generic.knockbackResistance\"},{Base:0.30000001192092896d,Name:\"generic.movementSpeed\"},{Base:0.0d,Name:\"generic.armor\"},{Base:0.0d,Name:\"generic.armorToughness\"},{Base:16.0d,Modifiers:[{UUIDMost:-3095412869162188453L,UUIDLeast:-6283034937680631004L,Amount:0.055668478091697275d,Operation:1,Name:\"Random spawn bonus\"}],Name:\"generic.followRange\"},{Base:4.0d,Name:\"generic.attackDamage\"}],Invulnerable:0b,FallFlying:0b,ForcedAge:0,PortalCooldown:0,AbsorptionAmount:0.0f,FallDistance:0.0f,InLove:0,DeathTime:0s,WorldUUIDMost:4274445143610573293L,HandDropChances:[0.085f,0.085f],PersistenceRequired:1b,Spigot.ticksLived:42157,Age:0,CollarColor:1b,Motion:[0.0d,-0.0784000015258789d,0.0d],Leashed:0b,UUIDLeast:-7796496611822457784L,Health:8.0f,Bukkit.updateLevel:2,LeftHanded:0b,Air:300s,OnGround:1b,Dimension:0,Rotation:[101.37413f,0.0f],HandItems:[{},{}],ArmorDropChances:[0.085f,0.085f,0.085f,0.085f],OwnerUUID:\"\",UUIDMost:4443869730051737981L,Pos:[446.5d,69.0d,421.5d],Fire:-1s,ArmorItems:[{},{},{},{}],CanPickUpLoot:0b,HurtTime:0s,WorldUUIDLeast:-8073140550504750389L}";


    public static void main(String[] args) throws MojangsonParseException, InterruptedException {
        NBTTagCompound nbt1 = (NBTTagCompound) MojangsonParser.parse(nbtprev);
        NBTTagCompound nbt2 = (NBTTagCompound) MojangsonParser.parse(nbtnext);

        System.out.println(nbt1.toString());
        System.out.println(nbt2.toString());

        System.out.println("nbt1 equals nbt2: " + nbt1.equals(nbt2));

        LinkedList<String>result1 = new LinkedList<>(), result2 = new LinkedList<>(), result3 = new LinkedList<>(), result4 = new LinkedList<>();

        int numRuns = 600;

        //Thread.sleep(2000);
        // recursive version
        long startTime1 = System.nanoTime(); // remember start of difference calculation
        for(int i = 0; i < numRuns; i++){
            result1 = NbtDiff.diff(nbt1,nbt2,new LinkedList<>());
        }
        long endTime1 = System.nanoTime();

        //Thread.sleep(2000);
        // iterative version
        long startTime2 = System.nanoTime(); // remember start of difference calculation
        for(int i = 0; i < numRuns; i++){
            result2 = NbtDiffIter.diff(nbt1,nbt2,new LinkedList<>());
        }
        long endTime2 = System.nanoTime();

        //Thread.sleep(2000);
        // recursive version
        long startTime3 = System.nanoTime(); // remember start of difference calculation
        for(int i = 0; i < numRuns; i++){
            result3 = NbtDiff.diff(nbt1,nbt2,new LinkedList<>());
        }
        long endTime3 = System.nanoTime();

        //Thread.sleep(2000);
        // iterative version
        long startTime4 = System.nanoTime(); // remember start of difference calculation
        for(int i = 0; i < numRuns; i++){
            result4 = NbtDiffIter.diff(nbt1,nbt2,new LinkedList<>());
        }
        long endTime4 = System.nanoTime();

        long diff1 = endTime1 - startTime1;
        long diff2 = endTime2 - startTime2;
        long diff3 = endTime3 - startTime3;
        long diff4 = endTime4 - startTime4;
        System.out.println("recursive diff:\t" + (diff1/1000000.0) + "ms\tavg: " + ((diff1/numRuns)/1000000.0) + "ms");
        System.out.println(result1.toString());
        System.out.println("------------------------------");
        System.out.println("iterative diff:\t" + (diff2/1000000.0) + "ms\tavg: " + ((diff2/numRuns)/1000000.0) + "ms");
        System.out.println(result2.toString());
        System.out.println("------------------------------");
        System.out.println("recursive diff:\t" + (diff3/1000000.0) + "ms\tavg: " + ((diff3/numRuns)/1000000.0) + "ms");
        System.out.println(result3.toString());
        System.out.println("------------------------------");
        System.out.println("iterative diff:\t" + (diff4/1000000.0) + "ms\tavg: " + ((diff4/numRuns)/1000000.0) + "ms");
        System.out.println(result4.toString());

    }

}