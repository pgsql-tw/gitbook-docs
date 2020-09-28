# F.5. bloom

Bloom 提供了一種基於 [**Bloom fliters**](https://en.wikipedia.org/wiki/Bloom_filter) 索引方法。

Bloom filter 是一種節省空間的資料結構，用於測試元素是否為集合的成員。在使用索引方法時，它透過 signatures（其大小是在建立索引時確定的）快速排除不相符的內容。

Signature 是索引屬性的失真表示，因此很容易誤報。也就是說，可能會回報某個元素在集合中（實際上沒有）。因此，必須使用資料中的實際屬性值來重新檢查索引並搜尋結果。較大的 signature 會減少了誤報的機率，也減少了無效的存取次數，但當然也會使索引變大，造成掃描速度變慢。

當資料表具有許多屬性並且查詢測試它們的任意組合時，這種類型的索引最有用。傳統的 btree 索引會比 Bloom 索引快，但是它可能需要許多 btree 索引來支援所有可能的查詢，而其中一個查詢只需要一個 Bloom 索引。但是請注意，bloom 索引僅支援相等查詢，而 btree 索引也可以用於不相等和範圍查詢。

## F.5.1. 參數

Bloom 索引的 WITH 子句接受以下參數：

`length`

每個 signature（索引項目）的長度（以位元為單位）。四捨五入到最接近的 16 的倍數。預設值為 80 位元，最大值為 4096。

`col1 — col32`

每個索引欄位產成的位元數。每個參數的名稱指的是它控制的索引欄位的編號。預設值為 2 位元，最大值為 4095。實際未使用的索引欄位的參數將被忽略。

## F.5.2. Examples

This is an example of creating a bloom index:

```text
CREATE INDEX bloomidx ON tbloom USING bloom (i1,i2,i3)
       WITH (length=80, col1=2, col2=2, col3=4);
```

The index is created with a signature length of 80 bits, with attributes i1 and i2 mapped to 2 bits, and attribute i3 mapped to 4 bits. We could have omitted the `length`, `col1`, and `col2` specifications since those have the default values.

Here is a more complete example of bloom index definition and usage, as well as a comparison with equivalent btree indexes. The bloom index is considerably smaller than the btree index, and can perform better.

```text
=# CREATE TABLE tbloom AS
   SELECT
     (random() * 1000000)::int as i1,
     (random() * 1000000)::int as i2,
     (random() * 1000000)::int as i3,
     (random() * 1000000)::int as i4,
     (random() * 1000000)::int as i5,
     (random() * 1000000)::int as i6
   FROM
  generate_series(1,10000000);
SELECT 10000000
=# CREATE INDEX bloomidx ON tbloom USING bloom (i1, i2, i3, i4, i5, i6);
CREATE INDEX
=# SELECT pg_size_pretty(pg_relation_size('bloomidx'));
 pg_size_pretty
----------------
 153 MB
(1 row)
=# CREATE index btreeidx ON tbloom (i1, i2, i3, i4, i5, i6);
CREATE INDEX
=# SELECT pg_size_pretty(pg_relation_size('btreeidx'));
 pg_size_pretty
----------------
 387 MB
(1 row)
```

A sequential scan over this large table takes a long time:

```text
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                 QUERY PLAN
-------------------------------------------------------------------​-----------------------------------------
 Seq Scan on tbloom  (cost=0.00..213694.08 rows=1 width=24) (actual time=1445.438..1445.438 rows=0 loops=1)
   Filter: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Filter: 10000000
 Planning time: 0.177 ms
 Execution time: 1445.473 ms
(5 rows)
```

So the planner will usually select an index scan if possible. With a btree index, we get results like this:

```text
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                           QUERY PLAN
-------------------------------------------------------------------​-------------------------------------------------------------
 Index Only Scan using btreeidx on tbloom  (cost=0.56..298311.96 rows=1 width=24) (actual time=445.709..445.709 rows=0 loops=1)
   Index Cond: ((i2 = 898732) AND (i5 = 123451))
   Heap Fetches: 0
 Planning time: 0.193 ms
 Execution time: 445.770 ms
(5 rows)
```

Bloom is better than btree in handling this type of search:

```text
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                        QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------
 Bitmap Heap Scan on tbloom  (cost=178435.39..178439.41 rows=1 width=24) (actual time=76.698..76.698 rows=0 loops=1)
   Recheck Cond: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Index Recheck: 2439
   Heap Blocks: exact=2408
   ->  Bitmap Index Scan on bloomidx  (cost=0.00..178435.39 rows=1 width=0) (actual time=72.455..72.455 rows=2439 loops=1)
         Index Cond: ((i2 = 898732) AND (i5 = 123451))
 Planning time: 0.475 ms
 Execution time: 76.778 ms
(8 rows)
```

請注意，這裡的誤報的數量相對較多：被選擇 2439 筆資料要進行確認，但實際上沒有與查詢相符的資料。我們可以透過指定更大的 signature 長度來減少這種情況。在此範例中，建立長度為 200 的索引可將誤報數量減少到 55；但它也使索引大小增加了一倍（至 306 MB），並最終使該查詢的速度變慢（總計 125 毫秒）。

現在，btree 搜搜的主要問題在於，當搜搜條件不限制前導索引欄時，btree 的效率低下。btree 的更好策略是在每欄位上建立一個單獨的索引。然後計劃程序將會選擇規劃以下內容：

```text
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                          QUERY PLAN
-------------------------------------------------------------------​-----------------------------------------------------------
 Bitmap Heap Scan on tbloom  (cost=9.29..13.30 rows=1 width=24) (actual time=0.148..0.148 rows=0 loops=1)
   Recheck Cond: ((i5 = 123451) AND (i2 = 898732))
   ->  BitmapAnd  (cost=9.29..9.29 rows=1 width=0) (actual time=0.145..0.145 rows=0 loops=1)
         ->  Bitmap Index Scan on tbloom_i5_idx  (cost=0.00..4.52 rows=11 width=0) (actual time=0.089..0.089 rows=10 loops=1)
               Index Cond: (i5 = 123451)
         ->  Bitmap Index Scan on tbloom_i2_idx  (cost=0.00..4.52 rows=11 width=0) (actual time=0.048..0.048 rows=8 loops=1)
               Index Cond: (i2 = 898732)
 Planning time: 2.049 ms
 Execution time: 0.280 ms
(9 rows)
```

儘管此查詢的執行速度比使用單個索引的查詢快得多，但我們在索引大小上付出了很大的代價。每個單欄位 btree 索引佔用 214 MB，因此所需的總空間超過 1.2GB，是 Bloom 索引使用的空間 8 倍以上。

## F.5.3. Operator Class Interface

An operator class for bloom indexes requires only a hash function for the indexed data type and an equality operator for searching. This example shows the operator class definition for the `text` data type:

```text
CREATE OPERATOR CLASS text_ops
DEFAULT FOR TYPE text USING bloom AS
    OPERATOR    1   =(text, text),
    FUNCTION    1   hashtext(text);
```

## F.5.4. Limitations

* Only operator classes for `int4` and `text` are included with the module.
* Only the `=` operator is supported for search. But it is possible to add support for arrays with union and intersection operations in the future.
* `bloom` access method doesn't support `UNIQUE` indexes.
* `bloom` access method doesn't support searching for `NULL` values.

## F.5.5. Authors

Teodor Sigaev `<`[`teodor@postgrespro.ru`](mailto:teodor@postgrespro.ru)`>`, Postgres Professional, Moscow, Russia

Alexander Korotkov `<`[`a.korotkov@postgrespro.ru`](mailto:a.korotkov@postgrespro.ru)`>`, Postgres Professional, Moscow, Russia

Oleg Bartunov `<`[`obartunov@postgrespro.ru`](mailto:obartunov@postgrespro.ru)`>`, Postgres Professional, Moscow, Russia

