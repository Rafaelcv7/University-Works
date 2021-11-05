#Coded by Rafael Cedeno Vazquez
from os import system
import sys

if len(sys.argv) == 3:
    N = int(sys.argv[1]) #Receive the Size of the Memory
    file = sys.argv[2]   #Receive the input's file name
else:
    print("Try: python lifo.py < Size of N > < File name >")
    exit(1)


#LIFO Page replacement algorithm function
def LIFO_Replacement(memory, page):
    memory.pop(N - 1)
    memory.append(page)

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
    r_Bit = 0 #This bit indicates if the page has been reference recently

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

with open(file) as f: #to go Line by Line and input by input file is open all the time until end of process
    for line in f :
        input = line.split()
        for e in input :
            data = e.split(':') 
            page = PAGE(data[0], data[1]) #initialize Page object for each input which is expected as X:Y format
            if(searchInMemory(physical_Memory, page)) :  #Page is in physical memory
                page_Hits += 1
                page.r_Bit = 1
                #print('page found!')
            else :                                       #Page is not in physical memory
                page_Faults += 1
                if(len(physical_Memory) != N) :          #Memory is not full
                    physical_Memory.append(page)         #Page is allocated
                    #print('page fault!')
                else :                                   #Memory is full
                    LIFO_Replacement(physical_Memory, page) #Replacement Algorithm
                    #print('page fault!')


f.close()
#print('PH Total: {}'.format(page_Hits))
print('PF: {}'.format(page_Faults))
