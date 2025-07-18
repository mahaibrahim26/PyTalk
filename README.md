# PyTalk 💬

**Author:** Maha Ibrahim  
**Course:** Computer Networks Final Project  
**Date:** July 2025

## Description
PyTalk is a Python-based chat application built with `socket`, `threading`, and a `Tkinter` GUI. It allows multiple clients to connect to a server, send/receive real-time messages, and includes admin features like kicking or banning users.

## Features
- Realtime chat with GUI (built using Tkinter)
- Admin authentication
- Kick and ban commands
- Message history with timestamps
- Stylish lavender UI with bubbly branding

## Technologies Used

- Python 3
- `socket` for networking
- `threading` for handling multiple clients
- `tkinter` for GUI
- Local file system for logging and bans

  
## How to Run

### 1. Start the Server
bash
python3 server.py


### 2 . Start a client
bash
python3 client.py

## For admin access:

Use nickname: admin

Password: adminpass

## Files
server.py: Main chat server

client.py: GUI-based chat client

bans.txt: Stores banned usernames

chat_history.txt: Logs chat messages with timestamps

README.md: Project overview

description.txt: Brief project description for submission


