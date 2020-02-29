--
cur.execute("create table if not exists transactions (\
    customer_id int, \
    store_id int, \
    spent double precision);")

cur.execute("insert into transactions \
    (customer_id, store_id, spent) \
    values (%s, %s, %s)",
    (1, 1, 20.50))

cur.execute("insert into transactions \
    (customer_id, store_id, spent) \
    values (%s, %s, %s)",
    (2, 1, 35.21))

--
cur.execute("create table if not exists customer (\
    customer_id int, \
    name text, \
    rewards char(1));")

cur.execute("insert into customer \
    (customer_id, name, rewards) \
    values (%s, %s, %s);",
    (1, "Amanda", "Y"))

cur.execute("insert into customer \
    (customer_id, name, rewards) \
    values (%s, %s, %s);",
    (2, "Toby", "N"))

cur.execute("create table if not exists item_purchased (\
    customer_id int, \
    item_number int, \
    item_name text);")

cur.execute("insert into item_purchased \
    (customer_id, item_number, item_name) \
    values (%s, %s, %s);",
    (1, 1, "Rubber Soul"))

cur.execute("insert into item_purchased \
    (customer_id, item_number, item_name) \
    values (%s, %s, %s);",
    (2, 3, "Let It Be"))

cur.execute("create table if not exists store (\
    store_id int, \
    state text);")

cur.execute("insert into store \
    (store_id, state) \
    values (%s, %s)",
    (1, "CA"))

cur.execute("insert into store \
    (store_id, state) \
    values (%s, %s)",
    (2, "WA"))

--
"select t.customer_id, cus.name, spent, state, item_name, rewards \
    from transactions t \
    join customer cus \
        on t.customer_id = cus.customer_id \
    join item_purchased i \
        on t.customer_id = i.customer_id \
    join store s \
        on t.store_id = s.store_id \
    where spent > 30"

--
"select customer_id, name, sum(spent) as total \
from transactions t \
    join customer cus \
        on t.customer_id = cus.customer_id \
where customer_id = 2 \
group by customer_id, name"



