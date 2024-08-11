import subprocess
import sys
import os
import argparse
import json

GROUPS_FILE = 'groups.json'
MEMBERS_FILE = 'members.json'

def load_groups():
    """Load groups from JSON file."""
    if os.path.exists(GROUPS_FILE):
        with open(GROUPS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_groups(groups):
    """Save groups to JSON file."""
    with open(GROUPS_FILE, 'w') as f:
        json.dump(groups, f, indent=4)

def load_members():
    """Load members from JSON file."""
    if os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_members(members):
    """Save members to JSON file."""
    with open(MEMBERS_FILE, 'w') as f:
        json.dump(members, f, indent=4)

def run_receiver(group_ip,port):
    """Start the receiver code as a subprocess with the specified group IP."""
    command = [r'.\reciever.exe', group_ip, port]
    try:
        subprocess.Popen(command)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def run_sender(file_paths, group_ip, port, interface_ip):
    """Start the sender code as a subprocess."""
    
    command = [r'.\sender.exe', group_ip, port, interface_ip]
    for file in file_paths:
        command.append(file) 

    print(command)
    try:
        subprocess.Popen(command)
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

def list_multicast_groups(groups):
    """List available multicast groups."""
    if not groups:
        print("No groups available.")
        return []
    
    print("Available multicast groups:")
    for i, (group_name, group_info) in enumerate(groups.items(), 1):
        print(f"{i}. {group_name} (IP: {group_info['ip']})")
    return list(groups.keys())

def create_group():
    """Create a new multicast group."""
    group_name = input("Enter the group name: ")
    group_ip = input("Enter the multicast IP: ")
    group_port = input("Enter the multicast port: ")

    groups = load_groups()
    if group_name in groups:
        print("Group already exists.")
        return

    groups[group_name] = {'ip': group_ip, 'port': group_port}
    save_groups(groups)
    print("Group created successfully.")

def delete_group():
    """Delete an existing multicast group."""
    groups = load_groups()
    if not groups:
        print("No groups available to delete.")
        return

    group_names = list_multicast_groups(groups)
    if not group_names:
        return

    choice = int(input("Select a group to delete by number: "))
    if 1 <= choice <= len(group_names):
        group_name = group_names[choice - 1]
        del groups[group_name]
        save_groups(groups)
        print(f"Group {group_name} deleted successfully.")
    else:
        print("Invalid choice. Please select a valid number.")

def admin_actions():
    """Handle admin actions."""
    while True:
        action = input("Select action (1: Send files, 2: Create group, 3: Delete group, 4: Exit): ")
        if action == '1':
            groups = load_groups()
            if not groups:
                print("No groups available. Please create a group first.")
                continue
            
            group_names = list_multicast_groups(groups)
            if not group_names:
                continue
            
            choice = int(input("Select a group by number: "))
            if 1 <= choice <= len(group_names):
                group_name = group_names[choice - 1]
                filepaths = []
                num_files = int(input("Enter the number of files to send: "))
                for _ in range(num_files):
                    file_path = input("Enter the file path: ")
                    filepaths.append(file_path)
                interface_ip = int(input("Enter your interface_ip "))
                run_sender(filepaths, groups[group_name]['ip'],groups[group_name]['port'],interface_ip)
            else:
                print("Invalid choice. Please select a valid number.")
        elif action == '2':
            create_group()
        elif action == '3':
            delete_group()
        elif action == '4':
            break
        else:
            print("Invalid option. Please try again.")

def member_actions():
    """Handle member actions."""
    groups = load_groups()
    if not groups:
        print("No groups available. Please contact an admin to create a group.")
        return

    group_names = list_multicast_groups(groups)
    if not group_names:
        return

    choice = int(input("Select a group by number to join: "))
    if 1 <= choice <= len(group_names):
        group_name = group_names[choice - 1]
        members = load_members()
        if group_name not in members:
            members[group_name] = {'ip': groups[group_name]['ip'], 'port': groups[group_name]['port']}
            save_members(members)
        
        print("You have joined the group.")
        receive_files = input("Do you want to receive files now? (y/n): ")
        if receive_files.lower() == 'y':
            run_receiver(groups[group_name]['ip'],groups[group_name]['port'])
    else:
        print("Invalid choice. Please select a valid number.")

def main():
    parser = argparse.ArgumentParser(description='CLI for managing file transfer')
    parser.add_argument('username', help='Username for login')
    parser.add_argument('password', help='Password for login')
    
    args = parser.parse_args()
    
    role = login(args.username, args.password)
    
    if role == 'admin':
        admin_actions()
    elif role == 'member':
        member_actions()
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
