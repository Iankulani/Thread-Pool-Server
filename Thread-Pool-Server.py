# -*- coding: utf-8 -*-
"""
Created on Tue March  26 08:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("Thread Pool Server")
print(Fore.GREEN+font)

import socket
import threading
import queue

# Function to handle client requests
def handle_client(client_socket, address):
    print(f"Connected to {address}")
    try:
        # Receive data from the client
        data = client_socket.recv(1024)
        print(f"Received: {data.decode('utf-8')} from {address}")

        # Respond to the client
        client_socket.send(f"Hello from server! Received your message: {data.decode('utf-8')}".encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the client connection
        client_socket.close()

# Function to manage the thread pool
def worker_thread(pool_queue):
    while True:
        # Get a client socket from the queue
        client_socket, address = pool_queue.get()
        if client_socket is None:
            break
        handle_client(client_socket, address)
        pool_queue.task_done()

# Function to start the thread pool server
def start_server(host, port, pool_size):
    # Create the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}. Waiting for connections...")

    # Create a queue to hold client sockets
    pool_queue = queue.Queue()

    # Create worker threads
    threads = []
    for _ in range(pool_size):
        thread = threading.Thread(target=worker_thread, args=(pool_queue,))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    # Accept incoming client connections
    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Accepted connection from {address}")
            pool_queue.put((client_socket, address))
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        # Stop worker threads by sending `None` to them
        for _ in range(pool_size):
            pool_queue.put((None, None))
        for thread in threads:
            thread.join()

# Main function to prompt user for input and start the server
def main():
    host = '0.0.0.0'  # Listen on all available network interfaces
    port = int(input("Enter the port number to start the server (e.g., 8080): "))
    pool_size = int(input("Enter the number of worker threads in the pool (e.g., 4): "))
    
    start_server(host, port, pool_size)

if __name__ == "__main__":
    main()
