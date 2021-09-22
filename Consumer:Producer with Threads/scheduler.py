from os import system
import socket, sys
from threading import Thread, Lock, Semaphore
from time import sleep

#---[CONFIG VARIABLES:]----|
N = 2 # Number of threads.
#--------------------------|

#---[ENVIROMENT'S GLOBAL VARIABLES]---------------------------------|
SEM = Semaphore(0) # To wake and sleep Threads
MUTEX = Lock()     # To protect Critical Regions
SHARED_QUEUE = []  # A list shared between Threads
ADDRESS = None     # Address to receive on one thread and send on the other
#-------------------------------------------------------------------|

#---[FUNCTIONS]-----------------------------------------------------|
# Print proccesses table by Process ID and Total CPU time
def printTable() :
        for i in range(1,len(pTable)):
            print("pID: {0} CPU Time: {1}".format(i,pTable[i]))

# Store "process" received from client in the shared list
def storeIn_Queue(processR):
    SHARED_QUEUE.append(processR)
    #print("stored {}".format(processR))

# Return the Job with the shortest time using a Linear search
def fetchJob(list) :
    shortest_Time = int((list[0].split(":"))[1])
    shortest_Job = 0
    for e in range(len(list)):
        job_ID, job_time = list[e].split(":")
        if int(job_time) < shortest_Time :
            shortest_Time = int(job_time)
            shortest_Job = e
    #print("Consuming..! " + list[shortest_Job])    
    return list.pop(shortest_Job)

# A extension of Thread Class to specify Run and Thread Number
class CounterThread(Thread):
	
    def __init__ (self, t_number):
			
	    self.t_number = t_number
	    Thread.__init__(self)

	# Define inside what the thread is to do.
    def run(self):
#-------------[PRODUCER THREADS PROCESS]------------------|    
    # Threads with t_number lower than the half of the
    # Total number of threads will behave like Producers.
        if self.t_number <= (N/2):
            while True:
                global ADDRESS
                data, ADDRESS = s.recvfrom(4088)
                processR = data.decode('utf-8')
                if processR == "0": break # To end connection
                MUTEX.acquire() # Enters Critical Region
                storeIn_Queue(processR)
                SEM.release()   # Wake up Consumer thread
                MUTEX.release() # Gets out of Critical Region
#---------------------------------------------------------|

#-------------[CONSUMER THREADS PROCESS]------------------|
        # Threads with t_number higher than the half of 
        # The total number of threads will behave like Consumers
        elif self.t_number > (N/2):
            while True:
                SEM.acquire()   #Go to sleep until job in Queue
                MUTEX.acquire() #Enters Critical Region
                d_ID, j_Time = fetchJob(SHARED_QUEUE).split(":")
                MUTEX.release() #Gets out of Critical Region
                pTable[int(d_ID)] += int(j_Time)
                sleep(int(j_Time))
                system("clear")
                printTable()
                #print(SHARED_QUEUE)
                send_data = "Device: {0} consumed: {1} seconds of CPU time.".format(d_ID,j_Time)
                s.sendto(send_data.encode('utf-8'), ADDRESS)
                if len(SHARED_QUEUE) < 1:
                    break
#---------------------------------------------------------|
               
# Creates a Buffer to store all the threads, start them
# And tells main process to wait for them to finish	
def main():
	IDEALTHREADS = N
	thread = [0] * IDEALTHREADS
	# Create two threads to fill the buffer and start the threads	
	for i in range(IDEALTHREADS):
		thread[i] = CounterThread(i+1)
		thread[i].start()
		
	# Make the original thread wait for the created threads.
	for i in range(IDEALTHREADS):
		thread[i].join()

#-------------------------------------------------------------------|

#---[MAIN PROCESS]--------------------------------------------------| 
# Get "IP address of Server" and "port number" from 
# argument 1 and argument 2
if len(sys.argv) == 2:
    #ip = sys.argv[1]
    ip = "localhost"
    port = int(sys.argv[1])
else:
    print("Try: scheduler.py <ip> <port> Ex: scheduler.py localhost 4040")
    exit(1)

# Create a UDP socket and Bind it to port.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip, port)
s.bind(server_address)
print("Server is listening . . . ")

# Receive a handshake from client, with the total of devices
# that will connect, and prepare table.
data, ADDRESS = s.recvfrom(4088)
pTable = [0] * (int(data) + 1)

main()
#printTable()
s.close()
#-------------------------------------------------------------------|