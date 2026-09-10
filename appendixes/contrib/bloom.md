## F.6. bloom — Bloom 篩選器索引存取方法 [#](#BLOOM)

[F.6.1. 參數](bloom.md#BLOOM-PARAMETERS)

[F.6.2. 範例](bloom.md#BLOOM-EXAMPLES)

[F.6.3. 運算子類別介面](bloom.md#BLOOM-OPERATOR-CLASS-INTERFACE)

[F.6.4. 限制](bloom.md#BLOOM-LIMITATIONS)

[F.6.5. 作者](bloom.md#BLOOM-AUTHORS)

<a id="id-1.11.7.16.2"></a>

`bloom` 提供以 [Bloom 篩選器](https://en.wikipedia.org/wiki/Bloom_filter)為基礎的索引存取方法。

Bloom 篩選器是用於測試元素是否為集合成員的空間效率資料結構。用於索引存取方法時，它會透過建立索引時決定大小的簽章，快速排除不相符的 tuple。

簽章是已建立索引屬性的有損表示法，因此容易產生誤判；也就是說，可能會回報元素在集合中，但實際並非如此。因此，索引搜尋結果必須一律使用堆積項目中的實際屬性值重新檢查。較大的簽章可降低誤判機率，進而減少無用的堆積存取次數，但也會使索引更大、掃描速度更慢。

當資料表有許多屬性且查詢測試其任意組合時，此類索引最有用。傳統 btree 索引比 bloom 索引快，但要支援所有可能的查詢，可能需要許多 btree 索引，而只需單一 bloom 索引即可。請注意，bloom 索引只支援等值查詢；btree 索引還可進行不等式與範圍搜尋。

<a id="BLOOM-PARAMETERS"></a>

### F.6.1. 參數 [#](#BLOOM-PARAMETERS)

`bloom` 索引在其 `WITH` 子句中接受下列參數：

`length`
:   每個簽章（索引項目）的長度，單位為位元。會向上取整至最接近的 `16` 倍數。預設為 `80` 位元，最大為 `4096`。

`col1 — col32`
:   為每個索引欄位產生的位元數。每個參數名稱都指向其控制的索引欄位編號。預設為 `2` 位元，最大為 `4095`。實際未使用的索引欄位參數會被忽略。

<a id="BLOOM-EXAMPLES"></a>

### F.6.2. 範例 [#](#BLOOM-EXAMPLES)

以下是建立 bloom 索引的範例：

```

CREATE INDEX bloomidx ON tbloom USING bloom (i1,i2,i3)
       WITH (length=80, col1=2, col2=2, col3=4);
```

此索引的簽章長度為 80 位元，屬性 i1 與 i2 各對應至 2 位元，屬性 i3 對應至 4 位元。可省略 `length`、`col1` 與 `col2` 規格，因為它們使用預設值。

以下是更完整的 bloom 索引定義與使用範例，並與等效 btree 索引比較。bloom 索引遠小於 btree 索引，且效能可能更好。

```

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
```

對此大型資料表進行循序掃描需要很長時間：

```

=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------------
 Seq Scan on tbloom  (cost=0.00..213744.00 rows=250 width=24) (actual time=357.059..357.059 rows=0.00 loops=1)
   Filter: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Filter: 10000000
   Buffers: shared hit=63744
 Planning Time: 0.346 ms
 Execution Time: 357.076 ms
(6 rows)
```

即使已定義 btree 索引，結果仍會是循序掃描：

```

=# CREATE INDEX btreeidx ON tbloom (i1, i2, i3, i4, i5, i6);
CREATE INDEX
=# SELECT pg_size_pretty(pg_relation_size('btreeidx'));
 pg_size_pretty
----------------
 386 MB
(1 row)
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                              QUERY PLAN
-------------------------------------------------------------------​-----------------------------------
 Seq Scan on tbloom  (cost=0.00..213744.00 rows=2 width=24) (actual time=351.016..351.017 rows=0.00 loops=1)
   Filter: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Filter: 10000000
   Buffers: shared hit=63744
 Planning Time: 0.138 ms
 Execution Time: 351.035 ms
(6 rows)
```

在資料表上定義 bloom 索引，處理此類搜尋時比 btree 更好：

```

=# CREATE INDEX bloomidx ON tbloom USING bloom (i1, i2, i3, i4, i5, i6);
CREATE INDEX
=# SELECT pg_size_pretty(pg_relation_size('bloomidx'));
 pg_size_pretty
----------------
 153 MB
(1 row)
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                     QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------
 Bitmap Heap Scan on tbloom  (cost=1792.00..1799.69 rows=2 width=24) (actual time=22.605..22.606 rows=0.00 loops=1)
   Recheck Cond: ((i2 = 898732) AND (i5 = 123451))
   Rows Removed by Index Recheck: 2300
   Heap Blocks: exact=2256
   Buffers: shared hit=21864
   ->  Bitmap Index Scan on bloomidx  (cost=0.00..178436.00 rows=1 width=0) (actual time=20.005..20.005 rows=2300.00 loops=1)
         Index Cond: ((i2 = 898732) AND (i5 = 123451))
         Index Searches: 1
         Buffers: shared hit=19608
 Planning Time: 0.099 ms
 Execution Time: 22.632 ms
(11 rows)
```

現在，btree 搜尋的主要問題在於，搜尋條件未限制前導索引欄位時，btree 效率不佳。對 btree 而言，更好的策略是為每個欄位建立獨立索引。規劃器接著會選擇如下的計畫：

```

=# CREATE INDEX btreeidx1 ON tbloom (i1);
CREATE INDEX
=# CREATE INDEX btreeidx2 ON tbloom (i2);
CREATE INDEX
=# CREATE INDEX btreeidx3 ON tbloom (i3);
CREATE INDEX
=# CREATE INDEX btreeidx4 ON tbloom (i4);
CREATE INDEX
=# CREATE INDEX btreeidx5 ON tbloom (i5);
CREATE INDEX
=# CREATE INDEX btreeidx6 ON tbloom (i6);
CREATE INDEX
=# EXPLAIN ANALYZE SELECT * FROM tbloom WHERE i2 = 898732 AND i5 = 123451;
                                                        QUERY PLAN
-------------------------------------------------------------------​--------------------------------------------------------
 Bitmap Heap Scan on tbloom  (cost=9.29..13.30 rows=1 width=24) (actual time=0.032..0.033 rows=0.00 loops=1)
   Recheck Cond: ((i5 = 123451) AND (i2 = 898732))
   Buffers: shared read=6
   ->  BitmapAnd  (cost=9.29..9.29 rows=1 width=0) (actual time=0.047..0.047 rows=0.00 loops=1)
         Buffers: shared hit=6
         ->  Bitmap Index Scan on btreeidx5  (cost=0.00..4.52 rows=11 width=0) (actual time=0.026..0.026 rows=7.00 loops=1)
               Index Cond: (i5 = 123451)
               Index Searches: 1
               Buffers: shared hit=3
         ->  Bitmap Index Scan on btreeidx2  (cost=0.00..4.52 rows=11 width=0) (actual time=0.007..0.007 rows=8.00 loops=1)
               Index Cond: (i2 = 898732)
               Index Searches: 1
               Buffers: shared hit=3
 Planning Time: 0.264 ms
 Execution Time: 0.047 ms
(15 rows)
```

雖然此查詢執行速度遠快於使用任一單一索引，但索引大小會付出代價。每個單欄位 btree 索引占用 88.5 MB，因此總共需要 531 MB，是 bloom 索引所用空間的三倍以上。

<a id="BLOOM-OPERATOR-CLASS-INTERFACE"></a>

### F.6.3. 運算子類別介面 [#](#BLOOM-OPERATOR-CLASS-INTERFACE)

bloom 索引的運算子類別只需要已建立索引資料型別的雜湊函式，以及用於搜尋的等值運算子。此範例顯示 `text` 資料型別的運算子類別定義：

```

CREATE OPERATOR CLASS text_ops
DEFAULT FOR TYPE text USING bloom AS
    OPERATOR    1   =(text, text),
    FUNCTION    1   hashtext(text);
```

<a id="BLOOM-LIMITATIONS"></a>

### F.6.4. 限制 [#](#BLOOM-LIMITATIONS)

* 模組只包括 `int4` 與 `text` 的運算子類別。
* 搜尋只支援 `=` 運算子，但未來可能新增使用聯集與交集運算的陣列支援。
* `bloom` 存取方法不支援 `UNIQUE` 索引。
* `bloom` 存取方法不支援搜尋 `NULL` 值。

<a id="BLOOM-AUTHORS"></a>

### F.6.5. 作者 [#](#BLOOM-AUTHORS)

Teodor Sigaev `<teodor@postgrespro.ru>`,
俄羅斯莫斯科 Postgres Professional

Alexander Korotkov `<a.korotkov@postgrespro.ru>`,
俄羅斯莫斯科 Postgres Professional

Oleg Bartunov `<obartunov@postgrespro.ru>`,
俄羅斯莫斯科 Postgres Professional

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/bloom.html)
