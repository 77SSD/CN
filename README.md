## Server README

This README file overviews the server application and outlines its functionalities, error-handling mechanisms, and tasks performed.

#### Server Overview

The server application facilitates secure communication and video streaming among multiple clients. It listens for incoming client connections, manages client information, encrypts and broadcasts messages, and streams video content upon client requests.

#### Functionalities

1. **Client Connection Management**
   - Upon connection, the server prompts clients to provide their name and generated public key.
   - It maintains a dictionary to store client names and corresponding public keys.
   - When a new client connects, the server broadcasts the updated dictionary to all connected clients.
   - Clients can disconnect by sending a "QUIT" message, which removes their entry from the dictionary and notifies other clients.

2. **Secure Communication Management**
   - Clients use the public key of the intended recipient to encrypt their messages.
   - The server broadcasts the encrypted messages to all clients.
   - Only the intended recipient possessing the corresponding private key can decrypt and read the message.

3. **Video Streaming Management**
   - The server maintains a directory with multiple resolutions for a video file.
   - Upon receiving a client's request, the server streams video frames sequentially from each resolution file.
   - Frames are sourced proportionately, ensuring a balanced distribution of frame qualities throughout the viewing experience.

#### Error Handling

- **Client Connection Errors**: The server handles errors related to client connections, ensuring graceful termination and cleanup.
- **Message Encryption Errors**: Proper error handling is implemented for encryption and decryption operations, preventing unexpected crashes.
- **Video Streaming Errors**: Error handling mechanisms are in place to manage issues related to video streaming, ensuring uninterrupted service.

#### Tasks Performed

1. **Client Connection Management** (6 marks)
   - Server socket created to receive client connection requests.
   - Clients prompted for name and public key.
   - Client information stored in a dictionary and broadcasted to all clients.
   - Clients can disconnect by sending a "QUIT" message.

2. **Secure Communication Management** (5 marks)
   - Clients encrypt messages using the recipient's public key.
   - Encrypted messages broadcasted via the server.
   - Only the intended recipient can decrypt and read the messages.

3. **Video Streaming Management** (4 marks)
   - Server maintains a directory with multiple video resolutions.
   - Video frames streamed sequentially from each resolution file, ensuring balanced quality distribution.

#### Conclusion

The server application provides robust functionality for managing client connections, facilitating secure communication, and streaming video content. Error handling mechanisms ensure smooth operation, enhancing the reliability of the server.


### Client README

This README provides an overview of the client application, its functionalities, and error handling mechanisms.

#### Client Overview

The client application facilitates communication with the server and enables video playback functionality. It establishes a connection with the server, sends and receives messages securely, and interacts with the server to play video files.

#### Functionalities

1. **Connection Establishment**
   - The client creates a socket and connects to the server.
   - Upon connection, it sends its name and generated public key to the server for identification and secure communication.

2. **Secure Communication**
   - The client maintains a dictionary to store other clients' names and public keys received from the server.
   - It updates the dictionary whenever the server broadcasts changes in client connections.
   - When sending a message to another client, the sender encrypts the message using the recipient's public key and sends it to the server.
   - The server broadcasts the encrypted message to all clients, and only the intended recipient can decrypt and read the message.

3. **Video Playback**
   - The client requests the server to list available videos.
   - It selects a video file from the available list and requests the server to play it.
   - The client receives video frames from the server and displays them for playback.

#### Error Handling

- **Connection Errors**: The client handles errors related to establishing connections with the server, ensuring graceful termination and cleanup.
- **Message Decryption Errors**: Proper error handling is implemented for decrypting received messages, preventing unexpected crashes.
- **Video Playback Errors**: Error handling mechanisms are in place to manage issues related to video playback, ensuring uninterrupted viewing experience.

#### Tasks Performed

1. **Connection Establishment** (4 marks)
   - Client socket created and connected to the server.
   - Client name and generated public key sent to the server for identification.

2. **Secure Communication** (4 marks)
   - Client maintains a dictionary of other clients' names and public keys.
   - Encrypts messages using recipient's public key and sends them to the server for broadcast.
   - Decrypts and displays received cipher text using its private key.

3. **Video Playback** (2 marks)
   - Client requests server to list available videos and selects one for playback.
   - Receives and displays video frames for playback.

#### Conclusion

The client application provides essential functionalities for establishing communication with the server, sending and receiving messages securely, and playing video files. Error handling mechanisms ensure smooth operation, enhancing the reliability of the client.



