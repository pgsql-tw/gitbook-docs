<a id="CATALOG-PG-OPERATOR"></a>

## 52.34. `pg_operator` [#](#catalog-pg-operator) <a href="#catalog-pg-operator" id="catalog-pg-operator"></a>

<a id="id-1.10.4.36.2"></a>

目錄 `pg_operator` 儲存運算子的相關資訊。
更多資訊請參閱 [CREATE OPERATOR](../../reference/sql-commands/sql-createoperator.md)
與[第 36.14 節](../../server-programming/extend/xoper.md)。

<a id="id-1.10.4.36.4"></a>

**表 52.34. `pg_operator` 欄位**

<table border="1" class="table" summary="表 52.34. pg_operator 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">oprname</code> <code class="type">name</code>
</p>
<p>
       運算子名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此運算子之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprkind</code> <code class="type">char</code>
</p>
<p>
<code class="literal">b</code> = 中置運算子（<span class="quote">“<span class="quote">both</span>”</span>），
       或 <code class="literal">l</code> = 前置運算子（<span class="quote">“<span class="quote">left</span>”</span>）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprcanmerge</code> <code class="type">bool</code>
</p>
<p>
       此運算子支援合併連接
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprcanhash</code> <code class="type">bool</code>
</p>
<p>
       此運算子支援雜湊連接
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprleft</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       左運算元的型別（前置運算子為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprright</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       右運算元的型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprresult</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       結果的型別
       （尚未定義的 <span class="quote">“<span class="quote">shell</span>”</span> 運算子為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprcom</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子的交換子（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprnegate</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子的否定子（若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprcode</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       實作此運算子的函式
       （尚未定義的 <span class="quote">“<span class="quote">shell</span>”</span> 運算子為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprrest</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子的限制選擇性估算函式
       （若無則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">oprjoin</code> <code class="type">regproc</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子的連接選擇性估算函式
       （若無則為零）
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-operator.html)（原文版本：18.6；核對日期：2026-10-17）
