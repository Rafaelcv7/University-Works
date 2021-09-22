# Consumer vs Producer Simulation with threads
<p align="center">
University of Puerto Rico at Rio Piedras
  </br>
Department of Computer Science
  </br>
CCOM4017: Operating Systems
  </p>
  
## About the project:
This project implements a simulation of Electronics devices which sends some Jobs to a compute Server. The Server will run the jobs for them
and send a message when done to the specific "edevice". 
</br>
</br>
### eDevice:
The edevice are simulated with threads, and each one is sending **N** messages with its ID and the time to compute a "Job". Using the structure X:Y
where X stands for "Device ID" and Y stands for "Job CPU Time".  Ex: 4:7  After each messages the edevice waits for server to respond to send the other</br>
The number of threads, the range of random generated Job times and how many messages each thread sends are configurable
</br>
</br>
### Compute Server:
In the server a Producer/Consumer problem solution is implemented, where one thread (the producer) takes care of receiving the messages from the edevices and storing them in a list that is shared between "Producer Thread" and "Consumer Thread". </br> The other thread (the consumer) access the shared list and with a
linear search, look for the "Job" with the shortest time and pick it up. The thread will sleep the time represented on the Job, update the Jobs Table and send
Done message to the corresponding edevice.

## Additional Features:
  - This implementation use a "handshake" like connection where at first the main process of the edevice.py sends a message with the total of devices
    that will be connecting to the Server. This way the server prepare the space for the table. It also does something similar at the end to end connection. </br>
  - Instead of having just 2 threads on the Server is possible to have **N** threads, the server will assign the role of ***Producer*** to a half of the threads and 
    ***consumer*** to the other half.
    - Note: *If more than 2 threads are present on the server the "end connection" gimmick won't work and programs would need to be stopped with Ctrl + Z*
  - Instead of printing to the screen the table at the end, it will update it consecutively as consumer, consume each process.
    - Note: *This can be disabled by commenting the `printTable()` function on the **Consumer Thread Process** and Decommenting the `printTable()` function after 
            `main()` in **Main Process**.*
  - **BONUS:** eDevices wait for server response before sending another message.

## How to Use:
Open two different terminals to run the two programs. </br>
First Run `scheduler.py` as such: </br>
```bash
python3 scheduler.py <Port>
```
On the other terminal run `edevice.py` as such: </br>
```bash
python3 edevice.py localhost <Same Port>
```
Note: Is important to run the two programs in this order.

## Demostration: </br>

![Programs-Demo](https://user-images.githubusercontent.com/55097377/134273246-02826cc0-73da-4867-be2e-328ec84ea9cb.mov)

#Extra: </br>
For better visuals of the process on `scheduler.py` decomment:
  - `print("Consuming..! " + list[shortest_Job])` on ``fetchJob()`` method.
  - `print(SHARED_QUEUE)` on Consumer Thread Process.



