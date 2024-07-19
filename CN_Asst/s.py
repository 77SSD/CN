import cv2
import socket

# Server IP address and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000

# Function to send video frames over the socket
def send_video(conn, video_files):
    frame_counts = [0] * len(video_files)
    current_file_index = 0
    while current_file_index < len(video_files):
        cap = cv2.VideoCapture(video_files[current_file_index])
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = (total_frames // 3)*current_file_index
        end_frame = (total_frames // 3) * (current_file_index+1)
        print("start_frame: ", start_frame, " end_frame: ", end_frame, "total_frames: ", total_frames)
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            # Serialize frame
            frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
            # Send frame size and data
            conn.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)
            # Switch to the next file if one-third of frames sent
            if  current_frame >= end_frame:
                current_file_index += 1
                break

        cap.release()

def main():
    # Create socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # Accept incoming connections
        conn, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        # Receive requested video file name from client
        video_name = conn.recv(1024).decode()
        print(f"[*] Received request for video: {video_name}")

        try:
            # Generate video file names with different resolutions
            video_files = [
                f"{video_name}_240p.mp4",
                f"{video_name}_720p.mp4",
                f"{video_name}_1440p.mp4"
            ]
            # Send requested video
            send_video(conn, video_files)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Close connection
            conn.close()

if __name__ == "__main__":
    main()