<a id="DATATYPE-BOOLEAN"></a>

## 8.6. 布林型別 [#](#DATATYPE-BOOLEAN)

<a id="id-1.5.7.14.2"></a><a id="id-1.5.7.14.3"></a><a id="id-1.5.7.14.4"></a>

PostgreSQL 提供標準 SQL 的 `boolean` 型別；請參閱[表 8.19](datatype-boolean.md#DATATYPE-BOOLEAN-TABLE)。`boolean` 型別可以有數種狀態：「true」、「false」，以及第三種狀態「unknown」，後者是以 SQL 的空值（null）來表示。

<a id="DATATYPE-BOOLEAN-TABLE"></a>

**表 8.19. 布林資料型別**

<table border="1" class="table" summary="Boolean Data Type"><colgroup><col/><col/><col/></colgroup><thead><tr><th>名稱</th><th>儲存空間大小</th><th>說明</th></tr></thead><tbody><tr><td><code class="type">boolean</code></td><td>1 個位元組</td><td>true 或 false 的狀態</td></tr></tbody></table>

<br>

在 SQL 查詢中，布林常數可以用 SQL 關鍵字 `TRUE`、`FALSE` 與 `NULL` 來表示。

`boolean` 型別的資料型別輸入函式接受下列這些代表「true」狀態的字串表示法：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">true</code></td></tr><tr><td><code class="literal">yes</code></td></tr><tr><td><code class="literal">on</code></td></tr><tr><td><code class="literal">1</code></td></tr></table>

以及下列這些代表「false」狀態的表示法：

<table border="0" class="simplelist" summary="Simple list"><tr><td><code class="literal">false</code></td></tr><tr><td><code class="literal">no</code></td></tr><tr><td><code class="literal">off</code></td></tr><tr><td><code class="literal">0</code></td></tr></table>

這些字串的唯一前綴也同樣被接受，例如 `t` 或 `n`。開頭或結尾的空白會被忽略，而且不區分大小寫。

`boolean` 型別的資料型別輸出函式一律只輸出 `t` 或 `f`，如[範例 8.2](datatype-boolean.md#DATATYPE-BOOLEAN-EXAMPLE)所示。

<a id="DATATYPE-BOOLEAN-EXAMPLE"></a>

**範例 8.2. 使用 `boolean` 型別**

```

CREATE TABLE test1 (a boolean, b text);
INSERT INTO test1 VALUES (TRUE, 'sic est');
INSERT INTO test1 VALUES (FALSE, 'non est');
SELECT * FROM test1;
 a |    b
---+---------
 t | sic est
 f | non est

SELECT * FROM test1 WHERE a;
 a |    b
---+---------
 t | sic est
```

<br>

在 SQL 查詢中撰寫布林常數時，關鍵字 `TRUE` 與 `FALSE` 是較建議（符合 SQL 標準）的方式。但你也可以依照[第 4.1.2.7 節](../sql-syntax/sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC)所述的通用字串常數語法來使用字串表示法，例如 `'yes'::boolean`。

請注意，剖析器會自動理解 `TRUE` 與 `FALSE` 屬於 `boolean` 型別，但 `NULL` 並非如此，因為它可以是任何型別。因此在某些情境下，你可能必須明確地將 `NULL` 轉換為 `boolean`，例如 `NULL::boolean`。反過來說，在剖析器能夠推斷出字面值必定為 `boolean` 型別的情境下，字串常數形式的布林值就可以省略型別轉換。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/datatype-boolean.html)（原文版本：18.6；核對日期：2026-09-12）
