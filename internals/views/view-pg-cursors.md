<a id="VIEW-PG-CURSORS"></a>

## 53.7. `pg_cursors` [#](#VIEW-PG-CURSORS)

<a id="id-1.10.5.11.2"></a>

檢視表 `pg_cursors` 列出目前可用的游標。游標可以用以下幾種方式定義：

* 透過 SQL 中的 [`DECLARE`](../../reference/sql-commands/sql-declare.md)
  陳述式
* 透過前端／後端協定中的 Bind 訊息，如
  [第 54.2.3 節](../protocol/protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)所述
* 透過伺服器程式設計介面（SPI），如
  [第 45.1 節](../../server-programming/spi/spi-interface.md)所述

檢視表 `pg_cursors` 會顯示以上述任何方式建立的游標。游標只在定義它的交易期間內存在，除非它被宣告為 `WITH HOLD`。因此，不可保留的游標只會在建立它的交易結束之前出現在此檢視表中。

### 注意

PostgreSQL 內部會使用游標來實作某些元件，例如程序語言。因此，`pg_cursors` 檢視表中可能包含並非由使用者明確建立的游標。

<a id="id-1.10.5.11.4"></a>

**表 53.7. `pg_cursors` 欄位**

<table border="1" class="table" summary="表 53.7. pg_cursors 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">name</code> <code class="type">text</code>
</p>
<p>
       游標的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">statement</code> <code class="type">text</code>
</p>
<p>
       為宣告此游標而送出的原始查詢字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_holdable</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> 表示游標可保留（也就是在宣告該游標的交易提交之後仍可存取）；否則為 <code class="literal">false</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_binary</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> 表示游標宣告為
       <code class="literal">BINARY</code>；否則為 <code class="literal">false</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">is_scrollable</code> <code class="type">bool</code>
</p>
<p>
<code class="literal">true</code> 表示游標可捲動（也就是允許以非循序的方式擷取資料列）；否則為
       <code class="literal">false</code>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">creation_time</code> <code class="type">timestamptz</code>
</p>
<p>
       宣告此游標的時間
      </p></td></tr></tbody></table>

<br>

`pg_cursors` 檢視表是唯讀的。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/view-pg-cursors.html)（原文版本：18.6；核對日期：2026-10-12）
