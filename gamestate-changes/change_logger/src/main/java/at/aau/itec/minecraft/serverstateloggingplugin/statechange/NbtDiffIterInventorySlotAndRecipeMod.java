package at.aau.itec.minecraft.serverstateloggingplugin.statechange;

import net.minecraft.server.v1_12_R1.*;

import java.util.Arrays;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;

public class NbtDiffIterInventorySlotAndRecipeMod {

    public static LinkedList<String> diff(String nbt1Json, String nbt2Json, List<String> keysToIgnore) throws MojangsonParseException {
        return diff( MojangsonParser.parse(nbt1Json), MojangsonParser.parse(nbt2Json), keysToIgnore);
    }

    public static LinkedList<String> diff(NBTTagCompound nbt1, NBTTagCompound nbt2, List<String> keysToIgnore){
        return diff(nbt1, nbt2, new LinkedList<>(), keysToIgnore);
    }

    private static LinkedList<String> diff(NBTTagCompound nbt1, NBTTagCompound nbt2, LinkedList<String> list, List<String> keysToIgnore){
        HashSet<String> nbt1Keys;
        HashSet<String> nbt2Keys;
        HashSet<String> intersectionKeys;
        NBTTagCompound[] nbtCompoundPair;
        NBTTagList[] nbtListPair, tmp;
        NBTBase item1, item2;
        String path;
        List<String> recipeBookLists = Arrays.asList("recipes", "toBeDisplayed");

        LinkedList<NBTTagList[]>tagListQueue = new LinkedList<>();
        LinkedList<NBTTagCompound[]>tagCompoundQueue = new LinkedList<>();
        LinkedList<String>tagListPaths = new LinkedList<>();
        LinkedList<String>tagCompoundPaths = new LinkedList<>();

        tagCompoundQueue.add(new NBTTagCompound[]{nbt1, nbt2});
        tagCompoundPaths.add("");


        while(true){
            if(!tagCompoundQueue.isEmpty()){
               path = tagCompoundPaths.removeFirst();
               nbtCompoundPair = tagCompoundQueue.removeFirst();
               nbt1Keys = new HashSet<>((nbtCompoundPair[0]).c());
               nbt2Keys = new HashSet<>((nbtCompoundPair[1]).c());
               nbt1Keys.removeAll(keysToIgnore);
               nbt2Keys.removeAll(keysToIgnore);
               intersectionKeys = new HashSet<>(nbt1Keys);
               intersectionKeys.retainAll(nbt2Keys);

                for(String key : intersectionKeys) { /// nbtCompoundPair[0].c() -> returns top-level keys of NBTTagCompound
                    item1 = nbtCompoundPair[0].get(key);
                    item2 = nbtCompoundPair[1].get(key);

                    if (!item1.equals(item2)) {
                        if(item1 instanceof NBTTagList && item2 instanceof NBTTagList){ // current items are tagLists (enqueue)
                            tmp = new NBTTagList[]{(NBTTagList) item1, (NBTTagList) item2};
                            if(recipeBookLists.contains(key)){
                                // handle list of (to be displayed) recipes in custom manner as they are just lists of String Values
                                diffStringTagLists(tmp, path + key + "/", list);
                            }else if(tmp[0].get(0).hasKey("Slot")){
                                tagCompoundQueue.add(new NBTTagCompound[]{convertSlotListToTagCompound(tmp[0]), convertSlotListToTagCompound(tmp[1])});
                                tagCompoundPaths.add(path + key + "/");
                            }else{
                                tagListQueue.add(tmp);
                                tagListPaths.add(path + key + "/");
                            }
                        }else if (item1 instanceof NBTTagCompound && item2 instanceof NBTTagCompound) { // current items are tagCompounds (enqueue)
                            tagCompoundQueue.add(new NBTTagCompound[]{(NBTTagCompound) item1, (NBTTagCompound) item2});
                            tagCompoundPaths.add(path + key + "/");
                        }else {
                            // current items are directly comparable ("primitive datatypes" like int, double, string, ...)
                            list.add(" - " + path + key + ":" + item1);
                            list.add(" + " + path + key + ":" + item2);
                        }
                    }

                }

                // all keys that exist in nbt1 (nbtCompoundPair[0]) but not in nbt2 (nbtCompoundPair[1]) (removed keys)
                nbt1Keys.removeAll(intersectionKeys);
                for(String key : nbt1Keys){
                    item1 = nbtCompoundPair[0].get(key);
                    list.add(" - " + path + key + ":" + item1.toString());
                }

                // all keys that exist in nbt2 (nbtCompoundPair[1]) but not in nbt1 (nbtCompoundPair[0]) (added keys)
                nbt2Keys.removeAll(intersectionKeys);
                for(String key: nbt2Keys){
                    item2 = nbtCompoundPair[1].get(key);
                    list.add(" + " + path + key + ":" + item2.toString());
                }

            }else if(!tagListQueue.isEmpty()){
                path = tagListPaths.removeFirst();
                nbtListPair = tagListQueue.removeFirst();

                int l1Size = nbtListPair[0].size();
                int l2Size = nbtListPair[1].size();
                int minsize = Math.min(l1Size, l2Size);

                for(int i=0; i < minsize; i++) {
                    item1 = nbtListPair[0].i(i);
                    item2 = nbtListPair[1].i(i);
                    if(item1 instanceof NBTTagCompound && item2 instanceof  NBTTagCompound){
                        tagCompoundQueue.add(new NBTTagCompound[]{(NBTTagCompound) item1, (NBTTagCompound) item2});
                        tagCompoundPaths.add(path + "[" + i + "]/");
                    }else if(item1 instanceof  NBTTagList && item2 instanceof  NBTTagList){
                        tmp = new NBTTagList[]{(NBTTagList) item1, (NBTTagList) item2};
                        if(tmp[0].get(0).hasKey("Slot")){
                            tagCompoundQueue.add(new NBTTagCompound[]{convertSlotListToTagCompound(tmp[0]), convertSlotListToTagCompound(tmp[1])});
                            tagCompoundPaths.add(path + "[" + i + "]/");
                        }else{
                            tagListQueue.add(tmp);
                            tagListPaths.add(path + "[" + i + "]/");
                        }
                    }else if(!item1.equals(item2)){
                        list.add(" - " + path +  "[" + i + "]" + ":" + item1);
                        list.add(" + " + path +  "[" + i + "]" + ":" + item2);
                    }
                }

                if(minsize < l1Size){ // l1 has more items than l2 (items removed)
                    for(int i = minsize; i<l1Size; i++){
                        item1 = nbtListPair[0].get(i);
                        list.add(" - " + path + "[" + i + "]" + ":" + item1.toString());
                    }
                } else if(minsize < l2Size){ // l2 has more items than l1 (items added)
                    for(int i = minsize; i<l2Size; i++){
                        item2 = nbtListPair[1].get(i);
                        list.add(" + " + path + "[" + i + "]" + ":" + item2.toString());
                    }
                }
            }else{
                // both queues are empty -> exit
                break;
            }
        }

        return list;
    }

