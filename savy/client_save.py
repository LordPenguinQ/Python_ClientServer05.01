import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, simpledialog
import time

PORT = 12345
IP_ADDRESS = '127.0.0.1'

MAX_MESSAGE = 1024

shutdown_flag = threading.Event()


class ClientWindow:
    def __init__(self, master, nickname):
        self.master = master
        self.master.title("Chat z bazą danych :)")
        self.nickname = nickname
        self.setup_window()

        self.client = Client(self.nickname, self.update_chat)
        self.client.connect_to_server()

        self.receive_thread = threading.Thread(target=self.client.receive_messages)
        self.receive_thread.start()

    def setup_window(self):
        self.chat_display = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_display.pack(expand=True, fill=tk.BOTH)

        self.input_entry = Entry(self.master, state=tk.NORMAL)
        self.input_entry.pack(expand=True, fill=tk.BOTH)
        self.input_entry.bind('<Return>', lambda event: self.send_message())

        self.send_button = Button(self.master, text="Wyślij", command=self.send_message)
        self.send_button.pack(expand=True, fill=tk.BOTH)

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.attributes('-topmost', True)

    def send_message(self):
        message = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        if message.lower() == '/exit':
            shutdown_flag.set()
            self.delay_and_shutdown(3)
        else:
            self.client.send_message(message)

    def delay_and_shutdown(self, time_to_wait, message=None):
        self.typing_enabled = False
        self.input_entry.config(state=tk.DISABLED)
        self.chat_display.config(state=tk.NORMAL)
        if message:
            self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.insert(tk.END, f"Wylogowanie za {time_to_wait} sekund\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)
        self.master.after(time_to_wait * 1000, self.on_close)

    def update_chat(self, message):
        if "Blad polaczenia" in message:
            self.delay_and_shutdown(3)
        else:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, message + "\n")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.yview(tk.END)

    def on_close(self):
        shutdown_flag.set()
        self.receive_thread.join()
        self.master.destroy()


class Client:
    def __init__(self, nickname, update_callback):
        self.nickname = nickname
        self.update_callback = update_callback
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client_socket.connect((IP_ADDRESS, PORT))
            self.client_socket.send(self.nickname.encode('utf-8'))
        except socket.error as e:
            self.update_callback('Nie udało się połączyć !')
            shutdown_flag.set()

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

    def receive_messages(self):
        while not shutdown_flag.is_set():
            try:
                broad_message = self.client_socket.recv(MAX_MESSAGE).decode('utf-8')
                if not broad_message:
                    self.update_callback('Blad polaczenia')
                    shutdown_flag.set()
                    break
                if broad_message == 'KEEP-ALIVE':
                    continue
                self.update_callback(broad_message)
            except socket.error as e:
                self.update_callback('Blad polaczenia')
                shutdown_flag.set()


if __name__ == "__main__":
    root = tk.Tk()
    nickname = simpledialog.askstring("Login - okienko", "Podaj nick:")
    window = ClientWindow(root, nickname)
    root.mainloop()
