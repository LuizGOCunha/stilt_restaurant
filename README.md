WELCOME TO STILT RESTAURANT!

This code is a simulation based on a test that the Stilt company was having for their developer position.
A junior dev (me) from the hunting team of Oowlish Technology decided to try it out for fun.
This is the result:

ABOUT THE CODE:
It's the simulation of a restaurant that has this data flow:

  Client 
    |
    | order every 2 seconds
    |
    |
    \/                          dispatch courier
 Kitchen (cooks food) -----------------------------> Courier
    |                                                   /
    |                                                  /
    |                                                 /
    |                                                /
    |                                               /
    \/                    Arrives to counter       /
  Counter (stores food) <_________________________/ 
    |
    |
    |
*FOOD DELIVERED!*

NOTES:
- All three main data structures (Client, Kitchen, Courier) work as separate processes, otherwise the code would get stuck on the first while loop
- The counter is nothing more than a data structure that serves as a gateway to the csv file thats serves as data storage
- There are two approaches for delivery: specific order and random order. in one the courier picks up an specific order, in the other he grabs the first one he sees
- The delivery approaches can be changed by commenting/uncommenting lines 33/34 from classes.py file 
- The timers that count the efficiency of every delivery approach are storaged in the deliverytime.csv file
- The amount of orders the clients will be able to send can be changed in line 80 on the classes.py file

It should also be noted that this code is not perfect, far from it. 
This code was written in one weekend by a man stricken by the flu.

PROBLEMS WITH THE CODE:
- When using the specific delivery method the code keeps running forever (must use ctrl+c)
- There was no organized testing done, only hands on debugging
- It wasn't possible to create all time metrics. Have not found a way to send the information of the time when the food is done for the Courier after it already initiated the paralel process of dispatch (could be solved with pointers, but this is python)
- There is an embarrassing amount of instances of "try: except ErrorCode: pass" in this code, which is far from good practice

FINAL WORDS:
This code was done with the intent of learning about multiprocessing, and i end this project a better dev than i started it.
I hope this is a good marker for how capable i am as a python programmer as of july 2022, may that be good or bad.
Thank you Stilt for the challenge, it was great.

- Luiz Gustavo Oliveira da Cunha