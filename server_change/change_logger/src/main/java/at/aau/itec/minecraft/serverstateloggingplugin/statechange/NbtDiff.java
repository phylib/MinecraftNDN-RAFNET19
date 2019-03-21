package at.aau.itec.minecraft.serverstateloggingplugin.statechange;

import net.minecraft.server.v1_12_R1.*;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;

public class NbtDiff {

    public static LinkedList<String> diff(String nbt1Json, String nbt2Json, List<String> keysToIgnore) throws MojangsonParseException {
        NBTTagCompound nbt1 = (NBTTagCompound) MojangsonParser.parse(nbt1Json);
        NBTTagCompound nbt2 = (NBTTagCompound) MojangsonParser.parse(nbt2Json);
        return diff(nbt1, nbt2, keysToIgnore);
    }

    public static LinkedList<String> diff(NBTTagCompound nbt1, NBTTagCompound nbt2, List<String> keysToIgnore){
        return diff(nbt1, nbt2, new LinkedList<String>(), "", keysToIgnore);
    }

    private static LinkedList<String> diff(NBTTagCompound nbt1, NBTTagCompound nbt2, LinkedList<String> list, String path, List<String> keysToIgnore){
        HashSet<String> nbt1Keys = new HashSet<>(nbt1.c());
        HashSet<String> nbt2Keys = new HashSet<>(nbt2.c());
        nbt1Keys.removeAll(keysToIgnore);
        nbt2Keys.removeAll(keysToIgnore);
        HashSet<String> intersectionKeys = new HashSet<>(nbt1Keys);
        intersectionKeys.retainAll(nbt2Keys);
        NBTBase item1, item2;

        for(String key : intersectionKeys) { /// nbt1.c() -> returns top-level keys of NBTTagCompound
            item1 = nbt1.get(key);
            item2 = nbt2.get(key);

            if (!item1.equals(item2)) {
                if(item1 instanceof NBTTagList && item2 instanceof NBTTagList){
                    diff((NBTTagList)item1,(NBTTagList)item2, list, path + key + "/", keysToIgnore);
                }else if (item1 instanceof NBTTagCompound && item2 instanceof NBTTagCompound) {
                    diff((NBTTagCompound)item1, (NBTTagCompound)item2, list, path + key + "/", keysToIgnore);
                }else {
                    list.add(" - " + path + key + ":" + item1);
                    list.add(" + " + path + key + ":" + item2);
                }
            }

        }

        // all keys that exist in nbt1 but not in nbt2 (removed keys)
        nbt1Keys.removeAll(intersectionKeys);
        for(String key : nbt1Keys){
            item1 = nbt1.get(key);
            list.add(" - " + path + key + ":" + item1.toString());
        }

        // all keys that exist in nbt2 but not in nbt1 (added keys)
        nbt2Keys.removeAll(intersectionKeys);
        for(String key: nbt2Keys){
            item2 = nbt2.get(key);
            list.add(" + " + path + key + ":" + item2.toString());
        }
        return list;
    }

    private static LinkedList<String> diff(NBTTagList l1, NBTTagList l2, LinkedList<String> list, String path, List<String> keysToIgnore){
        // check if list size equal
        int l1Size = l1.size();
        int l2Size = l2.size();
        int minsize = Math.min(l1Size, l2Size);
        NBTBase item1, item2;

        for(int i=0; i < minsize; i++){
            item1 = l1.i(i);
            item2 = l2.i(i);
            if(item1 instanceof NBTTagCompound && item2 instanceof  NBTTagCompound){
                diff((NBTTagCompound)item1, (NBTTagCompound)item2, list, path + "[" + i + "]/", keysToIgnore);
            }else if(item1 instanceof  NBTTagList && item2 instanceof  NBTTagList){
                diff((NBTTagList)item1, (NBTTagList)item2, list, path + "[" + i + "]/", keysToIgnore);
            }else if(!item1.equals(item2)){
                list.add(" - " + path +  "[" + i + "]" + ":" + item1);
                list.add(" + " + path +  "[" + i + "]" + ":" + item2);
            }
        }

        if(minsize < l1Size){ // l1 has more items than l2 (items removed)
            for(int i = minsize; i<l1Size; i++){
                item1 = l1.get(i);
                list.add(" - " + path + "[" + i + "]" + ":" + item1.toString());
            }
        } else if(minsize < l2Size){ // l2 has more items than l1 (items added)
            for(int i = minsize; i<l2Size; i++){
                item2 = l2.get(i);
                list.add(" + " + path + "[" + i + "]" + ":" + item2.toString());
            }
        }

        return list;
    }
}
