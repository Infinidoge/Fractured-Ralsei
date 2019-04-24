# Fractured-Ralsei, the Fluffiest Bot on Discord!
***
#### An Explanation
Ralsei is a multi-purpose modular Discord bot, friendly mainly to those who can program for the maximum functionality.
##### Note: This site will update with further information.

##### The main features of Ralsei are:
1. Dynamic cog loading
   * You can just drag and drop in cogs into the folder, and you can unload and reload them while the bot is running.
   * The bot comes with base functionality cogs, which can be disabled and configured to your liking.
2. Sharded out of the box
   * You can run with just 1 shard for small instances, or many if you want to upscale functionality.
   * Using MongoDB and PyMongo, Ralsei supports and natively uses configuration files for every server, for custom prefixes and more.
      * These server configurations can be tapped into by cogs you program or extensions you run!
3. Built for the general user and those who are experienced programmers
   * With extensive documentation and scripts which help with setup, anyone who can use a computer can setup Ralsei
      * Even for the pieces which Ralsei may be difficult to setup (I.E. the Databases or elements of custom functionality) the wiki will contain full setup instructions, in addition to links to the official resources of any outside elements, such as the MongoDB database's extensive documentation.
   * Experienced programmers will potentially enjoy the bounty of features available to those who wish to creature their own functionality, such as access to the database the bot uses, or hooks into the Dynamos directing the activity of the bot.
4. Extensive API
   * You can code your own bot out of the great amount of pieces within Ralsei. Documentation for such bot creation is documented in the github wiki.
5. Open Source and Community Driven
   * Have a feature that you feel Ralsei itself is lacking, or want to offer up a cog for the default cogs list? Feel free to fork the repository and add the feature, or make an issue and suggest it for the people of the internet to review and potentially implement.
   * Ralsei will always be open source, and always under the GNU AGPL v3 license, so it will remain open source for all of others modifications.
6. Backwards compatibility
   * Where possible, the minor versions iterated through on the **master** branch will be backwards compatible with code written for the current major version, and support will be given up until the major version prior, but said compatibility is not guaranteed across major versions and custom written code should be kept up to date with the latest version.
   
##### Some notes about running the bot.
* This bot **requires** a database to run, as the entire sharding configuration setup revolves around this Database.
* If you are planning on running Ralsei for the base of your major bot, it is recommended to not use the **dev-main** branch, as it changes often and can easily break custom coded setups. 
* All guarantees on stability and backwards compatibility are void on the **dev-main** branch, which can potentially change often.
