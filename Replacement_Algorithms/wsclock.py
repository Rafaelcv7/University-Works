from os import system
import sys

if len(sys.argv) == 4:
    #ip = sys.argv[1]
    N = int(sys.argv[1]) #Receive the Size of the Memory
    tau = int(sys.argv[2]) #Receive the tau unit
    file = sys.argv[3] #Receive the inputs file name
else:
    print("Try: python wsclock.py < Size of N > < tau > < File name >")
    exit(1)

#-------Functions Definitions:-----------------|
#Function to search in current memory the page with the minimum Tola (Time of last arrival)
def search_min_Tola(memory):
    tola = None
    index = 0
    for e in memory:
        if(e.tola < tola):
            tola = e.tola
            index = memory.index(e)
    return index

#WSCLOCK Page Replacement algorithm
def WSCLOCK_Replacement(memory, page, hand_Pointer):
    global virtual_Time
    start = hand_Pointer #The position in which the clock started rotating
    while True:
        if(memory[hand_Pointer].r_Bit == 0 and (virtual_Time - memory[hand_Pointer].tola) <= tau): #Check if current pointed page in memory is not referenced
            memory[hand_Pointer] = page                                                            #And if it's not in the working set
            page.r_Bit = 1 #update reference bit
            page.tola = virtual_Time #update page tola
            virtual_Time += 1 #clock +1 tick
            hand_Pointer = (hand_Pointer + 1) % N #Advance clock hand to next page
            return hand_Pointer
        else:                               #Pointed Page is referenced
            memory[hand_Pointer].r_Bit = 0  #Update reference bit to 0
            virtual_Time += 1               
            hand_Pointer = (hand_Pointer + 1) % N
            if(hand_Pointer == start):      #This means clock hands went full circle since the starting point
                #print("Getting minimum Tola")
                memory[search_min_Tola(memory)] = page #Page with minimum tola gets replaced
                hand_Pointer = (hand_Pointer + 1) % N
                return hand_Pointer

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

#--PAGE Object Implementation------------|
class PAGE:
    number = 0
    instruction = 'X' #This instruction will be Read(R) or Write(W), X is used as a placeholder
    r_Bit = 0  #This bit indicates if the page has been reference recently
    tola = 0 #Time of last arrival, the time the page got added to Memory or was last accessed

    #Constructor
    def __init__(self, instruction, number):
        self.number = number
        self.instruction = instruction

    #Function to print page with specific format X:Y
    def printing(self):
        print(self.instruction+':'+self.number)

#--Specific Variables------------------| 
input = []  #Used to hold each input from file before transforming it to page
physical_Memory = [] #The memory representation where a max of N pages can be stored
page_Faults = 0 #Keep track of every page fault (when a desired page is not in physical Memory array)
page_Hits = 0 #Keep track of every page hit (when desired page is found in physical memory array)
hand_Pointer = 0 #A pointer that goes through physical memory and go back to start at end (Like a clock)
virtual_Time = 0 #A clock simulation that keeps track of each second.

with open(file) as f: #To go Line by Line and input by input file is open all the time until end of process
    for line in f :
        input = line.split()
        for e in input :
            data = e.split(':')
            page = PAGE(data[0], data[1]) #initialize Page object for each input which is expected as X:Y format
            if(searchInMemory(physical_Memory, page)) : #Page is in physical memory
                page_Hits += 1
                page.r_Bit = 1
                page.tola = virtual_Time #update current page tola
                virtual_Time += 1
                #print('page found!')
                #print_Memory(physical_Memory)
            else :                     #Page is not in physical memory
                page_Faults += 1
                if(len(physical_Memory) != N) : #Memory is not full
                    physical_Memory.append(page) #Page is allocated
                    page.r_Bit = 1
                    page.tola = virtual_Time
                    virtual_Time += 1
                    hand_Pointer = (hand_Pointer + 1) % N
                    #print('page fault!')
                    #print_Memory(physical_Memory)
                else :                          #Memory is full
                    hand_Pointer = WSCLOCK_Replacement(physical_Memory, page, hand_Pointer) #Replacement Algorithm
                    #print('page fault!')
                    #print_Memory(physical_Memory)


    #print_Memory(physical_Memory)
    #print('PH Total: {}'.format(page_Hits))
    print('PF: {}'.format(page_Faults))
