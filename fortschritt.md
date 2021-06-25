# ch4t
## Progress
### June 18th
- Elias: created git-repository and files and tested server client connection with ncat
- Tobias: first successful test of cli_client with ncat
- Simon: github not working, but first gui with two labels/buttons

### June 19th
- Elias: created new python-file server_object-oriented

### June 22nd
- Elias: working server with clients as objects in a class
- Tobias: first working cli_client featuring two threads for handling message sending and receiving simultaneously.

### June 23rd
- Tobias: Cli_client is now able to receive and load pickles. We can now send messages with user metadata
- Elias: Server is now able to recieve and load pickles

### June 24th
- Elias: The communication between the server and the cli_client is working now, but still working on the bug that happens, when a client leaves
- Tobias: added '-toserver' client messages and support for server to understand it. Created 'server multicast message' method
- General: Celebrating 100 commits

### June 25th
- Tobias: removed some bugs



## TO DOs
- decrement client list at server when client disconnects (for continous operation of server -> avoids long lists)
- server support: assign 'user' to client objects for e.g. status messages like 'client x disconnected'
- client restart with '-r' input and also ask when connection failed

