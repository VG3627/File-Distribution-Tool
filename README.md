# File-Distribution-Tool

This Project was problem statement of Tally Codebrewers 2024(System Programming)

## Overview
This project is a Command-Line Interface (CLI) tool designed to facilitate file distribution across a network using multicast groups. The tool provides both sender and receiver functionalities, allowing Admin to send files to a multicast group and members can receive files from a admin. The tool includes role-based access contro.

Admin: Can send files to a multicast group.
Team Member: Can join a multicast group to receive files.

## Features

Role-Based Access: Admins can send files, while team members can receive files.

Multicast Group Management: Users can select from available multicast groups to join.
Subprocess Execution: The tool runs sender and receiver functionalities as separate subprocesses for better process management.

## Project Structure

receiver.py: Script to receive files over UDP multicast.

sender.py: Script to send files over UDP multicast.

tool.exe: To start the CLI.



# Getting Started with the File Distribution Tool

To get started with the File Distribution Tool, follow these steps:

## 1. Clone the Repository
Clone the repository using the following command:
    
```bash
git clone https://github.com/VG3627/File-Distribution-Tool.git
```

## 2. How to run

Open command prompt, go to the location of the cloned folder

```bash
cd dist
# for admin login 
# .\tool.exe admin_name admin_password

.\tool.exe admin adminpass

#for member login
# .\tool.exe member_name member_password

.\tool.exe member memberpass

```

## Future Enhancements

Add encryption for secure file transfer.
Improve the login system by integrating with a database.
