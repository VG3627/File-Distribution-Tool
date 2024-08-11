import socket
import struct
import sys
import os
import time
import threading



BUFFER_SIZE = 1400 # Increased buffer size to optimize transmission

# Setup encryption







def send_multicast(group_ip, port, interface_ip, file_paths):
    """Send multiple files over UDP multicast with file-specific chunk indexing."""
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # Set the time-to-live (TTL) for multicast
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Set the outgoing interface for multicast
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface_ip))
    
    # Set the socket to non-blocking mode
    sock.setblocking(False)
    
    try:
        for file_path in file_paths:
            # Get the file name and size
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            # Send file metadata
            metadata = f"{file_name}|{file_size}"
            print(f"Sending metadata: {metadata}")
            sock.sendto(metadata.encode(), (group_ip, port))

            chunk_cnt = (file_size + BUFFER_SIZE - 1) // BUFFER_SIZE 

            # Send file in chunks with file-specific index
            
            with open(file_path, 'rb') as file:
                index = 1  # Use a consistent index for all chunks of this file
                byte_sent = 0 
                while chunk_cnt > 0:
                    chunk = file.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    # Send chunk with file-specific index
                    # chunk_data = f"{file_name}|{index}|".encode() + chunk
                    sock.sendto(chunk, (group_ip, port))
                    byte_sent += len(chunk)
                    
                    
                   
                    chunk_cnt -= 1 
                    time.sleep(0.001)  # Small delay to avoid overwhelming the network
                    
            print('\n')
            print(f"File {file_name} sent to {group_ip}:{port} from interface {interface_ip}")
            print(f"{byte_sent} bytes sent of {file_size} bytes")

    except socket.timeout:
        print("Socket timeout occurred. Consider increasing the timeout duration.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

def send_file_threaded(group_ip, port, interface_ip, file_paths):
    """Run send_multicast in a thread."""
    thread = threading.Thread(target=send_multicast, args=(group_ip, port, interface_ip, file_paths))
    thread.start()
    return thread

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python sender.py <multicast_group_ip> <port> <interface_ip> <file_path1> [file_path2 ...]")
        sys.exit(1)
    
    group_ip = sys.argv[1]
    port = int(sys.argv[2])
    interface_ip = sys.argv[3]
    file_paths = sys.argv[4:]

    # Start the sending in a new thread
    send_file_threaded(group_ip, port, interface_ip, file_paths)


