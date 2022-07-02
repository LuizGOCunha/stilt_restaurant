from time import sleep
from random import randint
from uuid import uuid4

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
        print(f'Kitchen receives the order to cook {self.dishes[dish_index].name}')
        dish = self.dishes(dish_index)
        # We create the id for the order and then activate the Courier
        order_id = uuid4().hex
        self.couriers.dispatch(order_id)
        # Then it's time to prepare it based on how long is the prep time
        sleep(dish.prep_time)
        # This will put prepared food on the counter
        self.counter.put_food(dish.prepared(order_id))
        print(f'Order to cook {self.dishes[dish_index].name} with code {order_id} is Done!')


class Dishes:
    # Dishes are nothing but unprepared food, they are different from one another
    def __init__(self, name, prep_time):
        # Dishes are simple, they have a name...
        self.name = name
        # ...And a prep time
        self.prep_time = prep_time
        self.ready = False

    def prepared(self, order_id):
        # When the dish is prepared, we return it as food (ready to consume)
        return Food(self.name, order_id)

class Food(Dishes):
    # Food are dishes that have been prepared and are ready to consume
    def __init__(self, name, id):
        super().__init__(name)
        self.id = id
        self.ready = True

class Clients:
    def __init__(self, kitchen):
        # Clients will be unrelenting ordering machines, to keep our system functioning
        while True:
            self.order_up(kitchen)
            sleep(2)

    def order_up(self, kitchen):
        # We have to know which kitchen we are ordering in
        self.kitchen = kitchen
        # The order will be a random menu item
        order = randint(0,len(self.kitchen.dishes))
        print(f'Client selects the {self.kitchen.dishes[order]}')
        # then we ask them to cook the meal
        self.kitchen.cook(order)

class Counter:
    # The counter will be the place where the food will be put after its done.
    # Here it will wait for a courier
    def __init__(self):
        self.counter_top = []

    def put_food(self, food):
        self.counter_top.append(food)
        print(f'{food.name} with the code {food.id} is waiting to be delivered')

    def remove_food(self, food_index):
        self.counter_top.pop(food_index)

class Courier:
    # The courier will watch the Counter, and will act as soon as there is food in the counter top
    def __init__(self, counter):
        # The Couriers need to know where the counter is
        self.counter = counter

    def dispatch_random(self):
        # This type of dispatch make it so the courier grab the food that is ready randomly
        # The Courier always takes some time to get to the counter top
        sleep(randint(3,16))
        # Here he checks the amount of food in the counter top
        amount_of_food = len(self.counter.counter_top)
        # And here he does the eeny, meeny, miny, moe 
        random_counter_index = randint(0,amount_of_food)
        # after that, he takes the select food out and delivers it 
        self.counter.remove_food(random_counter_index)

    def dispatch_order(self, order_id):
        # The courier looks for the food with his order id, if he doesn't find it, he keeps looking
        while True:
            for index, food in enumerate(self.counter.counter_top):
                if food.id == order_id:
                    self.counter.remove_food(index)
                    print(f'{food.name} with the id {food.id} is delivered!')
                    break