    private static NBTTagCompound convertSlotListToTagCompound(NBTTagList list){
        NBTTagCompound resultCompound = new NBTTagCompound();
        NBTTagCompound entry;
        for(int i=0; i < list.size(); i++){
            entry = list.get(i);
            resultCompound.set("Slot:" + entry.get("Slot").toString(), entry);
        }
        return resultCompound;
    }

    private static void diffStringTagLists(NBTTagList[] tagLists, String key, LinkedList<String> list){
        HashSet<String> nbt1Keys = new HashSet<>(Arrays.asList(tagLists[0].toString().replaceAll("\\[|\\]|\"","").split(",")));
        HashSet<String> nbt2Keys = new HashSet<>(Arrays.asList(tagLists[1].toString().replaceAll("\\[|\\]|\"","").split(",")));
        HashSet<String> differenceKeys;
        nbt1Keys.remove("");
        nbt2Keys.remove("");

        differenceKeys = (HashSet<String>)nbt1Keys.clone();
        differenceKeys.removeAll(nbt2Keys); // all items that were there previously, but not anymore (-> were removed)
        for(String item : differenceKeys){
            list.add(" - " + key + item);
        }

        differenceKeys = (HashSet<String>)nbt2Keys.clone();
        differenceKeys.removeAll(nbt1Keys); // all items that were not previously present (-> were added)
        for(String item : differenceKeys){
            list.add(" + " + key + item);
        }
    }
}
