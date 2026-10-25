<a id="CATALOG-PG-COLLATION"></a>

## 52.12. `pg_collation` [#](#catalog-pg-collation) <a href="#catalog-pg-collation" id="catalog-pg-collation"></a>

<a id="id-1.10.4.14.2"></a>

目錄 `pg_collation` 描述可用的定序；定序本質上是從 SQL
名稱到作業系統區域設定類別的對應。
更多資訊請參閱[第 23.2 節](../../server-administration/charset/collation.md)。

<a id="id-1.10.4.14.4"></a>

**表 52.12. `pg_collation` 欄位**

<table border="1" class="table" summary="表 52.12. pg_collation 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">collname</code> <code class="type">name</code>
</p>
<p>
       定序名稱（在每個命名空間與編碼中唯一）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此定序之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       定序的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collprovider</code> <code class="type">char</code>
</p>
<p>
       定序的提供者：<code class="literal">d</code> = 資料庫預設，
       <code class="literal">b</code> = 內建（builtin），<code class="literal">c</code> = libc，
       <code class="literal">i</code> = icu </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collisdeterministic</code> <code class="type">bool</code>
</p>
<p>
       此定序是否為確定性定序？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collencoding</code> <code class="type">int4</code>
</p>
<p>
       此定序適用的編碼；若適用於任何編碼則為 -1
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collcollate</code> <code class="type">text</code>
</p>
<p>
此定序物件的 <code class="symbol">LC_COLLATE</code>。若提供者不是
       <code class="literal">libc</code>，則 <code class="structfield">collcollate</code> 為
       <code class="literal">NULL</code>，改用 <code class="structfield">colllocale</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collctype</code> <code class="type">text</code>
</p>
<p>
此定序物件的 <code class="symbol">LC_CTYPE</code>。若提供者不是
       <code class="literal">libc</code>，則 <code class="structfield">collctype</code> 為
       <code class="literal">NULL</code>，改用 <code class="structfield">colllocale</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">colllocale</code> <code class="type">text</code>
</p>
<p>
       此定序物件的定序提供者區域設定名稱。若提供者是
       <code class="literal">libc</code>，則
       <code class="structfield">colllocale</code> 為 <code class="literal">NULL</code>；
       改用 <code class="structfield">collcollate</code> 與
       <code class="structfield">collctype</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collicurules</code> <code class="type">text</code>
</p>
<p>
       此定序物件的 ICU 定序規則
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">collversion</code> <code class="type">text</code>
</p>
<p>
       定序的提供者特定版本。此值在建立定序時記錄，並在使用定序時檢查，
       以偵測可能導致資料損毀的定序定義變更。
      </p></td></tr></tbody></table>

<br>

請注意，此目錄上的唯一鍵是（`collname`,
`collencoding`, `collnamespace`），而不只是
（`collname`, `collnamespace`）。
PostgreSQL 通常會忽略所有
`collencoding` 既不等於目前資料庫的編碼、
也不等於 -1 的定序，而且禁止建立與某個
`collencoding` = -1 的項目同名的新項目。
因此，使用限定的 SQL 名稱
（*`schema`*.*`name`*）就足以識別一個定序，
即使依目錄定義這並不唯一。
如此定義此目錄的原因是：
initdb 會在叢集初始化時，以系統上所有可用區域設定的
項目填入此目錄，因此它必須能夠容納叢集中可能使用的
所有編碼的項目。

在 `template0` 資料庫中，建立編碼與資料庫編碼不相符的定序
可能會有用處，因為這些定序可能與日後從
`template0` 複製出的資料庫編碼相符。目前這必須以手動方式完成。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-collation.html)（原文版本：18.6；核對日期：2026-10-17）
