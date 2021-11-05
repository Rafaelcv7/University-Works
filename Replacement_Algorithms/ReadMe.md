# Assigment03 Page Replacement Algorithms
<p align="center">
University of Puerto Rico at Rio Piedras
	</br>
Deparment of Computer Science
	</br>
CCOM4017: Operating Systems
	</p>

## About the project:
This projet implements a simulation of three types of known page replacement Algorithms. The LIFO (Last In First Out), the Optimal replacement
and the WSClock (Working Set Clock) replacement. Each Algorithms will receive a .txt file with different inputs in the format of X:Y where 
each inputs its a page thats the "OS" want to access and X stand for instruction (Read(R) or Write(W)) and Y stand for the number of the page which
simulates its address in virtual memory.
</br>
Each process will be allocating page's access to an array that simulates the physical memory and counting each Page Fault (When the current page that wants to
be accessed is not in memory) and each Page Hits (When the current page that wants to be accessed is in memory. Once the memory is full then if a page fault is
occurs it will run the corresponding Replacement algorithm and replace the page accordingly.
</br>
</br>
### LIFO Replacement Algorithm:
When physical memory is full the algorithm will replace the Last page that was allocated on the physical memory. This basically means that the last index of the array
will be the slot that would always get replaced, accordingly to physical memory size.
</br>
</br>
### Optimal Replacement Algorithm:
Unique to this algorithm, this algorithm is the only one that knows before hand the order in which each input will arrive. It can be simulated but not implemented in reality
since in reality there's no way to know in which order pages are going to be accessed. Since this algorithm know the order in which all the pages will arrive; what is does is that
when the physical memory is full and page faults occurs it will look to the future (the upcoming pages inputted) to see if the current pages in the physical memory are going to be
referenced in the future again. Once it finds a current page in physical memory not referenced in the future it will replace that page with the one thats wants to be accessed. If all
the current pages in memory are going to be referenced in the future it would replace the farthest one in the future.
</br>
</br>
### WSCLOCK Replacement Algorithm:
On this algorithm another property is added to the page object called tola which means "Time of last Arrival"
When physicial memory is full, this algorithm start a clock like iterator that goes through all the 
physical memory looking for a page that has it's referece bit in 0, if found and it's not in the working set (
the current virtual time minus the tola of the page is less than the TAU unit (Time Access Unit)); then that page is replaced
if the referenced bit is 1 then it gets updated to 0 but hand is move to the next so is not replaced. If the iterator go around
and to where it started without replacing a page then the page with the minimum Tola is replaced.
</br>
</br>
## How to use:
Each Algorithm is run separately as so:
LIFO:
```bash
python lifo.py <Size of memory> <filename>
```
OPTIMAL:
```bash
python optimal.py <Size of memory> <filename>
```
WSCLOCK:
```bash
python wsclock.py <Size of memory> <tau> <filename>
```

Note: Input file has to be .txt and with each input separated by whitespace and in format X:Y
