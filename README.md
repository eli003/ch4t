# ch4t
the ultimate ch4t-bot (the 4 stands for 4ahel)

## Documentation
We want to make a chat were clients can connect to a server and send messsages to all users. When a clients sends a message, it provides the message and the user. The Server uses objects to handle the client connection and if a message from a client appears, it sends the message to all clients except to the one who sent it.

The GUI-Version of the client consists of a window, where all messages can be seen and on the bottom a text-input field in order to type in the message which should be sent.

For Communication, we will rely on an Object with a user and the message. For en/decoding we will use pickle. Documentation: 
https://pythonprogramming.net/pickle-objects-sockets-tutorial-python-3/

For developement it's nice to have more than one client active and open. To achieve this in PyCharm, start a client -> go to "Edit Configuration" in the upper right field -> check the option "Allow parallel run". You can now start another client without closing the old one :)

### Server
When the Server recieves a message of any client, it will send the message to all other clients.
The Server is waiting for you on Port 64001. Come by and have fun ;)

### CLI Client
For a better User Experience, we format the terminal output with colors. We use a 256-color scheme for our CLI client.
Documentation: https://stackabuse.com/how-to-print-colored-text-in-python


### GUI Client



