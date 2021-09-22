from os import system
import socket, sys, random
from threading import Thread

#-[CONFIG VARIABLES:]-------------------------|
T = 5  #Number of Threads
N = 20   #Number of messages before edevice stop
TR = 5 #Random Job Time range (1 - J)
#---------------------------------------------|

#---[FUNCTIONS]--------------------------------------------------|
# This function creates a "Job" with the structure x:y
# Where x is the "ID" of the device and y the time of its process
def createJob(i) : 
    return "{0}:{1}".format(i,str(random.randrange(1,TR + 1)))


#-------------[eDEVICE THREADS PROCESS]------------------|
#Each thread creates a Job and then send it to the Server
#After receiving response it will repeat process N times
def threadProcess(i) :
    j = 0
    while j < N:
        send_data = createJob(i)
        s.sendto(send_data.encode('utf-8'), (ip, port))
        #print("\n 1. => Client: ", send_data, "\n")
        data, address = s.recvfrom(4088)
        #system("clear")
        print("\n 2. <= Server: ", data.decode('utf-8'), "\n")
        j += 1
    #print("device {} finished.".format(i))
#---------------------------------------------------------|

#A extension of Thread Class to specify Run and Thread Number
class CounterThread(Thread):
	def __init__ (self, t_number):	
		self.t_number = t_number
		Thread.__init__(self)
	# Define thread task.
	def run(self):
		threadProcess(self.t_number)

#Creates a Buffer to store all the threads, start them
#And tells main process to wait for them to finish		
def main():
	idealThreads = T
	thread = [0] * idealThreads
	# Create two threads to fill the buffer and start the threads	
	for i in range(idealThreads):
		thread[i] = CounterThread(i+1)
		thread[i].start()
		
	# Make the original thread wait for the created threads.
	for i in range(idealThreads):
		thread[i].join()
#----------------------------------------------------------------|

#---[MAIN PROCESS]-----------------------------------------------|    
# Get "IP address of client" and also the "port number"
# from argument 1 and argument 2
if len(sys.argv) == 3:
    ip = sys.argv[1]
    port = int(sys.argv[2])
else:
    print("Try: edevice.py <ip> <port> Ex: edevice.py localhost 4040")
    exit(1)

# Create socket for client
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
#Send a "handshake" to server to let it know how 
#many devices are going to connect.
s.sendto(str(T).encode('utf-8'), (ip, port))

main()
#After all threads finished the client sends a 0 to the server
#To let it know that it has finished and is safe to close connection
print("Ending Connection...")
end_connection = "0"
s.sendto(end_connection.encode('utf-8'), (ip, port))
s.close()
#----------------------------------------------------------------|