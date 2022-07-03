from time import sleep, perf_counter
from random import randint
from uuid import uuid4
import multiprocessing

# function to make the creation of paralel processes easier
def create_paralel_process(func, list_of_args=[]):
    if list_of_args:
        process = multiprocessing.Process(target=func, args=list_of_args)
    else:
        process = multiprocessing.Process(target=func)
    return process


class Kitchen:
    def __init__(self, dishes, counter, couriers):
        # list of dishes
        self.dishes = dishes
        # The counter for the kitchen
        self.counter = counter
        # List of available Couriers
        self.couriers = couriers

    def cook(self, dish_index):
        # We identify the dish that the client wants
        dish = self.dishes[dish_index]
        print(f'Kitchen receives the order to cook {dish.name}')
        # We create the id for the order and then activate the Courier
        order_id = uuid4().hex
        # Start the counter for when the order is created
        counter_start = perf_counter()
        # Create a paralel process to dispatch the food
        # dispatch_process = create_paralel_process(self.couriers.dispatch_order, list_of_args=[order_id,counter_start])
        dispatch_process = create_paralel_process(self.couriers.dispatch_random, list_of_args=[counter_start,])
        dispatch_process.start()
        # Then it's time to prepare it based on how long is the prep time
        print(f'{dish.name} is being prepared...')
        sleep(dish.prep_time)
        # The food becomes ready
        prepared_food = dish.prepared(id=order_id)
        # This will put prepared food on the counter
        self.counter.put_food(prepared_food)
        print(f'Order to cook {dish.name} with code {order_id} is Done!')


class Dishes:
    # Dishes are nothing but unprepared food, they are different from one another
    def __init__(self, name, prep_time):
        # Dishes are simple, they have a name...
        self.name = name
        # ...And a prep time
        self.prep_time = prep_time
        self.is_ready = False

    def prepared(self, id):
        # When the dish is prepared, we return it as food (ready to consume)
        return Food(self.name, id)

    def __str__(self):
        return self.name

class Food(Dishes):
    # Food are dishes that have been prepared and are ready to consume
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.is_ready = True

    def __repr__(self):
        return f'{self.name}'

class Clients:
    def __init__(self, kitchen):
        self.kitchen = kitchen

    def initiate_ordering(self):
        # Lets limit the amount with a counter
        i = 0
        # Clients will be unrelenting ordering machines, to keep our system functioning
        while i != 5:
            order_process = create_paralel_process(self.order_up, [self.kitchen,])
            order_process.start()
            sleep(2)
            i += 1

    def order_up(self, kitchen):
        # We have to know which kitchen we are ordering in
        self.kitchen = kitchen
        # The order will be a random menu item
        order = randint(0,len(self.kitchen.dishes)-1)
        print(f'Client selects the {self.kitchen.dishes[order]}')
        # then we ask them to cook the meal
        self.kitchen.cook(order)

class Counter:
    # The counter will be a csv file, the class object will be the gateway for the csv file
    # Here it will wait for a courier

    def return_complex_countercsv_list(self,clear_file=False) -> list:
        '''This function just splits the csv file by line, then by comma, returning a 2D list'''
        with open('counter.csv', 'r') as csv_file:
            csv_string = csv_file.read()
            csv_rows_list = csv_string.split('\n')
            csv_complex_rows_list = []
            for row in csv_rows_list:
                list_row = row.split(',')
                csv_complex_rows_list.append(list_row)
            if clear_file:
                # Dont panic, this is just so we can clear the file
                with open('counter.csv', 'w') as _:
                    pass
        return csv_complex_rows_list
    
    # Time tracking here serves the purpose of knowing for what is this function being used. If it's used for timetracking it will upload a third item to the file
    # Not a very good practice, i know. But i can't see better options at the moment
    def write_data_to_countercsv(self, file_name, line_list):
        '''Receives a list with the name and number of food order to be inserted into the csv file'''
        line = ''
        for item in line_list:
            line += item + ','
        line = line[:-1]
        line += '\n'
        with open(file_name, 'a') as csv_file:
            csv_file.write(line)

    def remove_line_from_countercsv(self,id,):
        '''Receives an id to be remove, then pulls all data from csv, store it in a variable, 
        then puts it back in excluding the line with the mentioned id. 
        REMEMBER!!: The id must be a string, otherwise the function won't work'''
        csv_list = self.return_complex_countercsv_list(clear_file=True)
        for line_list in csv_list:
            try:
                if line_list[1] == id:
                    continue
                else: 
                    self.write_data_to_countercsv('counter.csv',line_list)
            except IndexError:
                continue

    def put_food(self, food):
        '''Adds food to the counter top'''
        line_list = [f'{food.name}', f'{food.id}']
        self.write_data_to_countercsv('counter.csv',line_list)

    def remove_food(self, food_id):
        '''Remove a given item from counter top'''
        self.remove_line_from_countercsv(food_id)

    def return_first_food(self):
        '''Remove the first item on the counter top'''
        id_of_nearest_item = self.return_complex_countercsv_list()[1]
        return id_of_nearest_item



