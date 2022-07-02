from classes import Kitchen, Dishes, Clients, Counter, Courier
import multiprocessing

# Remember:
# Kitchen, Clients and Couries must work independently at ALL TIMES. They must be separated into different processes.

# Create the dishes
stilt_dishes = [
    Dishes(name="Steak", prep_time=5),
    Dishes(name="Roasted Potatoes", prep_time=8),
    Dishes(name="Pasta", prep_time=6),
    Dishes(name="Fried Chicken", prep_time=3),
    Dishes(name="Baião", prep_time=9),
]

# Create the counter where the food will rest
stilt_counter = multiprocessing.Process(Counter())

# Create the couriers that will deliver the food
stilt_couriers = multiprocessing.Process(Courier())

# Create the kitchen itself, presenting all the objects that came before
stilt_kitchen = multiprocessing.Process(Kitchen(stilt_dishes, stilt_counter, stilt_couriers))

# Now, after initializing the clients, it will bombard the kitchen with orders
stilt_clients = multiprocessing.Process(Clients(stilt_kitchen))

stilt_counter.start()