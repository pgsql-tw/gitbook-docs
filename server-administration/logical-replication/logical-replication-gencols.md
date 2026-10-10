<a id="LOGICAL-REPLICATION-GENCOLS"></a>

## 29.6. 產生欄位的複寫 [#](#LOGICAL-REPLICATION-GENCOLS)

一般而言，訂閱者端資料表的定義會與
發佈者資料表相同，因此如果發佈者資料表有 [`GENERATED column`](../../the-sql-language/ddl/ddl-generated-columns.md)（產生欄位），則訂閱者資料表
也會有相對應的產生欄位。在這種情況下，所使用的一律是訂閱者
資料表產生欄位的值。

例如，請注意下方訂閱者資料表產生欄位的值來自
訂閱者欄位的計算結果。

```

/* pub # */ CREATE TABLE tab_gen_to_gen (a int, b int GENERATED ALWAYS AS (a + 1) STORED);
/* pub # */ INSERT INTO tab_gen_to_gen VALUES (1),(2),(3);
/* pub # */ CREATE PUBLICATION pub1 FOR TABLE tab_gen_to_gen;
/* pub # */ SELECT * FROM tab_gen_to_gen;
 a | b
---+---
 1 | 2
 2 | 3
 3 | 4
(3 rows)

/* sub # */ CREATE TABLE tab_gen_to_gen (a int, b int GENERATED ALWAYS AS (a * 100) STORED);
/* sub # */ CREATE SUBSCRIPTION sub1 CONNECTION 'dbname=test_pub' PUBLICATION pub1;
/* sub # */ SELECT * from tab_gen_to_gen;
 a | b
---+----
 1 | 100
 2 | 200
 3 | 300
(3 rows)
```

事實上，在 18.0 版之前，邏輯複寫完全不會發佈
`GENERATED` 欄位。

不過，有時候會希望將產生欄位複寫到一般欄位。

<a id="LOGICAL-REPLICATION-GENCOLS-TIP"></a>

### 提示

透過輸出外掛將資料複寫到
非 PostgreSQL 資料庫時，這項功能可能很有用，特別是當目標資料庫
不支援產生欄位時。

產生欄位預設不會被發佈，但使用者可以選擇
像一般欄位一樣發佈儲存式產生欄位。

有兩種方式可以做到這點：

* 將 `PUBLICATION` 參數
  [`publish_generated_columns`](../../reference/sql-commands/sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) 設為 `stored`。
  這會指示 PostgreSQL 邏輯複寫發佈該發佈之資料表中
  目前與未來的儲存式產生欄位。
* 指定資料表的[欄位清單](logical-replication-col-lists.md)，
  明確指定要發佈哪些儲存式產生欄位。

  <a id="LOGICAL-REPLICATION-GENCOLS-NOTE"></a>

  ### 注意

  在決定要發佈資料表的哪些欄位時，欄位清單
  優先，會覆寫
  `publish_generated_columns` 參數的作用。

下表摘要說明邏輯複寫涉及產生欄位時的
行為。表中分別列出未啟用發佈產生欄位時，
以及已啟用時的結果。

<a id="LOGICAL-REPLICATION-GENCOLS-TABLE-SUMMARY"></a>

**表 29.2. 複寫結果摘要**

<table border="1" class="table" summary="複寫結果摘要"><colgroup><col/><col/><col/><col/></colgroup><thead><tr><th>發佈產生欄位？</th><th>發佈者資料表欄位</th><th>訂閱者資料表欄位</th><th>結果</th></tr></thead><tbody><tr><td>否</td><td>GENERATED</td><td>GENERATED</td><td>發佈者資料表欄位不會被複寫。使用訂閱者資料表產生欄位的值。</td></tr><tr><td>否</td><td>GENERATED</td><td>一般欄位</td><td>發佈者資料表欄位不會被複寫。使用訂閱者資料表一般欄位的預設值。</td></tr><tr><td>否</td><td>GENERATED</td><td>--不存在--</td><td>發佈者資料表欄位不會被複寫。不會發生任何事。</td></tr><tr><td>是</td><td>GENERATED</td><td>GENERATED</td><td>錯誤（ERROR）。不支援。</td></tr><tr><td>是</td><td>GENERATED</td><td>一般欄位</td><td>發佈者資料表欄位的值會複寫到訂閱者資料表欄位。</td></tr><tr><td>是</td><td>GENERATED</td><td>--不存在--</td><td>錯誤（ERROR）。該欄位會被回報為訂閱者資料表中缺少的欄位。</td></tr></tbody></table>

<br>

<a id="LOGICAL-REPLICATION-GENCOLS-WARNING"></a>

### 警告

目前不支援由多個發佈組成、且同一個資料表
在這些發佈中以不同欄位清單發佈的訂閱。請參閱[第 29.5 節](logical-replication-col-lists.md)。

如果某個發佈會發佈產生欄位，而同一訂閱中的另一個發佈
對同一個資料表不發佈產生欄位，也可能發生同樣的情況。

<a id="LOGICAL-REPLICATION-GENCOLS-NOTE-2"></a>

### 注意

如果訂閱者是 18 之前的版本，則即使發佈者中定義了產生欄位，
初始資料表同步也不會複製這些產生欄位。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/logical-replication-gencols.html)（原文版本：18.6；核對日期：2026-10-10）
