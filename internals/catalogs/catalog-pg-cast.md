<a id="CATALOG-PG-CAST"></a>

## 52.10. `pg_cast` [#](#CATALOG-PG-CAST)

<a id="id-1.10.4.12.2"></a>

系統目錄 `pg_cast` 存放資料型別的轉換路徑，包括內建的與使用者定義的。

請注意，`pg_cast` 並未呈現系統知道如何執行的每一種型別轉換，
只呈現那些無法由某種通用規則推導出來的轉換。例如，網域與其基礎型別之間的
型別轉換並未明確呈現在 `pg_cast` 中。另一個重要的例外是
「自動 I/O 轉換型別轉換」，也就是使用資料型別本身的 I/O 函式與 `text` 或其他
字串型別相互轉換的型別轉換，也並未明確呈現在
`pg_cast` 中。

<a id="id-1.10.4.12.5"></a>

**表 52.10. `pg_cast` 欄位**

<table border="1" class="table" summary="表 52.10. pg_cast 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oid</code> <code class="type">oid</code>
</p>
<p>
       資料列識別碼
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castsource</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       來源資料型別的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">casttarget</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       目標資料型別的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castfunc</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       用來執行此型別轉換之函式的 OID。若此轉換方法不需要函式，
       則存放零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castcontext</code> <code class="type">char</code>
</p>
<p>
       表示此型別轉換可以在哪些情境中呼叫。
       <code class="literal">e</code> 表示只能作為明確型別轉換（使用
       <code class="literal">CAST</code> 或 <code class="literal">::</code> 語法）。
       <code class="literal">a</code> 表示除了明確轉換之外，也可以在指派給目標欄位時
       隱含地進行。
       <code class="literal">i</code> 表示除了上述其他情況之外，也可以在運算式中
       隱含地進行。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">castmethod</code> <code class="type">char</code>
</p>
<p>
       表示此型別轉換的執行方式。
       <code class="literal">f</code> 表示使用 <code class="structfield">castfunc</code> 欄位中指定的函式。
       <code class="literal">i</code> 表示使用輸入／輸出函式。
       <code class="literal">b</code> 表示這些型別可二進位強制轉換，因此不需要任何轉換。
      </p></td></tr></tbody></table>

<br>

`pg_cast` 中列出的型別轉換函式必須一律以型別轉換的來源型別
作為第一個引數的型別，並以型別轉換的目的型別作為結果型別。
型別轉換函式最多可以有三個引數。第二個引數若存在，
必須是 `integer` 型別；它接收與目的型別相關聯的型別修飾詞，
若沒有則接收 -1。第三個引數若存在，必須是 `boolean` 型別；
若此型別轉換是明確型別轉換，它接收 `true`，否則接收 `false`。

若相關聯的函式接受超過一個引數，則建立來源與目標型別相同的
`pg_cast` 項目是合法的。這類項目代表
「長度強制轉換函式」，它們將該型別的值強制轉換為
對特定型別修飾詞值而言合法的值。

當 `pg_cast` 項目的來源與目標型別不同，且其函式接受超過一個引數時，
它代表在單一步驟中從一種型別轉換為另一種型別並套用長度強制轉換。
若沒有這樣的項目可用，強制轉換為使用型別修飾詞的型別時會涉及兩個步驟：
一個步驟在資料型別之間轉換，第二個步驟套用修飾詞。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-cast.html)（原文版本：18.6；核對日期：2026-10-17）