class Courier:
    # The courier will watch the Counter, and will act as soon as there is food in the counter top
    def __init__(self, counter):
        # The Couriers need to know where the counter is
        self.counter = counter

    def dispatch_random(self,counter_start):
        # This type of dispatch make it so the courier grab the food that is closer to him, then delivers it
        # The Courier always takes some time to get to the counter top
        time_to_get_there = randint(3,16)
        sleep(time_to_get_there)
        print(f'Courier has arrived to take an order')
        courier_arrival_timer = perf_counter()
        # The Courier starts watching the counter
        while True:
            # He will keep trying to remove the nearest food until some appear
            # The try/except exist so the program doesn't interrupt itself for not finding anything
            try:
                # Grabs the first food, saving its details on this variable
                food = self.counter.return_first_food()
                # Saves the id in this variable
                try:
                    food_id = food[1]
                # There must be a better way to do this... unfortunately, i don't know what it is
                except IndexError: 
                    pass
                # Delivers it based on id
                try:
                    self.counter.remove_food(food_id)
                # If it falls on the first except, ends up falling in this one too
                except UnboundLocalError:
                    pass
                # Time for us to save the delivery time
                counter_end = perf_counter()
                time_to_deliver = counter_end - counter_start
                timer_arrival_to_deliver = counter_end - courier_arrival_timer
                # Here we will save the delivery format in a foodname,foodcode,time_to_deliver format
                self.counter.write_data_to_countercsv('deliverytime.csv', [food[0],food[1],f'{timer_arrival_to_deliver}',f'{time_to_deliver}'])
                print(f'{food[0]} with the id {food[1]} is delivered!')
                break
            except KeyError:
                continue
        

    def dispatch_order(self, order_id, counter_start):
        # The courier looks for the food with his order id, if he doesn't find it, he keeps looking
        time_to_get_there = randint(3,16)
        sleep(time_to_get_there)
        print(f'Courier has arrived to take order with id {order_id}')
        courier_arrival_timer = perf_counter()
        while True:
            # This loop is the equivalent of the courier watching the countertop until his order arrives
            counter_contents = self.counter.return_complex_countercsv_list()
            for food in counter_contents:
                # check the id of the food (second index for each line)
                try:
                    if food[1] == order_id:
                        # Food delivered!
                        self.counter.remove_food(order_id)
                        # Time for us to save the delivery time
                        counter_end = perf_counter()
                        time_to_deliver = counter_end - counter_start
                        timer_arrival_to_deliver = counter_end - courier_arrival_timer
                        # Here we will save the delivery format in a foodname,foodcode,time_to_deliver format
                        self.counter.write_data_to_countercsv('deliverytime.csv', [food[0],food[1],f'{timer_arrival_to_deliver}',f'{time_to_deliver}'])
                        print(f'{food[0]} with the id {food[1]} is delivered!')
                        break
                # This is just so when it finds an empty string our code doesn't break, going to the next iteration instead
                except IndexError:
                    continue
        
