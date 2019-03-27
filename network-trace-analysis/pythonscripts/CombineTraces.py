import argparse
import pandas as pd
import numpy as np
import math
from enum import Enum
import os
import glob

import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

start_time = 0

def execute(input, players):
    input_files = glob.glob(input + "*interpolated.csv")

    ##################### MERGE AND SORT TRACES
    df_list = []
    for input_file in input_files:
        stream_identifier = input_file.split("/")[-1].split("_")[0]
        df = pd.read_csv(input_file, delimiter="\t")
        df = df.ix[:, 1:]
        # Filter only clientbound packets
        df = df[df["Direction"] == "S->C"]
        df["stream"] = stream_identifier
        df_list.append(df)

    df = pd.concat(df_list)
    df = df.sort_values(by=["Timestamp"])
    df.reset_index()
    df.index = range(0, len(df))

    #################### CALCULATE TICK
    global start_time
    start_time = df.loc[0, "Timestamp"]

    def getTickNo(csv_entry):
        ts = csv_entry["Timestamp"]
        global start_time
        ts -= start_time
        tick = int(ts / 1000 / 20)
        return tick
    df["Tick"] = df.apply(getTickNo, axis=1)


    #################### Calculate packet name
    # name should be in format
    # /<chunkXZ>/<tick>/<entityId>/<packettype>
    def get_ndn_name(csv_entry):

        entity_id = csv_entry["EntityId"]
        if math.isnan(entity_id):
            # in the first version, only classify entity packets
            return
        entity_id = int(entity_id)
        return "/" + str(csv_entry["Chunk"]) + "/" + str(csv_entry["Tick"]) + "/" + str(entity_id) + "/" + csv_entry["MessageType"] + "/"
    df["ndn-name"] = df.apply(get_ndn_name, axis=1)

    print(df)

    print(len(df[df["ndn-name"].str.contains("/", na=False)]["ndn-name"]))
    print(len(df[df["ndn-name"].str.contains("/", na=False)]["ndn-name"].unique()))


    df_names = df[df["ndn-name"].str.contains("/", na=False)]


    df.to_csv(input + "combined-trace.csv", sep="\t")


# python3 ~/PythonScripts/minecraft/CombineTraces.py -i parsedPackets/
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputFolder", required=True)
    parser.add_argument("-p", "--playerList", default="219,93,180,57")
    args = parser.parse_args()

    input = args.inputFolder
    players = args.playerList

    execute(input, players.split(","))
