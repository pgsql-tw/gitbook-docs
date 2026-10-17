<a id="CATALOG-PG-OPCLASS"></a>

## 52.33. `pg_opclass` [#](#CATALOG-PG-OPCLASS)

<a id="id-1.10.4.35.2"></a>

目錄 `pg_opclass` 定義索引存取方法的運算子類別。每個運算子類別為特定資料型別與特定索引存取方法的索引欄位定義語意。運算子類別本質上是指定某個特定的運算子家族適用於某個特定的可索引欄位資料型別。該家族中實際可用於此索引欄位的運算子，就是那些接受該欄位資料型別作為左側輸入的運算子。

[第 36.16 節](../../server-programming/extend/xindex.md)詳細說明了運算子類別。

<a id="id-1.10.4.35.5"></a>

**表 52.33. `pg_opclass` 欄位**

<table border="1" class="table" summary="表 52.33. pg_opclass 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">opcmethod</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子類別所適用的索引存取方法
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcname</code> <code class="type">name</code>
</p>
<p>
       此運算子類別的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子類別的命名空間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子類別的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcfamily</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-opfamily.md"><code class="structname">pg_opfamily</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此運算子類別的運算子家族
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcintype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子類別所索引的資料型別
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opcdefault</code> <code class="type">bool</code>
</p>
<p>
       若此運算子類別是 <code class="structfield">opcintype</code> 的預設運算子類別，則為 true
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opckeytype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       儲存於索引中的資料型別；若與 <code class="structfield">opcintype</code> 相同則為零
</p></td></tr></tbody></table>

<br>

運算子類別的 `opcmethod` 必須與包含它的運算子家族的 `opfmethod` 相符。此外，對於任何給定的 `opcmethod` 與 `opcintype` 組合，`opcdefault` 為 true 的 `pg_opclass` 資料列不得超過一個。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-opclass.html)（原文版本：18.6；核對日期：2026-10-17）
