import socket
import struct
import os
import time
import threading



BUFFER_SIZE = 1400  # Increased buffer size for better performance

active_file_locks = {}




def receive_file(sock, group_ip, port, interface_ip):
    """Receive multiple files over UDP multicast with file-specific chunk indexing."""
    while True:
        try:
            # Receive file metadata
            while True:
                try:
                    metadata, addr = sock.recvfrom(BUFFER_SIZE)
                    if metadata:
                        break
                except BlockingIOError:
                    continue
            metadata = metadata.decode().strip()

            # Debugging: Print received metadata
            print(f"Received metadata: {metadata}")

            # Split metadata into file name and file size
            parts = metadata.split('|')
            if len(parts) != 2:
                raise ValueError("Unexpected metadata format")

            file_name = parts[0].strip()  # Get the file name and remove extra spaces
            file_size_str = parts[1].strip().strip('|')  # Remove extra spaces and trailing '|'
            file_size = int(file_size_str)
            chunk_cnt = (file_size + BUFFER_SIZE - 1) // BUFFER_SIZE 

            # Debugging: Print parsed metadata
            print(f"Parsed metadata - File name: {file_name}, File size: {file_size}")

            # Acquire lock for the file to prevent overwriting
            if file_name in active_file_locks:
                print(f"File {file_name} is already being received. Skipping this transmission.")
                continue

            active_file_locks[file_name] = True
            # received_chunks[file_name] = {}  # Initialize chunk tracking
            
            try:
                # Open file for writing
                with open(file_name, 'wb') as file:
                    byte_received = 0 
                    expected_index = 1
                    while chunk_cnt > 0:
                        try:
                            chunk_data, addr = sock.recvfrom(BUFFER_SIZE)
                            if not chunk_data:
                                continue
                            
                            file.write(chunk_data)
                            byte_received += len(chunk_data)
                           
                            
                            
                            expected_index += 1
                            if expected_index > (file_size + BUFFER_SIZE - 1) // BUFFER_SIZE:
                                break
                        
                        except BlockingIOError:
                            # If nothing is received, continue without blocking
                            time.sleep(0.1)  # Slight delay to avoid tight loop

                    print(f"File {file_name} received successfully.")
                    print(f"File {file_name} data loss : {file_size - byte_received}")
                    

            finally:
                del active_file_locks[file_name]
                # del received_chunks[file_name]

        except ValueError as e:
            print(f"Error parsing metadata: {e}")
        except UnicodeDecodeError as e:
            print(f"Error decoding metadata: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        # Wait for the next file's metadata
        print("Waiting for the next file...")

def receive_multicast(group_ip, port, interface_ip):
    """Set up the socket and start receiving files."""
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Set the socket to non-blocking mode
    sock.setblocking(False)
    
    # Bind the socket to the port
    sock.bind((interface_ip, port))
    
    # Join the multicast group
    mreq = struct.pack('4sl', socket.inet_aton(group_ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    print(f"Listening for files on {group_ip}:{port} from interface {interface_ip}")

    # Start a thread for receiving files
    thread = threading.Thread(target=receive_file, args=(sock, group_ip, port, interface_ip))
    thread.start()

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python multicast_receiver.py <multicast_group_ip> <port>")
        sys.exit(1)

    group_ip = sys.argv[1]
    port = int(sys.argv[2])
    interface_ip = '0.0.0.0'  # Listening on all interfaces

    receive_multicast(group_ip, port, interface_ip)

