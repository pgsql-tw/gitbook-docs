<a id="CATALOG-PG-DEFAULT-ACL"></a>

## 52.17. `pg_default_acl` [#](#catalog-pg-default-acl) <a href="#catalog-pg-default-acl" id="catalog-pg-default-acl"></a>

<a id="id-1.10.4.19.2"></a>

系統目錄 `pg_default_acl` 存放要指派給新建立物件的初始權限。

<a id="id-1.10.4.19.4"></a>

**表 52.17. `pg_default_acl` 欄位**

<table border="1" class="table" summary="表 52.17. pg_default_acl 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">defaclrole</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       與此項目相關聯之角色的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">defaclnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       與此項目相關聯之命名空間的 OID；若無則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">defaclobjtype</code> <code class="type">char</code>
</p>
<p>
       此項目所適用的物件類型：
       <code class="literal">r</code> = 關聯（資料表、檢視表），
       <code class="literal">S</code> = 序列，
       <code class="literal">f</code> = 函式，
       <code class="literal">T</code> = 型別，
       <code class="literal">n</code> = 綱要，
       <code class="literal">L</code> = 大型物件
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">defaclacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       此類物件在建立時應具有的存取權限
      </p></td></tr></tbody></table>

<br>

`pg_default_acl` 項目顯示要指派給屬於指定使用者之物件的初始權限。目前有兩種項目：`defaclnamespace` = 零的「全域」項目，以及參照特定綱要的「個別綱要」項目。若存在全域項目，它會*覆寫*該物件類型一般寫死的預設權限。個別綱要項目若存在，則代表要*加入*全域或寫死之預設權限的權限。

請注意，當另一個系統目錄中的 ACL 項目為 null 時，它會被視為代表其物件寫死的預設權限，*而不是* `pg_default_acl` 當下可能存放的任何內容。`pg_default_acl` 只會在物件建立期間被查閱。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-default-acl.html)（原文版本：18.6；核對日期：2026-10-17）
