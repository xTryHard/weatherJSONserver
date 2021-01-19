import socket
import semaphores as sem
import threading
import json
import queries



def worker(clients, workers_info):
    worker_data = {}
    greet_and_identify(workers_info, worker_data) #Initial thread info
    
    while True:
        sem.client_added.acquire() #Check new client added to queue

        sem.process_client.acquire() #Lock access to critical section

        client = clients.popleft() #Extract corresponding client
        print(clients)

        sem.process_client.release() #Exit critical section

        client_handler(client, workers_info, worker_data) #Handle client



def client_handler(client, workers_info, worker_data):
    print(f'Handling client: {client[1]}')

    update_thread_data(workers_info, worker_data, client[1][0], client[1][1], 'working')
    print('Updated workers info: ', workers_info)

    client[0].send(f'Hello, I am Thread: {threading.get_ident()}. I am here to serve you.'.encode())
    try:
        while True:
            #services_info(client)
            request = client[0].recv(4096).decode()

            if request == '':
                break

            print(request)
            
            is_request = analyze_request(request, workers_info)

            if (is_request == -1): client[0].sendall('Sorry. Your request is out of the scope of our services :('.encode())

            else:
                is_request_json = json.dumps(is_request, indent=4).encode()
                client[0].sendall(is_request_json)
    except:
        print('Client disconnected!')
    update_thread_data(workers_info, worker_data, 'enjoy', 'the journey', 'idle')
    print(workers_info)
    client[0].close() #If client disconnects, close connection


#Initial workers information
def greet_and_identify(workers_info, worker_data):
    # current_thread = {} #Current thread info
    thread_id = threading.get_ident()
    worker_data['thread_id'] = thread_id #Thread ID key
    worker_data['status'] = 'idle' #Status: working or idle
    worker_data['client_ip'] = 'enjoy' #Client IP
    worker_data['client_port'] = 'the journey' #Client Port

    sem.workers_info.acquire() #Acquire workers info dict

    workers_info[thread_id] = worker_data #Add current thread to workers info dict

    sem.workers_info.release() #Release workers info dict

    print('Workers info:', workers_info) 

#Update worker data, after connection of a client, or another event
def update_thread_data(workers_info, worker_data, client_ip, client_port, status):

    thread_id = threading.get_ident() #Current thread id
    
    worker_data['client_ip'] = client_ip #Update client IP
    worker_data['client_port'] = client_port #Update client port
    worker_data['status'] = status

    sem.workers_info.acquire() #Acquire workers info mutex
    workers_info[thread_id] = worker_data #Update current thread data
    sem.workers_info.release() #Release workers info mutex

#Prints to STDOUT the services offered and the commands to require them
#get_current: fetches the most recent weather info in the db.
#get_range: 
def services_info(client):
    info_str= '\n\nServices and its commands: \n\n\
    1. Get last reading: get_current\n\
    2. Get range of readings: get_range, start_date, end_date\n\
    3. Get server status: get_server_status, [active_only]\n\n'
    info_str = info_str.encode()
    client[0].sendall(info_str)


#Analyze request and choose proper query executor
def analyze_request(request, workers_info):
    
    request = json.loads(request) #parse request to object
    response = ''
    #Check if 'get_current' service is requested
    if (request['command'] == 'get_current'): 
        #Execute 'get_current_query'
        response = queries.get_current_query()

    #Check if 'get_range' service is requested
    elif (request['command'] == 'get_range'):
        #Execute 'get_range_query'
        response = queries.get_range_query(request['start_date'], request['end_date'])

    #Check if 'get_server_status' service is requested
    elif (request['command'] == 'get_server_status'):
    
        active_only = True

        if 'active_only' in request:
            if request['active_only'].lower() == 'false':
                active_only = False

        response = get_server_status_query(workers_info, active_only) #Execute 'get_server_status_query'
    else:
        response = -1 
    
    return response

#For 'get_server_status' request
def get_server_status_query(workers_info, active_only):

    response = {}
    response['status'] = 'OK'
    response['num_threads'] = len(workers_info)
    response['active_only'] = active_only
    response['active_threads'] = len(get_active_threads(workers_info))

    if (active_only): response['data'] = get_active_threads(workers_info)
    else: response['data'] = get_all_threads(workers_info)

    return response


#Get active threads
def get_active_threads(workers_info):
    active_threads = [] #List to keep active threads
    for key in workers_info: #Iterate through workers info dict
        #if thread is active ('working') add it to the list

        sem.workers_info.acquire() #Acquire mutex to access workers info dict
        if(workers_info[key]['status'] == 'working'): #If thread is active
            active_threads.append(workers_info[key]) #Add it to the list
        sem.workers_info.release() #Release mutex
    return active_threads

#Get all threads from the pool
def get_all_threads(workers_info):
    all_threads = []

    for key in workers_info:
        sem.workers_info.acquire()
        all_threads.append(workers_info[key])
        sem.workers_info.release()
    return all_threads

        

