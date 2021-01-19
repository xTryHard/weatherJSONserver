
from threading import Semaphore

#New client added semaphore:
client_added = Semaphore(0)

#Mutex from critical section of accesing queue of clients
process_client = Semaphore(1)

#Mutex for workers info dict
workers_info = Semaphore(1)