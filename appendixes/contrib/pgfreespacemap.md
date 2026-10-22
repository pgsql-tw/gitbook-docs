<a id="PGFREESPACEMAP"></a>

## F.27. pg_freespacemap — 檢視可用空間對應表 [#](#PGFREESPACEMAP)

[F.27.1. 函式](pgfreespacemap.md#PGFREESPACEMAP-FUNCS)

[F.27.2. 輸出範例](pgfreespacemap.md#PGFREESPACEMAP-SAMPLE-OUTPUT)

[F.27.3. 作者](pgfreespacemap.md#PGFREESPACEMAP-AUTHOR)

<a id="id-1.11.7.37.2"></a>

`pg_freespacemap` 模組提供檢視[可用空間對應表](../../internals/storage/storage-fsm.md)（FSM）的方法。它提供一個名為 `pg_freespace` 的函式，精確地說，是兩個多載函式。這些函式會顯示可用空間對應表中為指定頁面或為關聯中所有頁面所記錄的值。

預設情況下，只有超級使用者與具有 `pg_stat_scan_tables` 角色權限的角色可以使用。可以使用 `GRANT` 將存取權授與其他人。

<a id="PGFREESPACEMAP-FUNCS"></a>

### F.27.1. 函式 [#](#PGFREESPACEMAP-FUNCS)

`pg_freespace(rel regclass IN, blkno bigint IN) returns int2` <a id="id-1.11.7.37.5.2.1.1.2"></a>
:   依據 FSM，傳回關聯中由 `blkno` 指定之頁面上的可用空間量。

`pg_freespace(rel regclass IN, blkno OUT bigint, avail OUT int2)`
:   依據 FSM，顯示關聯中每個頁面上的可用空間量。傳回一組
    `(blkno bigint, avail int2)`
    元組，關聯中的每個頁面各對應一個元組。

可用空間對應表中儲存的值並不精確。這些值會捨入到 `BLCKSZ` 的 1/256 精度（使用預設的 `BLCKSZ` 時為 32 位元組），而且在插入與更新元組時，這些值不會隨時保持完全最新。

對索引而言，所追蹤的是完全未使用的頁面，而不是頁面內的可用空間。因此，這些值本身沒有意義，只表示頁面是使用中還是空的。

<a id="PGFREESPACEMAP-SAMPLE-OUTPUT"></a>

### F.27.2. 輸出範例 [#](#PGFREESPACEMAP-SAMPLE-OUTPUT)

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

<a id="PGFREESPACEMAP-AUTHOR"></a>

### F.27.3. 作者 [#](#PGFREESPACEMAP-AUTHOR)

原始版本由 Mark Kirkwood `<markir@paradise.net.nz>` 撰寫。
於 8.4 版由 Heikki Linnakangas `<heikki@enterprisedb.com>` 改寫，以配合新的 FSM 實作。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/pgfreespacemap.html)（原文版本：18.6；核對日期：2026-10-23）
