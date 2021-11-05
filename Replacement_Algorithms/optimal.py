#Coded by Rafael Cedeno Vazquez
from os import system
import sys

if len(sys.argv) == 3:
    N = int(sys.argv[1]) #Receive the Size of the Memory
    file = sys.argv[2] #Receveive the inputs file name
else:
    print("Try: python optimal.py < Size of N > < File name >")
    exit(1)

#-----Functions Definitions:-------------------|

#Functions to search for a page in the upcoming inputs
#This functions search in reversed order for a page in
#the array with the future inputs to come. It also
#store the farthest page in the future from physicalMem
def searchInFuture(future, page):
    global farthest #store the farthest page in future
    z = 0           #store the index of the current farthest page
    for e in reversed(future):
        x = e.split(':')[1]
        if (x == page.number):
            if(future.index(e) > z):
                z = future.index(e)
                farthest = page
            return True
    return False

#Optimal Page Replacement Algorithm function
def optimal_Replacement(memory, future, page):
    global farthest
    for pages in range(len(memory)):
        if(searchInFuture(future, memory[pages])): #Check if current page of memory is going to be used in future
            #print('found in future')
            pass
        else:                                      #If not Page gets replaced
            memory[pages] = page
            return
    memory[memory.index(farthest)] = page          #If if all Pages in physical memory are used in the future, replace the farthest

#Look for a specific Page by number, in Physical memory
def searchInMemory(memory, page):
    for e in memory:
        if (e.number == page.number):
            e.instruction = page.instruction
            return True
    return False

#To print current pages in memory with specific format X:Y
#for debugging
def print_Memory(memory):
    for e in memory:
        e.printing()

#Return an array which contains all the inputs from the file.
def reveal():
    future = []
    with open(file) as f:
        for line in f :
            input = line.split()
            for e in input :
                future.append(e)
    return future

#--PAGE Object Implementation------------|
class PAGE:
    number = 0
    instruction = 'X' #This instruction will be Read(R) or Write(W), X is used as a placeholder
    r_Bit = 0 #This bit indicates if the page has been reference recently
    
    #Constructor
    def __init__(self, instruction, number):
        self.number = number
        self.instruction = instruction

    #Function to print page with specific format X:Y
    def printing(self):
        print(self.instruction+':'+self.number)

#--Specific Variables------------------| 
farthest = 0  #Variable that store the page that is used farthest in the future
input = []  #Used to hold each input from file before transforming it to page 
physical_Memory = [] #The memory representation where a max of N pages can be stored
future_Array = [] #Array that contains all the inputs from the file
page_Faults = 0 #Keep track of every page fault (when a desired page is not in physical Memory array)
page_Hits = 0 #Keep track of every page hit (when desired page is found in physical memory array)

future_Array = reveal()
#print(future_Array)

with open(file) as f: #To go Line by Line and input by input file is open all the time until end of process
    for line in f :
        input = line.split()
        for e in input :
            data = e.split(':')
            page = PAGE(data[0], data[1]) #initialize Page object for each input which is expected as X:Y format
            future_Array.pop(0) #Remove current inputted page from future_array
            if(searchInMemory(physical_Memory, page)) : #Page is in physical memory
                page_Hits += 1
                page.r_Bit = 1
                #print_Memory(physical_Memory)
                #print('page found!')
            else :                                      #Page is not in physical memory
                page_Faults += 1
                if(len(physical_Memory) != N) :         #Memory is not full
                    physical_Memory.append(page)        #Page is allocated
                    #print_Memory(physical_Memory)
                    #print('page fault!')
                else :                                  #Memory is full
                    optimal_Replacement(physical_Memory, future_Array, page) #Replacement Algorithm
                    #print_Memory(physical_Memory)
                    #print('page fault!')

f.close()    
#print('PH Total: {}'.format(page_Hits))
print('PF: {}'.format(page_Faults))
