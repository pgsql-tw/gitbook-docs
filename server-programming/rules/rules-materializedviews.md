<a id="RULES-MATERIALIZEDVIEWS"></a>

## 39.3. 具體化檢視表 [#](#RULES-MATERIALIZEDVIEWS)

<a id="id-1.8.6.8.2"></a><a id="id-1.8.6.8.3"></a><a id="id-1.8.6.8.4"></a>

PostgreSQL 中的具體化檢視表像檢視表一樣使用規則系統，但會把結果以類似資料表的形式保存下來。下面兩者：

```

CREATE MATERIALIZED VIEW mymatview AS SELECT * FROM mytab;
```

以及：

```

CREATE TABLE mymatview AS SELECT * FROM mytab;
```

之間的主要差異在於，具體化檢視表之後無法直接被更新，而且用來建立具體化檢視表的那個查詢，是以與檢視表的查詢完全相同的方式儲存，因此可以用下列指令為具體化檢視表產生新的資料：

```

REFRESH MATERIALIZED VIEW mymatview;
```

在 PostgreSQL 系統目錄中，關於具體化檢視表的資訊和資料表或檢視表的資訊完全相同。所以對剖析器而言，具體化檢視表就是一個關聯，就像資料表或檢視表一樣。當查詢中參照到具體化檢視表時，資料會像從資料表取得那樣直接從具體化檢視表回傳；規則只用於填入具體化檢視表的內容。

雖然存取具體化檢視表中所儲存的資料，通常比直接存取底層資料表或透過檢視表存取要快上許多，但這些資料不見得是最新的；不過有時候並不需要最新的資料。考慮一個記錄銷售的資料表：

```

CREATE TABLE invoice (
    invoice_no    integer        PRIMARY KEY,
    seller_no     integer,       -- ID of salesperson
    invoice_date  date,          -- date of sale
    invoice_amt   numeric(13,2)  -- amount of sale
);
```

如果人們希望能夠快速地繪製歷史銷售資料的圖表，他們可能會想要做彙總，而且可能不在意當天尚未完整的資料：

```

CREATE MATERIALIZED VIEW sales_summary AS
  SELECT
      seller_no,
      invoice_date,
      sum(invoice_amt)::numeric(13,2) as sales_amt
    FROM invoice
    WHERE invoice_date < CURRENT_DATE
    GROUP BY
      seller_no,
      invoice_date;

CREATE UNIQUE INDEX sales_summary_seller
  ON sales_summary (seller_no, invoice_date);
```

這個具體化檢視表對於在為業務人員建立的儀表板中顯示圖表可能很有用。可以排程一個工作，在每天晚上用這個 SQL 陳述式來更新統計資料：

```

REFRESH MATERIALIZED VIEW sales_summary;
```

具體化檢視表的另一個用途，是讓透過 foreign data wrapper 從遠端系統取得的資料能夠被更快速地存取。下面是一個使用 `file_fdw` 的簡單範例，並附上執行時間；但由於這是使用本機系統上的快取，實際上和存取遠端系統相比，效能差異通常會比這裡所顯示的更大。請注意，我們同時也利用了可以在具體化檢視表上建立索引的能力，而 `file_fdw` 並不支援索引；這項優勢對於其他種類的外部資料存取可能就不適用了。

設定：

```

CREATE EXTENSION file_fdw;
CREATE SERVER local_file FOREIGN DATA WRAPPER file_fdw;
CREATE FOREIGN TABLE words (word text NOT NULL)
  SERVER local_file
  OPTIONS (filename '/usr/share/dict/words');
CREATE MATERIALIZED VIEW wrd AS SELECT * FROM words;
CREATE UNIQUE INDEX wrd_word ON wrd (word);
CREATE EXTENSION pg_trgm;
CREATE INDEX wrd_trgm ON wrd USING gist (word gist_trgm_ops);
VACUUM ANALYZE wrd;
```

現在我們來拼字檢查一個單字。直接使用 `file_fdw`：

```

SELECT count(*) FROM words WHERE word = 'caterpiler';

 count
-------
     0
(1 row)
```

使用 `EXPLAIN ANALYZE`，我們可以看到：

```

 Aggregate  (cost=21763.99..21764.00 rows=1 width=0) (actual time=188.180..188.181 rows=1.00 loops=1)
   ->  Foreign Scan on words  (cost=0.00..21761.41 rows=1032 width=0) (actual time=188.177..188.177 rows=0.00 loops=1)
         Filter: (word = 'caterpiler'::text)
         Rows Removed by Filter: 479829
         Foreign File: /usr/share/dict/words
         Foreign File Size: 4953699
 Planning time: 0.118 ms
 Execution time: 188.273 ms
```

如果改用具體化檢視表，這個查詢就快得多：

```

 Aggregate  (cost=4.44..4.45 rows=1 width=0) (actual time=0.042..0.042 rows=1.00 loops=1)
   ->  Index Only Scan using wrd_word on wrd  (cost=0.42..4.44 rows=1 width=0) (actual time=0.039..0.039 rows=0.00 loops=1)
         Index Cond: (word = 'caterpiler'::text)
         Heap Fetches: 0
         Index Searches: 1
 Planning time: 0.164 ms
 Execution time: 0.117 ms
```

不論用哪一種方式，這個單字都拼錯了，所以讓我們來找找我們原本可能想要輸入的字。同樣先使用 `file_fdw` 與 `pg_trgm`：

```

SELECT word FROM words ORDER BY word <-> 'caterpiler' LIMIT 10;

     word
---------------
 cater
 caterpillar
 Caterpillar
 caterpillars
 caterpillar's
 Caterpillar's
 caterer
 caterer's
 caters
 catered
(10 rows)
```

```

 Limit  (cost=11583.61..11583.64 rows=10 width=32) (actual time=1431.591..1431.594 rows=10.00 loops=1)
   ->  Sort  (cost=11583.61..11804.76 rows=88459 width=32) (actual time=1431.589..1431.591 rows=10.00 loops=1)
         Sort Key: ((word <-> 'caterpiler'::text))
         Sort Method: top-N heapsort  Memory: 25kB
         ->  Foreign Scan on words  (cost=0.00..9672.05 rows=88459 width=32) (actual time=0.057..1286.455 rows=479829.00 loops=1)
               Foreign File: /usr/share/dict/words
               Foreign File Size: 4953699
 Planning time: 0.128 ms
 Execution time: 1431.679 ms
```

使用具體化檢視表：

```

 Limit  (cost=0.29..1.06 rows=10 width=10) (actual time=187.222..188.257 rows=10.00 loops=1)
   ->  Index Scan using wrd_trgm on wrd  (cost=0.29..37020.87 rows=479829 width=10) (actual time=187.219..188.252 rows=10.00 loops=1)
         Order By: (word <-> 'caterpiler'::text)
         Index Searches: 1
 Planning time: 0.196 ms
 Execution time: 198.640 ms
```

如果你可以容忍以週期性的方式把遠端資料更新到本機資料庫，效能上的好處可能相當可觀。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/rules-materializedviews.html)（原文版本：18.6；核對日期：2026-09-13）
