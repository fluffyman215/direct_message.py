# direct_message.py

Run with the following command:

[YOUR PYTHON] GUI.py

NOTE: The framework of the graphical interface was provided by Professor Baldwin of ICS 32.

The GUI.py file is the graphical interface of our project. The GUI takes use of the DirectMessenger class in the ds_messenger.py file and allows for the user to send and receive messages.

The GUI contains 3 classes: Body, Footer, and MainApp. The MainApp class is the hub for all functions for the buttons in the Footer class. These include the main functionality for the Add User, Refresh, and the Send button. The Footer class connects the functionality of the functions in the MainApp to the GUI. Finally, the Body class manages the text and the inputs from user in response to interactions with the buttons and the text editor.

ds_messenger.py

The file contains the shell for sending and storing user data.

NOTE: The framework of this code was provided by Professor Baldwin of ICS 32.

The ds_messenger.py is the main relayer of information. It contains the funcitonality to send data to the server, store and manage data of the user, and receive messages from the server.

Essentially, the file contains the DirectMessenger Class which sends and receives information from the server utilizing a username, a password, a server id, and a token (which is received from the server via the join function). The DirectMessenger Class is weaved throughout the GUI, mainly the MainApp class.


ds_protocol.py

This file translates information stored in the DirectMessenger Class into JSON format to be readable to the server. The same file contains protocols to translate received messages from the server.
