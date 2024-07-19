import cv2
import socket
import numpy as np

# Server IP address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def receive_video(client_socket):
    while True:
        # Receive frame size
        frame_size_data = client_socket.recv(16)
        # print(frame_size_data)
        if not frame_size_data:
            break

        frame_size = int(frame_size_data.strip())
        if frame_size == 0:
            break

        # Receive frame data
        frame_data = b''
        while len(frame_data) < frame_size:
            remaining_bytes = frame_size - len(frame_data)
            frame_data += client_socket.recv(remaining_bytes)

        # Convert frame data to numpy array
        frame_np = np.frombuffer(frame_data, dtype=np.uint8)

        # Decode frame
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
        # Resize frame to 720x1080
        frame = cv2.resize(frame, (1080, 720))
        
        # Display frame
        cv2.imshow('Video Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def main():
    # Create socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"[*] Connected to {SERVER_HOST}:{SERVER_PORT}")

    # Request video file from server
    video_file = input("Enter video file name: ")
    client_socket.send(video_file.encode())

    # Receive and display video frames
    receive_video(client_socket)

    # Close socket connection
    client_socket.close()

if __name__ == "__main__":
    main()