<a id="CATALOG-PG-SHDEPEND"></a>

## 52.48. `pg_shdepend` [#](#catalog-pg-shdepend) <a href="#catalog-pg-shdepend" id="catalog-pg-shdepend"></a>

<a id="id-1.10.4.50.2"></a>

系統目錄 `pg_shdepend` 記錄資料庫物件與共享物件（例如角色）之間的相依關係。這些資訊讓 PostgreSQL 能在嘗試刪除這些物件之前，確保它們未被參照。

另請參閱 [`pg_depend`](catalog-pg-depend.md)，它對涉及單一資料庫內物件的相依關係執行類似的功能。

與大多數系統目錄不同，`pg_shdepend` 由叢集中的所有資料庫共享：每個叢集只有一份 `pg_shdepend`，而不是每個資料庫各一份。

<a id="id-1.10.4.50.6"></a>

**表 52.48. `pg_shdepend` 欄位**

<table border="1" class="table" summary="表 52.48. pg_shdepend 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">dbid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       相依物件所在資料庫的 OID；若為共享物件則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       相依物件所在之系統目錄的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       特定相依物件的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">objsubid</code> <code class="type">int4</code>
</p>
<p>
       對於資料表欄位，這是欄位編號（<code class="structfield">objid</code> 與 <code class="structfield">classid</code> 參照資料表本身）。對於所有其他物件類型，此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">refclassid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       被參照物件所在之系統目錄的 OID（必須是共享系統目錄）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">refobjid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       特定被參照物件的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">deptype</code> <code class="type">char</code>
</p>
<p>
       定義此相依關係特定語意的代碼；請參閱正文
      </p></td></tr></tbody></table>

<br>

在所有情況下，`pg_shdepend` 項目都表示：若不同時刪除相依物件，就無法刪除被參照物件。不過，`deptype` 還區分出數種子類型：

`SHARED_DEPENDENCY_OWNER` (`o`)
:   被參照物件（必須是角色）是相依物件的擁有者。

`SHARED_DEPENDENCY_ACL` (`a`)
:   被參照物件（必須是角色）出現在相依物件的 ACL 中。（不會為物件的擁有者建立 `SHARED_DEPENDENCY_ACL` 項目，因為擁有者無論如何都會有一筆 `SHARED_DEPENDENCY_OWNER` 項目。）

`SHARED_DEPENDENCY_INITACL` (`i`)
:   被參照物件（必須是角色）出現在相依物件的某筆 [`pg_init_privs`](catalog-pg-init-privs.md) 項目中。

`SHARED_DEPENDENCY_POLICY` (`r`)
:   被參照物件（必須是角色）被列為某個相依政策物件的目標。

`SHARED_DEPENDENCY_TABLESPACE` (`t`)
:   被參照物件（必須是資料表空間）被列為某個沒有實體儲存之關聯的資料表空間。

未來可能需要其他相依類型。特別要注意，目前的定義只支援以角色與資料表空間作為被參照物件。

與 `pg_depend` 系統目錄相同，大多數在 initdb 期間建立的物件都被視為「釘住」（pinned）的物件。`pg_shdepend` 中不會建立任何以釘住物件作為被參照物件或相依物件的項目。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-shdepend.html)（原文版本：18.6；核對日期：2026-10-17）
