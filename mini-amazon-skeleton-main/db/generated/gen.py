from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random

num_users = 100
num_products = 2000
num_purchases = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('db/generated/Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
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
            writer.writerow([uid, email, password, firstname, lastname, address])
        print(f'{num_users} generated')
    return


def gen_products(num_products):
    available_pids = []
    with open('db/generated/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(num_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            name = fake.sentence(nb_words=4)[:-1]
            category = fake.random_element(elements=('toys', 'electronic', 'clothes', 'tools'))
            description = fake.sentence(nb_words=15)[:-1]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            available = fake.random_element(elements=('true', 'false'))
            if available == 'true':
                available_pids.append(pid)
            writer.writerow([pid, name, category, description, price, available])
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    with open('db/generated/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=available_pids, unique = True)
            time_purchased = fake.date_time()
            writer.writerow([id, uid, pid, time_purchased])
        print(f'{num_purchases} generated')
    return

def gen_cart(available_pids):
    with open('db/generated/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            for pid in fake.random_elements(available_pids, length=fake.random_int(min=1, max=30), unique=True):
                qty = fake.random_int(min=1, max=20)
                writer.writerow([uid, pid, qty])
    return

# def gen_reviews():

def gen_inventory(num_users, available_pids):
    sellers = [] #contains sid/uid of sellers
    with open('db/generated/Inventory.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        for uid in range(num_users):
            if random.randint(1,5) == 5: # 20% chance that a user is also seller
                sellers.append(uid)
        id = 0
        for pid in available_pids:
            num_sellers = random.randint(1,9)  # number of sellers who have this same pid in inventory
            seller_pid = [] # all sellers who have this pid in inventory
            for i in range(num_sellers):
                if id % 200 == 0:
                    print(f'{id}', end=' ', flush=True)
                sid = random.choice(sellers)
                if sid not in seller_pid: # prevents duplicate sid/pid pairing
                    seller_pid.append(sid)
                    qty = random.choice([1,1,1,10,10,10,20,20,30,50,70,100]) + random.randint(1,9)
                    writer.writerow([id, sid, pid, qty])
                    id += 1
        print(f'{id} entries generated')
    return

gen_users(num_users)
available_pids = gen_products(num_products)
gen_purchases(num_purchases, available_pids)
gen_cart(available_pids)
gen_inventory(num_users, available_pids)