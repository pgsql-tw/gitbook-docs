<a id="CATALOG-PG-POLICY"></a>

## 52.38. `pg_policy` [#](#CATALOG-PG-POLICY)

<a id="id-1.10.4.40.2"></a>

目錄 `pg_policy` 儲存資料表的資料列層級安全性政策。一個政策包含：它所適用的命令種類（可能是所有命令）、它所適用的角色、要作為安全屏障條件加入包含該資料表之查詢的運算式，以及要作為 `WITH CHECK` 選項加入嘗試在該資料表新增紀錄之查詢的運算式。

<a id="id-1.10.4.40.4"></a>

**表 52.38. `pg_policy` 欄位**

<table border="1" class="table" summary="表 52.38. pg_policy 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">polname</code> <code class="type">name</code>
</p>
<p>
       政策名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此政策所適用的資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polcmd</code> <code class="type">char</code>
</p>
<p>
       此政策所套用的命令類型：
       <code class="literal">r</code> 表示 <a class="xref" href="../../reference/sql-commands/sql-select.md"><span class="refentrytitle">SELECT</span></a>、
       <code class="literal">a</code> 表示 <a class="xref" href="../../reference/sql-commands/sql-insert.md"><span class="refentrytitle">INSERT</span></a>、
       <code class="literal">w</code> 表示 <a class="xref" href="../../reference/sql-commands/sql-update.md"><span class="refentrytitle">UPDATE</span></a>、
       <code class="literal">d</code> 表示 <a class="xref" href="../../reference/sql-commands/sql-delete.md"><span class="refentrytitle">DELETE</span></a>，
       或 <code class="literal">*</code> 表示全部
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polpermissive</code> <code class="type">bool</code>
</p>
<p>
       此政策是寬鬆政策還是限制性政策？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polroles</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此政策所套用的角色；
       零表示 <code class="literal">PUBLIC</code>
       （且通常在陣列中單獨出現）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polqual</code> <code class="type">pg_node_tree</code>
</p>
<p>
       要加入使用該資料表之查詢的安全屏障條件中的運算式樹
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">polwithcheck</code> <code class="type">pg_node_tree</code>
</p>
<p>
       要加入嘗試在該資料表新增資料列之查詢的 WITH CHECK 條件中的運算式樹
      </p></td></tr></tbody></table>

<br>

### 注意

儲存在 `pg_policy` 中的政策，只有在其資料表的
[`pg_class`](catalog-pg-class.md).`relrowsecurity` 已設定時才會套用。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-policy.html)（原文版本：18.6；核對日期：2026-10-17）
