
from socket_server import server_socket as server #Importing the server instance
from socket_server import SHUT_RDWR
from collections import deque
import semaphores as sem
import threading
import worker_thread

MAX_WORKERS = 10 #Max number of working concurrent threads
clients = deque() #Queue for incoming clients. 
workers_info = {} #General info of the workers

def create_threads(clients):

    for _ in range(0, MAX_WORKERS):
        worker = threading.Thread(target=worker_thread.worker, args=(clients, workers_info, ))
        worker.start()

def main():
    create_threads(clients)
    running = True
    print(threading.get_ident())
    
    try:
        while running:
            client, address = server.accept() #accept client connection
            
            sem.process_client.acquire() #Acquire mutex for critial section

            clients.append((client, address)) #Add client to the queue
            print(clients)

            sem.client_added.release() #Alert workers about new client

            sem.process_client.release() #Release mutex for critical section

    except KeyboardInterrupt:
        server.shutdown(SHUT_RDWR)
        server.close()

if __name__ == "__main__":
    main()