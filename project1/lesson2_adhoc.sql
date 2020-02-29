create table if not exists transactions2 (transaction_id int, \
                                          customer_name text, \
                                          cashier_id text, \
                                          year int);

create table if not exists albums_sold (album_id int,
                                        transaction_id int,
                                        album_name text);

create table if not exists employees (employee_id int, \
                                      employee_name text);

create table if not exists sales (transaction_id int, \
                                  amount_spent int);

select t.transaction_id, t,customer_name, e.employee_name, t.year, a.album_name, s.amount_spent \
from transactions2 t join albums_sold a \
    on t.transaction_id = a.transaction_id \
    join employees e \
    on t.cashier_id = e.employee_id \
    join sales s \
    on t.transaction_id = s.transaction_id

create table if not exists transactions (transaction_id int, \
                                         customer_name text, \
                                         cashier_name text, \
                                         year int, \
                                         amount_spent int);

transaction_id, customer_name, cashier_name, year, amount_spent

create table if not exists cashier_sales (transaction_id int, \
                                          cashier_name text, \
                                          cashier_id int, \
                                          amount_spent int);

transaction_id, cashier_name, cashier_id, amount_spent


