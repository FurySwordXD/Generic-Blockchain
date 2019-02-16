# Generic-Blockchain
All forms and validations are dynamically generated based on the variables names' in the class Data available in block_data.py
So all you need to do is modify this class as per your requirement and your blockchain will hold data in that structure.

To start the chain, run "python app_node.py < port >". You can run this multiple times to create more nodes in the network.

And for the user, "python client.py < ip of a node > < port of a node >". This runs on port 5010.
	
So once all the nodes are running, you can go the url of one of those nodes and set up the network, so that every nodes knows the existence of every other node. Once the network is setup, you can start adding transactions to each node, then, when they are mined they are added to the blockchain and are synchronized with the rest of the nodes.

By default, the app_node.py runs on 5001 and client.py gets connected to 5001. So any transaction created by the client/user is added to the transaction list on 5001 which needs to be mined from admin interface to be reflected on the chain and the rest of the nodes.

Create nodes -> Set up network -> Add Transaction -> Mine on the port with transactions -> Gets added to the chain -> Replicated throughout the network
