# ChangeLogger Minecraft plugin

The code in this folder is a snapshot of the `ChangeLogger` plugin. The plugin is under steady development and the current version can be found in http://path/to/git/repo. Nevertheless, this snapshot of the code was used to generate the game-state logging for the paper described by this repository.

## Installing the plugin

Before being able to build the plugin with `maven`, we need to build `craftbukkit` in version `1.12.2`. Therefore, complete the following steps:

1. Obtain the build_tools (https://www.spigotmc.org/wiki/buildtools/)
2. Build the spigot-server ("java -jar BuildTools.jar --rev 1.11.2")
3. `craftbukkit-1.12.2-R0.1-SNAPSHOT.jar` can be found in <BuildTools.jar-directory>/CraftBukkit/target
4. Place `craftbukkit-1.12.2-R0.1-SNAPSHOT.jar` in the `./lib` folder.


Finally, the plugin can be build. Therefore, execute the following command:

    mvn clean install

You can now find the plugin in the `target` directory. In order to use it, copy it to the `plugins` folder of your Spigot server. The plugin should be automatically start the logging process.
