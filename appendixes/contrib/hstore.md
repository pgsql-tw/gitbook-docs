<a id="HSTORE"></a>

## F.17. hstore — hstore 鍵／值資料型別 [#](#hstore) <a href="#hstore" id="hstore"></a>

[F.17.1. `hstore` 外部表示法](hstore.md#hstore-external-rep)

[F.17.2. `hstore` 運算子與函式](hstore/hstore-ops-funcs.md#hstore-ops-funcs)

[F.17.3. 索引](hstore.md#hstore-indexes)

[F.17.4. 範例](hstore.md#hstore-examples)

[F.17.5. 統計資訊](hstore.md#hstore-statistics)

[F.17.6. 相容性](hstore.md#hstore-compatibility)

[F.17.7. 轉換](hstore.md#hstore-transforms)

[F.17.8. 作者](hstore.md#hstore-authors)

<a id="id-1.11.7.27.2"></a>

此模組實作 `hstore` 資料型別，用於在單一 PostgreSQL 值中儲存一組鍵／值配對。它適用於多種情境，例如含有許多但很少查閱之屬性的資料列，或半結構化資料。鍵和值都只是文字字串。

此模組被視為「受信任」，亦即具有目前資料庫 `CREATE` 權限的非超級使用者可以安裝它。

<a id="HSTORE-EXTERNAL-REP"></a>

### F.17.1. `hstore` 外部表示法 [#](#hstore-external-rep) <a href="#hstore-external-rep" id="hstore-external-rep"></a>

`hstore` 用於輸入與輸出的文字表示法，包含零個或多個以逗號分隔的 *`key`* `=>` *`value`* 配對。範例：

```

k => v
foo => bar, baz => whatever
"1-a" => "anything at all"
```

配對順序並不重要（輸出時也可能不會重現）。配對之間或 `=>` 符號周圍的空白會被忽略。包含空白、逗號、`=` 或 `>` 的鍵和值必須以雙引號括住。若鍵或值中要包含雙引號或反斜線，請以反斜線逸出。

`hstore` 中的每個鍵都是唯一的。若宣告含有重複鍵的 `hstore`，只會有一個儲存在 `hstore` 中，且不保證會保留哪一個：

```

SELECT 'a=>1,a=>2'::hstore;
  hstore
----------
 "a"=>"1"
```

值（但鍵不可）可以是 SQL `NULL`。例如：

```

key => NULL
```

`NULL` 關鍵字不區分大小寫。以雙引號括住 `NULL`，即可將其視為一般字串「NULL」。

### 注意

請記得，作為輸入使用時，`hstore` 文字格式會在任何必要的引號或逸出處理*之前*套用。若透過參數傳遞 `hstore` 字面值，則不需要額外處理。但若將它作為帶引號的字面常數傳遞，則任何單引號字元及（依 `standard_conforming_strings` 組態參數的設定而定）反斜線字元，都必須正確逸出。關於字串常數的處理，請參閱[第 4.1.2.1 節](../../the-sql-language/sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-STRINGS)。

輸出時，鍵和值一律會以雙引號括住，即使嚴格而言並非必要。

### F.17.2. `hstore` 運算子與函式 [#](#hstore-ops-funcs) <a href="#hstore-ops-funcs" id="hstore-ops-funcs"></a>

完整內容請見 [F.17.2. hstore 運算子與函式](hstore/hstore-ops-funcs.md#hstore-ops-funcs)。

<a id="HSTORE-INDEXES"></a>

### F.17.3. 索引 [#](#hstore-indexes) <a href="#hstore-indexes" id="hstore-indexes"></a>

`hstore` 對 `@>`、`?`、`?&` 與 `?|` 運算子支援 GiST 與 GIN 索引。例如：

```

CREATE INDEX hidx ON testhstore USING GIST (h);

CREATE INDEX hidx ON testhstore USING GIN (h);
```

`gist_hstore_ops` GiST 運算子類別會將一組鍵／值配對近似為點陣圖簽章。其可選整數參數 `siglen` 決定簽章長度（以位元組計）。預設長度為 16 位元組。有效的簽章長度介於 1 至 2024 位元組之間。較長的簽章可帶來更精確的搜尋（掃描較小比例的索引與較少的堆積頁面），代價是索引較大。

以下範例建立簽章長度為 32 位元組的此類索引：

```

CREATE INDEX hidx ON testhstore USING GIST (h gist_hstore_ops(siglen=32));
```

`hstore` 也支援 `=` 運算子的 `btree` 或 `hash` 索引。這讓 `hstore` 欄位可宣告為 `UNIQUE`，或用於 `GROUP BY`、`ORDER BY` 或 `DISTINCT` 表達式。`hstore` 值的排序順序不特別實用，但這些索引可能適合等值查找。請如下為 `=` 比較建立索引：

```

CREATE INDEX hidx ON testhstore USING BTREE (h);

CREATE INDEX hidx ON testhstore USING HASH (h);
```

<a id="HSTORE-EXAMPLES"></a>

### F.17.4. 範例 [#](#hstore-examples) <a href="#hstore-examples" id="hstore-examples"></a>

新增一個鍵，或以新值更新現有鍵：

```

UPDATE tab SET h['c'] = '3';
```

另一種執行相同工作的方式是：

```

UPDATE tab SET h = h || hstore('c', '3');
```

若要在一次操作中新增或變更多個鍵，串接方式比使用下標更有效率：

```

UPDATE tab SET h = h || hstore(array['q', 'w'], array['11', '12']);
```

刪除一個鍵：

```

UPDATE tab SET h = delete(h, 'k1');
```

將 `record` 轉換為 `hstore`：

```

CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT hstore(t) FROM test AS t;
                   hstore
---------------------------------------------
 "col1"=>"123", "col2"=>"foo", "col3"=>"bar"
(1 row)
```

將 `hstore` 轉換為預先定義的 `record` 型別：

```

CREATE TABLE test (col1 integer, col2 text, col3 text);

SELECT * FROM populate_record(null::test,
                              '"col1"=>"456", "col2"=>"zzz"');
 col1 | col2 | col3
------+------+------
  456 | zzz  |
(1 row)
```

使用 `hstore` 中的值修改現有記錄：

```

CREATE TABLE test (col1 integer, col2 text, col3 text);
INSERT INTO test VALUES (123, 'foo', 'bar');

SELECT (r).* FROM (SELECT t #= '"col3"=>"baz"' AS r FROM test t) s;
 col1 | col2 | col3
------+------+------
  123 | foo  | baz
(1 row)
```

<a id="HSTORE-STATISTICS"></a>

### F.17.5. 統計資訊 [#](#hstore-statistics) <a href="#hstore-statistics" id="hstore-statistics"></a>

`hstore` 型別天生具有彈性，因此可能含有許多不同的鍵。檢查鍵是否有效是應用程式的責任。以下範例示範數種檢查鍵與取得統計資訊的技術。

簡單範例：

```

SELECT * FROM each('aaa=>bq, b=>NULL, ""=>1');
```

使用資料表：

```

CREATE TABLE stat AS SELECT (each(h)).key, (each(h)).value FROM testhstore;
```

即時統計資訊：

```

SELECT key, count(*) FROM
  (SELECT (each(h)).key FROM testhstore) AS stat
  GROUP BY key
  ORDER BY count DESC, key;
    key    | count
-----------+-------
 line      |   883
 query     |   207
 pos       |   203
 node      |   202
 space     |   197
 status    |   195
 public    |   194
 title     |   190
 org       |   189
...................
```

<a id="HSTORE-COMPATIBILITY"></a>

### F.17.6. 相容性 [#](#hstore-compatibility) <a href="#hstore-compatibility" id="hstore-compatibility"></a>

自 PostgreSQL 9.0 起，`hstore` 使用與舊版不同的內部表示法。這不會造成傾印／還原升級的阻礙，因為文字表示法（用於傾印）未變更。

進行二進位升級時，新程式碼會辨識舊格式資料以維持向上相容性。處理尚未由新程式碼修改的資料時，這會產生些微效能損失。可如下執行 `UPDATE` 陳述式，強制升級資料表欄位中的所有值：

```

UPDATE tablename SET hstorecol = hstorecol || '';
```

另一種方式是：

```

ALTER TABLE tablename ALTER hstorecol TYPE hstore USING hstorecol || '';
```

`ALTER TABLE` 方法需要在資料表上取得 `ACCESS EXCLUSIVE` 鎖定，但不會因舊資料列版本而使資料表膨脹。

<a id="HSTORE-TRANSFORMS"></a>

### F.17.7. 轉換 [#](#hstore-transforms) <a href="#hstore-transforms" id="hstore-transforms"></a>

另有可用擴充功能，為 PL/Perl 與 PL/Python 語言實作 `hstore` 型別的轉換。PL/Perl 的擴充功能分別名為 `hstore_plperl` 與 `hstore_plperlu`，對應受信任與不受信任的 PL/Perl。若安裝這些轉換並在建立函式時指定它們，`hstore` 值會對應到 Perl 雜湊。PL/Python 的擴充功能名為 `hstore_plpython3u`；若使用它，`hstore` 值會對應到 Python 字典。

<a id="HSTORE-AUTHORS"></a>

### F.17.8. 作者 [#](#hstore-authors) <a href="#hstore-authors" id="hstore-authors"></a>

Oleg Bartunov `<oleg@sai.msu.su>`, Moscow, Moscow University, Russia

Teodor Sigaev `<teodor@sigaev.ru>`, Moscow, Delta-Soft Ltd., Russia

Andrew Gierth `<andrew@tao11.riddles.org.uk>`（英國）的額外改進

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/hstore.html)
