<a id="PGFREESPACEMAP"></a>

# F.29. pg_freespacemap

[F.29.1. 函式](#id-1.11.7.38.5)

[F.29.2. 輸出範例](#id-1.11.7.38.6)

[F.29.3. 作者](#id-1.11.7.38.7)

<a id="id-1.11.7.38.2"></a>

`pg_freespacemap` 模組提供檢視[可用空間對照表](../../internals/database-physical-storage/free-space-map.md)（FSM）的方式。更精確地說，它提供一個名為 `pg_freespace` 的函式，或者說兩個多載函式。這些函式顯示可用空間對照表中，指定頁面或關聯內所有頁面所記錄的值。

預設只有超級使用者與具有 `pg_stat_scan_tables` 角色權限的角色可以使用。可使用 `GRANT` 將存取權授與其他人。

<a id="id-1.11.7.38.5"></a>

## F.29.1. 函式

`pg_freespace(rel regclass IN, blkno bigint IN) returns int2` <a id="id-1.11.7.38.5.2.1.1.2"></a>

依據 FSM，傳回關聯中由 `blkno` 指定頁面的可用空間量。

`pg_freespace(rel regclass IN, blkno OUT bigint, avail OUT int2)`

依據 FSM，顯示關聯中每個頁面的可用空間量。傳回一組 `(blkno bigint, avail int2)` 資料列，關聯中的每個頁面各有一筆資料列。

可用空間對照表中儲存的值並不精確。它們會四捨五入至 `BLCKSZ` 的 1/256 精度（預設 `BLCKSZ` 時為 32 位元組），且不會隨著插入及更新資料列而完全維持最新狀態。

對索引而言，追蹤的是完全未使用的頁面，而不是頁面內的可用空間。因此，這些數值本身沒有意義，只表示頁面正在使用或為空。

<a id="id-1.11.7.38.6"></a>

## F.29.2. 輸出範例

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

## F.29.3. 作者

原始版本由 Mark Kirkwood <code class="email">&lt;<a class="email" href="mailto:markir@paradise.net.nz">markir@paradise.net.nz</a>&gt;</code> 撰寫。為配合新的 FSM 實作，Heikki Linnakangas <code class="email">&lt;<a class="email" href="mailto:heikki@enterprisedb.com">heikki@enterprisedb.com</a>&gt;</code> 在 8.4 版重寫。

---

原文：[PostgreSQL 15.19 Documentation](https://www.postgresql.org/docs/15/pgfreespacemap.html)
