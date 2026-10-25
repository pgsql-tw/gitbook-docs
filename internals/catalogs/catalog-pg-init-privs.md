<a id="CATALOG-PG-INIT-PRIVS"></a>

## 52.28. `pg_init_privs` [#](#catalog-pg-init-privs) <a href="#catalog-pg-init-privs" id="catalog-pg-init-privs"></a>

<a id="id-1.10.4.30.2"></a>

目錄 `pg_init_privs` 記錄系統中物件之初始權限的相關資訊。資料庫中每個具有非預設（非 NULL）初始權限集合的物件，都各有一個項目。

物件取得初始權限的方式有兩種：一是在系統初始化時（由 initdb）設定這些權限；二是物件在 [`CREATE EXTENSION`](../../reference/sql-commands/sql-createextension.md) 期間建立，且擴充功能腳本使用 [`GRANT`](../../reference/sql-commands/sql-grant.md) 系統設定初始權限。請注意，系統會在擴充功能腳本執行期間自動處理權限的記錄，擴充功能作者只需在腳本中使用 `GRANT` 與 `REVOKE` 陳述式，即可讓這些權限被記錄下來。`privtype` 欄位指出初始權限是由 initdb 設定，還是在 `CREATE EXTENSION` 命令期間設定。

初始權限由 initdb 設定的物件，其項目的 `privtype` 為 `'i'`；初始權限由 `CREATE EXTENSION` 設定的物件，其項目的 `privtype` 為 `'e'`。

<a id="id-1.10.4.30.6"></a>

**表 52.28. `pg_init_privs` 欄位**

<table border="1" class="table" summary="表 52.28. pg_init_privs 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objoid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       特定物件的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此物件所在之系統目錄的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int4</code>
</p>
<p>
       對於資料表欄位，這是欄位編號（<code class="structfield">objoid</code> 與 <code class="structfield">classoid</code> 參照資料表本身）。對於所有其他物件類型，此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">privtype</code> <code class="type">char</code>
</p>
<p>
       定義此物件初始權限類型的代碼；請參閱本文
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">initprivs</code> <code class="type">aclitem[]</code>
</p>
<p>
       初始存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-init-privs.html)（原文版本：18.6；核對日期：2026-10-17）
