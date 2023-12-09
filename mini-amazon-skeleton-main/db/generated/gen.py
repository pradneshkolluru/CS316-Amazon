from enum import unique
from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
from datetime import datetime

num_users = 100
num_sellers = 50
num_products = 20
#num_purchases = 2500
num_orders = 40

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('db/generated/Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid == 0:
                writer.writerow(["0","icecream@tastes.good","pbkdf2:sha256:260000$1GvmeoAkcWb89TyU$5f711eafb243c1c1a884715dd9bd6d185f29ccd3dab59ad19cc201a7260091cb","Joey","Shmoey","420 Chapel Dr", "1000"])
            else:
                if uid % 10 == 0:
                    print(f'{uid}', end=' ', flush=True)
                profile = fake.profile()
                email = profile['mail']
                plain_password = f'pass{uid}'
                password = generate_password_hash(plain_password)
                name_components = profile['name'].split(' ')
                firstname = name_components[0]
                lastname = name_components[-1]
                address = profile['residence']
                balance = fake.random_int(min=0)
                writer.writerow([uid, email, password, firstname, lastname, address, balance])
        print(f'{num_users} generated')
    return

def gen_sellers(num_sellers):
    sellers = []
    with open('db/generated/Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        for uid in fake.random_elements(list(range(num_users)), length=num_sellers, unique=True):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            sellers.append(uid)
            writer.writerow([uid])
        print(f'{num_sellers} generated')
    return sellers

# determines which products are available
def get_available_products(num_products):
    available_pids = []
    for pid in range(num_products):
        if pid % 100 == 0:
            print(f'{pid}', end=' ', flush=True)
        available = fake.random_element(elements=('true', 'false'))
        if available == 'true':
            available_pids.append(pid)
    return available_pids

def gen_products(num_products, seller_pid, available_pids):
    #available_pids = []
    with open('db/generated/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        unavailable_pids = list(set(range(num_products)) - set(available_pids))
        unique_pid_available = {} # key: id, value: (pid, sid)
        unique_pid_unavailable = {} # key: id, value: (pid, sid)
        id = 0
        for pid in available_pids:
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            category = fake.random_element(elements=('toys', 'electronic', 'clothes', 'tools', 'food', 'beauty'))
            for sid in seller_pid[pid]: # for each seller that sells current pid
                description = fake.sentence(nb_words=15)[:-1]
                price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
                available = 'true'
                unique_pid_available[id] = (pid, sid)
                writer.writerow([id, pid, sid, name, category, description, price, available])
                id += 1 # id is unique, pid is not unique (multiple sellers can have same pid)
        for pid in unavailable_pids:
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            category = fake.random_element(elements=('toys', 'electronic', 'clothes', 'tools', 'food', 'beauty'))
            description = fake.sentence(nb_words=15)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            unique_pid_unavailable[id] = (pid, sid)
            available = 'false'
            writer.writerow([id, pid, sid, name, category, description, price, available])
            id += 1 # id is unique, pid is not unique (multiple sellers can have same pid)
        print(f'{id} product listings generated; {len(available_pids)} products available; {len(unavailable_pids)} products unavailable')
    return unique_pid_available, unique_pid_unavailable


def gen_purchases(purchases):
    with open('db/generated/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for p in purchases:
            writer.writerow(p)
        print(f'{len(purchases)} generated')
    return



# product, seller, buyer, time_purchased
def gen_orders(num_orders, num_users, unique_pid_available):
    with open('db/generated/Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        purchases = []
        purchase_id = 0
        available_unique_pids = list(unique_pid_available.keys())
        time_fulfilled = datetime.min 
        for oid in range(num_orders):
            if oid % 100 == 0:
                    print(f'{oid}', end=' ', flush=True)
            order_price = 0.0
            uid = random.choice(list(range(num_users)))
            order_fulfilled = 'false'
            num_purchases_per_order = random.randint(1, 10)
            time_purchased = fake.date_time()
            for purchase in range(num_purchases_per_order):
                if purchase_id % 100 == 0:
                    print(f'{purchase_id}', end=' ', flush=True)
                unique_pid = fake.random_element(available_unique_pids)
                # if (purchase_id) and unique_pid in purchases[purchase_id]:
                #     break # skip purchase if the product is already in this order
                sid = unique_pid_available[unique_pid][1]
                unit_price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
                qty = fake.random_int(min=1, max=20)
                purchase_fulfilled='false'
                purchases.append([purchase_id, uid, unique_pid, oid, qty, purchase_fulfilled, time_fulfilled, sid, unit_price])
                order_price += float(unit_price) * qty
                purchase_id += 1
            order_price = "{:.2f}".format(order_price)
            writer.writerow([oid, uid, order_fulfilled, time_purchased, order_price])
    return purchases


def gen_cart(unique_pid_available):
    with open('db/generated/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        unique_available_pids = list(unique_pid_available.keys())
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            for pid in fake.random_elements(unique_available_pids, length=fake.random_int(min=1, max=10), unique=True):
                qty = fake.random_int(min=1, max=20)
                writer.writerow([uid, pid, qty])
    return

def gen_reviews(num_products, unique_pid_available, num_purchases):
    # available_pids = []
    unique_available_pids = list(unique_pid_available.keys())
    with open('db/generated/Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product Reviews...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            review_text = fake.sentence(nb_words=15)[:-1]
            pid = fake.random_element(elements=unique_available_pids)
            time_purchased = fake.date_time()
            rating = fake.random_int(min=1,max=5)
            writer.writerow([id, uid, pid, time_purchased, rating, review_text])
        # print(f'{num_products} generated; {len(unique_available_pids)} available')
    return

def gen_sellerReviews(num_users, sellers):
    # available_pids = []
    with open('db/generated/SellerReviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Seller Reviews...', end=' ', flush=True)
        for id in range(num_users):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_element(elements=sellers)
            while sid == uid:
                uid = fake.random_int(min=0, max=num_users-1)
            review_text = fake.sentence(nb_words=15)[:-1]
            time_posted = fake.date_time()
            rating = fake.random_int(min=1,max=5)
            writer.writerow([id, uid, sid, time_posted, rating, review_text])
        # print(f'{num_products} generated; {len(available_pids)} available')
    return    

# function that assigns sellers to available pids
def get_seller_to_pid(available_pids, sellers): #### use all pids, not just available_pids
    seller_pid = {} # dictionary with key:pid and value:list of sids that sell pid
    for pid in available_pids:
        seller_pid[pid] = [] # all sellers who have this pid in inventory
        num_sellers = random.randint(1,9)  # number of sellers who have this same pid in inventory
        #seller_pid = [] # all sellers who have this pid in inventory
        for i in range(num_sellers):
            sid = random.choice(sellers)
            if sid not in seller_pid[pid]: # prevents duplicate sid/pid pairing
                seller_pid[pid].append(sid)
    return seller_pid

# inventory needs products to set unavailable pids to qty = 0
def gen_inventory(unique_pid_available, unique_pid_unavailable):
    #sellers = [] #contains sid/uid of sellers
    #seller_pid = {} # dictionary with key:pid and value:list of sids that sell pid
    with open('db/generated/Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True) 
        id = 0
        for unique_pid in unique_pid_available.keys():
            sid = unique_pid_available[unique_pid][1]
            qty = random.choice([1,1,1,10,10,10,20,20,30,50,70,100]) + random.randint(1,9)
            writer.writerow([id, sid, unique_pid, qty])
            id += 1
                
        for unique_pid in unique_pid_unavailable.keys():
            sid = unique_pid_unavailable[unique_pid][1]
            qty = 0
            writer.writerow([id, sid, unique_pid, qty])
            id += 1
        print(f'{id} entries generated')
    return

gen_users(num_users)
sellers = gen_sellers(num_sellers)
available_pids = get_available_products(num_products)
seller_pid = get_seller_to_pid(available_pids, sellers)
unique_pid_available, unique_pid_unavailable = gen_products(num_products, seller_pid, available_pids)
gen_inventory(unique_pid_available, unique_pid_unavailable)

purchases = gen_orders(num_orders, num_users, unique_pid_available)
num_purchases = len(purchases)
gen_purchases(purchases)

gen_cart(unique_pid_available)
gen_reviews(num_products, unique_pid_available, num_purchases)
gen_sellerReviews(num_users, sellers)

print('DONE!!!')