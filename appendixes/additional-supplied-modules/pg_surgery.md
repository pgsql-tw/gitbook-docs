<a id="PGSURGERY"></a>

# F.34. pg_surgery

[F.34.1. Functions](#id-1.11.7.43.4)

[F.34.2. Authors](#id-1.11.7.43.5)

<a id="id-1.11.7.43.2"></a>

The `pg_surgery` module provides various functions to perform surgery on a damaged relation. These functions are unsafe by design and using them may corrupt (or further corrupt) your database. For example, these functions can easily be used to make a table inconsistent with its own indexes, to cause `UNIQUE` or `FOREIGN KEY` constraint violations, or even to make tuples visible which, when read, will cause a database server crash. They should be used with great caution and only as a last resort.

<a id="id-1.11.7.43.4"></a>

## F.34.1. Functions

`heap_force_kill(regclass, tid[]) returns void`

`heap_force_kill` marks “used” line pointers as “dead” without examining the tuples. The intended use of this function is to forcibly remove tuples that are not otherwise accessible. For example:

```

test=> select * from t1 where ctid = '(0, 1)';
ERROR:  could not access status of transaction 4007513275
DETAIL:  Could not open file "pg_xact/0EED": No such file or directory.

test=# select heap_force_kill('t1'::regclass, ARRAY['(0, 1)']::tid[]);
 heap_force_kill
-----------------

(1 row)

test=# select * from t1 where ctid = '(0, 1)';
(0 rows)
```

`heap_force_freeze(regclass, tid[]) returns void`

`heap_force_freeze` marks tuples as frozen without examining the tuple data. The intended use of this function is to make accessible tuples which are inaccessible due to corrupted visibility information, or which prevent the table from being successfully vacuumed due to corrupted visibility information. For example:

```

test=> vacuum t1;
ERROR:  found xmin 507 from before relfrozenxid 515
CONTEXT:  while scanning block 0 of relation "public.t1"

test=# select ctid from t1 where xmin = 507;
 ctid
-------
 (0,3)
(1 row)

test=# select heap_force_freeze('t1'::regclass, ARRAY['(0, 3)']::tid[]);
 heap_force_freeze
-------------------

(1 row)

test=# select ctid from t1 where xmin = 2;
 ctid
-------
 (0,3)
(1 row)
```

<a id="id-1.11.7.43.5"></a>

## F.34.2. Authors

Ashutosh Sharma <code class="email">&lt;<a class="email" href="mailto:ashu.coek88@gmail.com">ashu.coek88@gmail.com</a>&gt;</code>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/pgsurgery.html)（英文原文，待翻譯）
