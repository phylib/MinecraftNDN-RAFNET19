# Analyzing the Minecraft network trace

The provided Minecraft network trace contains the raw traffic recorded on the server. The first step in analyzis is to parse the Minecraft packets from the TCP/IP traffic. Therefore, a small Java application, the `McPcapParser`, is used.

To build the Java project, simple execute the following commands:

    git submodule init
    cd McPcapParser
    mvn clean install

The `jar` file to run the parser should than be in `McPcapParser/target`.
