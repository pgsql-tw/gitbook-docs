<a id="PGFREESPACEMAP"></a>

# F.29. pg_freespacemap

[F.29.1. Functions](#id-1.11.7.38.5)

[F.29.2. Sample Output](#id-1.11.7.38.6)

[F.29.3. Author](#id-1.11.7.38.7)

<a id="id-1.11.7.38.2"></a>

The `pg_freespacemap` module provides a means for examining the [free space map](../../internals/database-physical-storage/free-space-map.md) (FSM). It provides a function called `pg_freespace`, or two overloaded functions, to be precise. The functions show the value recorded in the free space map for a given page, or for all pages in the relation.

By default use is restricted to superusers and roles with privileges of the `pg_stat_scan_tables` role. Access may be granted to others using `GRANT`.

<a id="id-1.11.7.38.5"></a>

## F.29.1. Functions

`pg_freespace(rel regclass IN, blkno bigint IN) returns int2` <a id="id-1.11.7.38.5.2.1.1.2"></a>

Returns the amount of free space on the page of the relation, specified by `blkno`, according to the FSM.

`pg_freespace(rel regclass IN, blkno OUT bigint, avail OUT int2)`

Displays the amount of free space on each page of the relation, according to the FSM. A set of `(blkno bigint, avail int2)` tuples is returned, one tuple for each page in the relation.

The values stored in the free space map are not exact. They're rounded to precision of 1/256th of `BLCKSZ` (32 bytes with default `BLCKSZ`), and they're not kept fully up-to-date as tuples are inserted and updated.

For indexes, what is tracked is entirely-unused pages, rather than free space within pages. Therefore, the values are not meaningful, just whether a page is in-use or empty.

<a id="id-1.11.7.38.6"></a>

## F.29.2. Sample Output

```

postgres=# SELECT * FROM pg_freespace('foo');
 blkno | avail
-------+-------
     0 |     0
     1 |     0
     2 |     0
     3 |    32
     4 |   704
     5 |   704
     6 |   704
     7 |  1216
     8 |   704
     9 |   704
    10 |   704
    11 |   704
    12 |   704
    13 |   704
    14 |   704
    15 |   704
    16 |   704
    17 |   704
    18 |   704
    19 |  3648
(20 rows)

postgres=# SELECT * FROM pg_freespace('foo', 7);
 pg_freespace
--------------
         1216
(1 row)
```

<a id="id-1.11.7.38.7"></a>

## F.29.3. Author

Original version by Mark Kirkwood <code class="email">&lt;<a class="email" href="mailto:markir@paradise.net.nz">markir@paradise.net.nz</a>&gt;</code>. Rewritten in version 8.4 to suit new FSM implementation by Heikki Linnakangas <code class="email">&lt;<a class="email" href="mailto:heikki@enterprisedb.com">heikki@enterprisedb.com</a>&gt;</code>

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/pgfreespacemap.html)（英文原文，待翻譯）
