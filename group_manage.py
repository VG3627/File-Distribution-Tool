# import argparse
# import subprocess
# import sys

# def login(username, password):
#     """Check credentials and return the role."""
#     admins = {'admin': 'adminpass'}
#     team_members = {'member': 'memberpass'}
    
#     if username in admins and admins[username] == password:
#         return 'admin'
#     elif username in team_members and team_members[username] == password:
#         return 'member'
#     else:
#         print("Invalid credentials")
#         return None

# def run_receiver(group_ip):
#     """Start the receiver code as a subprocess with the specified group IP."""
#     # Command to run the receiver script
#     command = ['python', 'reciever.py', group_ip, '5004']
#     subprocess.Popen(command)

# def run_sender(file_path):
#     """Start the sender code as a subprocess."""
#     # Command to run the sender script
#     command = ['python', 'sender.py', '224.0.0.1', '5004', '192.168.0.101', file_path]
#     subprocess.Popen(command)

# def list_multicast_groups():
#     """List available multicast groups (for demonstration, use static list)."""
#     groups = ['224.0.0.1', '224.0.0.2', '224.0.0.3']
#     print("Available multicast groups:")
#     for i, group in enumerate(groups, 1):
#         print(f"{i}. {group}")
#     return groups

# def main():
#     parser = argparse.ArgumentParser(description='CLI for managing file transfer')
#     parser.add_argument('username', help='Username for login')
#     parser.add_argument('password', help='Password for login')
    
#     args = parser.parse_args()
    
#     role = login(args.username, args.password)
    
#     if role == 'admin':
#         file_path = input("Enter the file path to send: ")
#         run_sender(file_path)
#     elif role == 'member':
#         groups = list_multicast_groups()
#         try:
#             choice = int(input("Select a multicast group by number: "))
#             if 1 <= choice <= len(groups):
#                 group_ip = groups[choice - 1]
#                 run_receiver(group_ip)
#             else:
#                 print("Invalid choice. Please select a valid number.")
#         except ValueError:
#             print("Invalid input. Please enter a number.")
#     else:
#         sys.exit(1)

# if __name__ == "__main__":
#     main()

import subprocess
import sys
import os
import argparse

# Define relative paths to the executables
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# RECEIVER_EXE = '/reciever.exe'
# SENDER_EXE = os.path.join(BASE_DIR, 'sender.exe')

def run_receiver(group_ip):
    """Start the receiver code as a subprocess with the specified group IP."""
    # print(RECEIVER_EXE)
    command = [r'.\reciever.exe', group_ip, '5007']
    try:
        subprocess.Popen(command)
        # result = subprocess.run(command, capture_output=True, text=True, check=True)
        # print("Receiver output:", result.stdout)
        # print("Receiver error output:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def run_sender(file_path):
    """Start the sender code as a subprocess."""
    command = ['.\sender.exe', '224.1.1.1', '5007', '192.168.0.101', file_path]
    try:
        subprocess.Popen(command)
        # print("Sender output:", result.stdout)
        # print("Sender error output:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def login(username, password):
    """Check credentials and return the role."""
    admins = {'admin': 'adminpass'}
    team_members = {'member': 'memberpass'}
    
    if username in admins and admins[username] == password:
        return 'admin'
    elif username in team_members and team_members[username] == password:
        return 'member'
    else:
        print("Invalid credentials")
        return None

def list_multicast_groups():
    """List available multicast groups (for demonstration, use static list)."""
    groups = ['224.1.1.1', '224.1.1.2', '224.1.1.3']
    print("Available multicast groups:")
    for i, group in enumerate(groups, 1):
        print(f"{i}. {group}")
    return groups

def main():
    parser = argparse.ArgumentParser(description='CLI for managing file transfer')
    parser.add_argument('username', help='Username for login')
    parser.add_argument('password', help='Password for login')
    
    args = parser.parse_args()
    
    role = login(args.username, args.password)
    
    if role == 'admin':
        file_path = input("Enter the file path to send: ")
        run_sender(file_path)
    elif role == 'member':
        groups = list_multicast_groups()
        try:
            choice = int(input("Select a multicast group by number: "))
            if 1 <= choice <= len(groups):
                group_ip = groups[choice - 1]
                run_receiver(group_ip)
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    # print(RECEIVER_EXE)
    main()
