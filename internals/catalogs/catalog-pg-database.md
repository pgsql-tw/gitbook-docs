<a id="CATALOG-PG-DATABASE"></a>

## 52.15. `pg_database` [#](#CATALOG-PG-DATABASE)

<a id="id-1.10.4.17.2"></a>

系統目錄 `pg_database` 存放可用資料庫的相關資訊。資料庫是以 [`CREATE DATABASE`](../../reference/sql-commands/sql-createdatabase.md) 命令建立的。關於部分參數意義的詳細資訊，請參閱[第 22 章](../../server-administration/managing-databases/README.md)。

與大多數系統目錄不同，`pg_database` 由叢集中的所有資料庫共享：每個叢集只有一份 `pg_database`，而不是每個資料庫各一份。

<a id="id-1.10.4.17.5"></a>

**表 52.15. `pg_database` 欄位**

<table border="1" class="table" summary="表 52.15. pg_database 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       資料庫名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datdba</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       資料庫的擁有者，通常是建立它的使用者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">encoding</code> <code class="type">int4</code>
</p>
<p>
       此資料庫的字元編碼（<a class="link" href="../../the-sql-language/functions/functions-info.md#PG-ENCODING-TO-CHAR"><code class="function">pg_encoding_to_char()</code></a> 可以將此數字轉換為編碼名稱）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datlocprovider</code> <code class="type">char</code>
</p>
<p>
       此資料庫的區域設定提供者：<code class="literal">b</code> = builtin，
       <code class="literal">c</code> = libc，<code class="literal">i</code> = icu </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datistemplate</code> <code class="type">bool</code>
</p>
<p>
       若為真，則任何具有 <code class="literal">CREATEDB</code> 權限的使用者都可以複製此資料庫；若為假，則只有超級使用者或資料庫的擁有者可以複製它。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datallowconn</code> <code class="type">bool</code>
</p>
<p>
       若為假，則沒有人能連線到此資料庫。這用來保護 <code class="literal">template0</code> 資料庫不被修改。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dathasloginevt</code> <code class="type">bool</code>
</p>
<p>
        表示此資料庫中定義了登入事件觸發程序。此旗標用來避免在每次後端啟動時，對 <code class="structname">pg_event_trigger</code> 資料表進行額外的查詢。此旗標由 <span class="productname">PostgreSQL</span> 內部使用，不應手動修改，也不應為了監控目的而讀取。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datconnlimit</code> <code class="type">int4</code>
</p>
<p>
       設定可對此資料庫建立的最大同時連線數。-1 表示沒有限制，-2 表示該資料庫無效。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datfrozenxid</code> <code class="type">xid</code>
</p>
<p>
       在此資料庫中，此 ID 之前的所有交易 ID 都已被替換為永久的（<span class="quote">“<span class="quote">frozen</span>”</span>，凍結）交易 ID。這用來追蹤資料庫是否需要執行 vacuum，以防止交易 ID 回捲，或讓 <code class="literal">pg_xact</code> 得以縮減。它是各資料表 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relfrozenxid</code> 值中的最小值。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datminmxid</code> <code class="type">xid</code>
</p>
<p>
       在此資料庫中，此 ID 之前的所有 multixact ID 都已被替換為交易 ID。這用來追蹤資料庫是否需要執行 vacuum，以防止 multixact ID 回捲，或讓 <code class="literal">pg_multixact</code> 得以縮減。它是各資料表 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">relminmxid</code> 值中的最小值。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dattablespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此資料庫的預設資料表空間。在此資料庫中，所有 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">reltablespace</code> 為零的資料表都會存放在此資料表空間中；特別是，所有非共享的系統目錄都會在這裡。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datcollate</code> <code class="type">text</code>
</p>
<p>
       此資料庫的 LC_COLLATE
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datctype</code> <code class="type">text</code>
</p>
<p>
       此資料庫的 LC_CTYPE
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datlocale</code> <code class="type">text</code>
</p>
<p>
       此資料庫的定序提供者區域設定名稱。若提供者為 <code class="literal">libc</code>，則 <code class="structfield">datlocale</code> 為 <code class="literal">NULL</code>，改為使用 <code class="structfield">datcollate</code> 與 <code class="structfield">datctype</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">daticurules</code> <code class="type">text</code>
</p>
<p>
       此資料庫的 ICU 定序規則
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datcollversion</code> <code class="type">text</code>
</p>
<p>
       定序的提供者特定版本。這會在建立資料庫時記錄下來，並在使用資料庫時檢查，以偵測可能導致資料損毀的定序定義變更。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-database.html)（原文版本：18.6；核對日期：2026-10-17）
