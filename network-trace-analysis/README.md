# Analyzing the Minecraft network trace

The provided Minecraft network trace contains the raw traffic recorded on the server. The first step in analyzis is to parse the Minecraft packets from the TCP/IP traffic. Therefore, a small Java application, the `McPcapParser`, is used.

To build the Java project, simple execute the following commands:

    git submodule update --init --remote
    cd McPcapParser
    mvn clean install
    cd ..

The resulting `jar` file to run the parser should than be in `McPcapParser/target`. In order to parse minecraft packets from the PCAP file in the data folder, run the following command:

    java -jar MCPcapParser/target/mcpcapparser.jar -p ../data/networkTrace.pcap -o ./parsedPackets/

Not every single Minecraft packet can be parsed correctly, which is why some parsing errors occur, but in general, the parsed Minecraft packets now appear in the `parsedPackets` folder. Each file represents a single TCP session. Most of them only query the server for information like server version and only contain a few packets. Four of them however, represent the game sessions of the four players and are substantially larger in size.

In the following, Python scripts are used to extract relevant information from those packet-logs.

## Execute python scrips evaluating the traces

    # Create a virtual python environment
    python3 -m venv traceanalysis-env
    source traceanalysis-env/bin/activate
    # Install dependences
    pip install -r pythonscripts/requirements.txt
    # Execute script extracting chunk indizes
    ls parsedPackets/ | grep parsedPackets.log | xargs -I {} python3 pythonscripts/MCChunkInterpolation.py -i "./parsedPackets/{}"
    # Calculate figures from paper
    # This may take a while...
    python pythonscripts/CalculateMCPacketStatistics.py -i parsedPackets/143205122180-59194_parsedPackets_interpolated.csv -b False
    # To count the number of duplicated packets, execute the following command
    python pythonscripts/CombineTraces.py -i parsedPackets/
