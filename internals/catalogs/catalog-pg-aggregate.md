<a id="CATALOG-PG-AGGREGATE"></a>

## 52.2. `pg_aggregate` [#](#CATALOG-PG-AGGREGATE)

<a id="id-1.10.4.4.2"></a>

目錄 `pg_aggregate` 儲存彙總函式的相關資訊。
彙總函式是一種對一組值（通常是每個符合查詢條件之資料列中的某一個欄位）
進行運算，並傳回由所有這些值計算出之單一值的函式。
典型的彙總函式有 `sum`、`count` 與
`max`。`pg_aggregate` 中的每一筆項目
都是 [`pg_proc`](catalog-pg-proc.md) 中某一筆項目的延伸。
該 `pg_proc` 項目記載彙總函式的名稱、
輸入與輸出資料型別，以及其他與一般函式相似的資訊。

<a id="id-1.10.4.4.4"></a>

**表 52.2. `pg_aggregate` 欄位**

<table border="1" class="table" summary="pg_aggregate 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggfnoid</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
彙總函式的 <code class="structname">pg_proc</code> OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggkind</code> <code class="type">char</code>
</p>
<p>
       彙總函式種類：
       <code class="literal">n</code> 表示<span class="quote">「<span class="quote">一般</span>」</span>彙總函式，
       <code class="literal">o</code> 表示<span class="quote">「<span class="quote">有序集合</span>」</span>彙總函式，
       <code class="literal">h</code> 表示<span class="quote">「<span class="quote">假設集合</span>」</span>彙總函式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggnumdirectargs</code> <code class="type">int2</code>
</p>
<p>
       有序集合或假設集合彙總函式的直接（非彙總）引數數量，
       可變引數陣列計為一個引數。
       若等於 <code class="structfield">pronargs</code>，則該彙總函式必須是可變引數（variadic）的，
       且該可變引數陣列同時描述被彙總的引數
       與最後的直接引數。
       一般彙總函式一律為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggtransfn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       轉換函式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggfinalfn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       最終函式（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggcombinefn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       合併函式（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggserialfn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       序列化函式（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggdeserialfn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       反序列化函式（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggmtransfn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       移動彙總模式的正向轉換函式（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggminvtransfn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       移動彙總模式的反向轉換函式（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggmfinalfn</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       移動彙總模式的最終函式（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggfinalextra</code> <code class="type">bool</code>
</p>
<p>
       為真時，會傳遞額外的虛擬引數給 <code class="structfield">aggfinalfn</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggmfinalextra</code> <code class="type">bool</code>
</p>
<p>
       為真時，會傳遞額外的虛擬引數給 <code class="structfield">aggmfinalfn</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggfinalmodify</code> <code class="type">char</code>
</p>
<p>
       <code class="structfield">aggfinalfn</code> 是否會修改
       轉換狀態值：
       <code class="literal">r</code> 表示它是唯讀的，
       <code class="literal">s</code> 表示 <code class="structfield">aggtransfn</code>
       不能在 <code class="structfield">aggfinalfn</code> 之後套用，
       <code class="literal">w</code> 表示它會寫入該值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggmfinalmodify</code> <code class="type">char</code>
</p>
<p>
       與 <code class="structfield">aggfinalmodify</code> 相同，但適用於
       <code class="structfield">aggmfinalfn</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggsortop</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       相關聯的排序運算子（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggtranstype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       彙總函式內部轉換（狀態）資料的資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggtransspace</code> <code class="type">int4</code>
</p>
<p>
       轉換狀態資料的大約平均大小（以位元組為單位），
       或為零以使用預設估計值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggmtranstype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       移動彙總模式下，彙總函式內部轉換（狀態）資料的
       資料型別（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggmtransspace</code> <code class="type">int4</code>
</p>
<p>
       移動彙總模式下轉換狀態資料的大約平均大小（以位元組為單位），
       或為零以使用預設估計值
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">agginitval</code> <code class="type">text</code>
</p>
<p>
       轉換狀態的初始值。這是一個文字欄位，
       以外部字串表示法存放初始值。
       若此欄位為 null，轉換狀態值
       一開始即為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">aggminitval</code> <code class="type">text</code>
</p>
<p>
       移動彙總模式下轉換狀態的初始值。
       這是一個文字欄位，以外部字串表示法
       存放初始值。若此欄位為 null，轉換狀態值
       一開始即為 null。
      </p></td></tr></tbody></table>

<br>

新的彙總函式以 [`CREATE AGGREGATE`](../../reference/sql-commands/sql-createaggregate.md)
命令註冊。關於撰寫彙總函式以及轉換函式等的意義，
更多資訊請參閱[第 36.12 節](../../server-programming/extend/xaggr.md)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-aggregate.html)（原文版本：18.6；核對日期：2026-10-17）
