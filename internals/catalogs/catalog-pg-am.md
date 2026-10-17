<a id="CATALOG-PG-AM"></a>

## 52.3. `pg_am` [#](#CATALOG-PG-AM)

<a id="id-1.10.4.5.2"></a>

系統目錄 `pg_am` 存放關聯存取方法的相關資訊。系統所支援的每一種存取方法各有一筆資料列。
目前只有資料表與索引具有存取方法。資料表存取方法與索引存取方法的需求，分別在[第 62 章](../tableam/README.md)與
[第 63 章](../indexam/README.md)中詳細討論。

<a id="id-1.10.4.5.4"></a>

**表 52.3. `pg_am` 欄位**

<table border="1" class="table" summary="表 52.3. pg_am 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">amname</code> <code class="type">name</code>
</p>
<p>
       存取方法的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amhandler</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       負責提供該存取方法相關資訊之處理函式的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">amtype</code> <code class="type">char</code>
</p>
<p>
<code class="literal">t</code> = 資料表（包括具體化檢視表），
       <code class="literal">i</code> = 索引。
      </p></td></tr></tbody></table>

<br>

### 注意

在 PostgreSQL 9.6 之前，`pg_am`
包含許多代表索引存取方法特性的額外欄位。這些資料現在只能在 C 程式碼層級直接看到。
不過，已新增 `pg_index_column_has_property()` 及相關
函式，讓 SQL 查詢可以檢視索引存取方法的特性；請參閱[表 9.76](../../the-sql-language/functions/functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE)。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-am.html)（原文版本：18.6；核對日期：2026-10-17）
