import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

# Explicit socket creation
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

class ClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("💬 PyTalk Chat")
        self.master.geometry("600x500")
        self.master.configure(bg="#E6E6FA")  

        
        self.header = tk.Canvas(master, height=50, bg="#E6E6FA", highlightthickness=0)
        self.header.pack(fill=tk.X)
        self.header.create_text(300, 25, text="PyTalk", font=("Helvetica", 28, "bold"),
                                fill="white", activefill="white", anchor="center")
        self.header.create_text(300, 25, text="PyTalk", font=("Helvetica", 28, "bold"),
                                fill="#6a0dad", anchor="center")

        
        self.chat_frame = tk.Frame(master, bg="#E6E6FA")
        self.chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.user_frame = tk.Frame(master, bg="#dcd0ff", width=120)
        self.user_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.user_label = tk.Label(self.user_frame, text="👥 Users", bg="#dcd0ff", fg="#4B0082", font=("Helvetica", 12, "bold"))
        self.user_label.pack(pady=(10, 5))

        self.user_listbox = tk.Listbox(self.user_frame, bg="#f4f0ff", fg="#333", font=("Helvetica", 10))
        self.user_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        
        self.text_area = scrolledtext.ScrolledText(self.chat_frame, bg="#f5f5f5", fg="#000000", font=("Helvetica", 12))
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_area.config(state='disabled')

        
        self.entry = tk.Entry(self.chat_frame, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        
        self.nickname = simpledialog.askstring("Nickname", "Choose your nickname:", parent=master)
        if self.nickname.lower() == 'admin':
            self.password = simpledialog.askstring("Password", "Enter admin password:", show='*', parent=master)
        else:
            self.password = None

        self.running = True
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            command = message.strip().lower()
            if command.startswith("/kick") and self.nickname == "admin":
                target = command[6:]
                client.send(f'KICK {target}'.encode('ascii'))
            elif command.startswith("/ban") and self.nickname == "admin":
                target = command[5:]
                client.send(f'BAN {target}'.encode('ascii'))
            elif command.startswith("/kick") or command.startswith("/ban"):
                self.append_message("❌ Only admin can use that command.")
            else:
                now = datetime.now().strftime("%H:%M")
                full_message = f"[{now}] {self.nickname}: {message}"
                client.send(full_message.encode('ascii'))
            self.entry.delete(0, tk.END)

    def receive(self):
        while self.running:
            try:
                message = client.recv(1024).decode('ascii')

                if message == 'NICK':
                    client.send(self.nickname.encode('ascii'))

                elif message == 'PASS':
                    client.send(self.password.encode('ascii'))

                elif message == 'REFUSE':
                    self.append_message("❌ Wrong admin password. Connection refused.")
                    self.running = False
                    client.close()

                elif message == 'BAN':
                    self.append_message("🚫 You are banned from this server.")
                    self.running = False
                    client.close()

                elif message.startswith("USERLIST:"):
                    users = message.replace("USERLIST:", "").split(',')
                    self.update_user_list(users)

                else:
                    self.append_message(message)

            except Exception:
                self.append_message("⚠️ Connection lost.")
                self.running = False
                client.close()
                break

    def append_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.yview(tk.END)
        self.text_area.config(state='disabled')
        
        with open("chat_history.txt", "a") as f:
            f.write(message + "\n")


    def update_user_list(self, users):
        self.user_listbox.delete(0, tk.END)
        for user in users:
            if user.strip():
                self.user_listbox.insert(tk.END, user.strip())


root = tk.Tk()
gui = ClientGUI(root)
root.mainloop()
