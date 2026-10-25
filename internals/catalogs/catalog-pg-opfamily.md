<a id="CATALOG-PG-OPFAMILY"></a>

## 52.35. `pg_opfamily` [#](#catalog-pg-opfamily) <a href="#catalog-pg-opfamily" id="catalog-pg-opfamily"></a>

<a id="id-1.10.4.37.2"></a>

目錄 `pg_opfamily` 定義運算子家族。每個運算子家族是一組運算子及相關支援常式的集合，這些運算子與常式實作了為特定索引存取方法所指定的語意。此外，同一家族中的運算子全都以存取方法所指定的方式彼此「相容」。運算子家族的概念讓跨資料型別的運算子可以搭配索引使用，並可運用存取方法語意的知識對其進行推理。

[第 36.16 節](../../server-programming/extend/xindex.md)詳細說明了運算子家族。

<a id="id-1.10.4.37.5"></a>

**表 52.35. `pg_opfamily` 欄位**

<table border="1" class="table" summary="表 52.35. pg_opfamily 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">opfmethod</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子家族所適用的索引存取方法
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opfname</code> <code class="type">name</code>
</p>
<p>
       此運算子家族的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opfnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子家族的命名空間
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">opfowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此運算子家族的擁有者
      </p></td></tr></tbody></table>

<br>

定義運算子家族的大部分資訊並不在其 `pg_opfamily` 資料列中，而是在
[`pg_amop`](catalog-pg-amop.md)、
[`pg_amproc`](catalog-pg-amproc.md)
與
[`pg_opclass`](catalog-pg-opclass.md) 中的相關資料列。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-opfamily.html)（原文版本：18.6；核對日期：2026-10-17）
