# Memos for Project 3: dwh on cloud

amazon redshift を使うらしい

### l1 e1 step 3

- film
  - film_id, title, year

##### 1

```sql
select
    f.title,
    sum(p.amount) revenue
from payment p
    join rental r
        on p.rental_id = r.rental_id
    join inventory i
        on r.inventory_id = i.inventory_id
    join film f
        on i.film_id = f.film_id
group by f.title
order by revenue desc
limit 10;
```

##### 2

```sql
select
    c.city,
    sum(p.amount) revenue
from payment p
    join customer u
        on p.customer_id = u.customer_id
    join address a
        on u.address_id = a.address_id
    join city c
        on a.city_id = c.city_id
group by c.city
order by revenue desc
limit 10;
```

##### 3

```sql
select
    f.title,
    ci.city,
    extract(month from p.payment_date) as month,
    sum(p.amount) revenue
from payment p
    join rental r
        on ( p.rental_id = r.rental_id )
    join inventory i
        on ( r.inventory_id = i.inventory_id )
    join film f
        on ( i.film_id = f.film_id)
    join customer c
        on ( p.customer_id = c.customer_id )
    join address a
        on ( c.address_id = a.address_id )
    join city ci
        on ( a.city_id = ci.city_id )
group by f.title, ci.city, month
order by month, revenue desc
limit 10;
```

### 最初の方はPostgreSQLを使ったETLの話
つまらん


# eof
