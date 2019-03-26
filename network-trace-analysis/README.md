# Analyzing the Minecraft network trace

The provided Minecraft network trace contains the raw traffic recorded on the server. The first step in analyzis is to parse the Minecraft packets from the TCP/IP traffic. Therefore, a small Java application, the `McPcapParser`, is used.

To build the Java project, simple execute the following commands:

    git submodule init
    cd McPcapParser
    mvn clean install
    cd ..

The resulting `jar` file to run the parser should than be in `McPcapParser/target`. In order to parse minecraft packets from the PCAP file in the data folder, run the following command:

    java -jar MCPcapParser/target/mcpcapparser.jar -p ../data/networkTrace.pcap -o ./parsedPackets/

Not every single Minecraft packet can be parsed correctly, which is why some parsing errors occur, but in general, the parsed Minecraft packets now appear in the `parsedPackets` folder. Each file represents a single TCP session. Most of them only query the server for information like server version and only contain a few packets. Four of them however, represent the game sessions of the four players and are substantially larger in size.

In the following, Python scripts are used to extract relevant information from those packet-logs.
