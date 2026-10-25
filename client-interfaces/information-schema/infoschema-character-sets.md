<a id="INFOSCHEMA-CHARACTER-SETS"></a>
## 35.7. `character_sets` [#](#infoschema-character-sets) <a href="#infoschema-character-sets" id="infoschema-character-sets"></a>

檢視表 `character_sets` 識別目前資料庫中可用的字元集。由於 PostgreSQL 不支援
在單一資料庫中使用多個字元集，此檢視表只會顯示一個，也就是資料庫編碼。

請留意下列術語在 SQL 標準中的用法：

字元庫（character repertoire）
:   字元的抽象集合，例如 `UNICODE`、`UCS` 或
    `LATIN1`。它不會以 SQL 物件的形式公開，但可以在此檢視表中看到。

字元編碼形式（character encoding form）
:   某個字元庫的一種編碼。大多數較舊的字元庫只使用一種編碼形式，因此這些編碼形式
    沒有另外的名稱（例如，`LATIN2` 是適用於 `LATIN2`
    字元庫的編碼形式）。但舉例來說，Unicode 有 `UTF8`、`UTF16` 等編碼形式
    （並非全部都受 PostgreSQL 支援）。編碼形式不會以 SQL 物件的形式公開，但可以在此
    檢視表中看到。

字元集（character set）
:   一個具名的 SQL 物件，用來識別一個字元庫、一種字元編碼與一個預設定序。預先定義的
    字元集通常會與某個編碼形式同名，但使用者可以定義其他名稱。例如，字元集 `UTF8`
    通常會識別字元庫 `UCS`、編碼形式 `UTF8`，以及某個預設定序。

你可以把 PostgreSQL 中的「編碼」視為字元集，也可以視為字元編碼形式。兩者的名稱
相同，而且一個資料庫中只能有一個。

<a id="id-1.7.6.11.4"></a>

**表 35.5. `character_sets` 欄位**

<table border="1" class="table" summary="character_sets 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元集目前並未實作為綱要物件，因此此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元集目前並未實作為綱要物件，因此此欄位為 null。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_set_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元集名稱，目前的實作是顯示資料庫編碼的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">character_repertoire</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元庫；顯示 <code class="literal">UCS</code>（若編碼為 <code class="literal">UTF8</code>），否則只顯示編碼名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">form_of_use</code> <code class="type">sql_identifier</code>
</p>
<p>
       字元編碼形式，與資料庫編碼相同
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_collate_catalog</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含預設定序的資料庫名稱（若有識別出任何定序，則一律為目前資料庫）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_collate_schema</code> <code class="type">sql_identifier</code>
</p>
<p>
       包含預設定序的綱要名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">default_collate_name</code> <code class="type">sql_identifier</code>
</p>
<p>
       預設定序的名稱。預設定序是指與目前資料庫的
       <code class="literal">COLLATE</code> 與 <code class="literal">CTYPE</code>
       設定相符的定序。若沒有這樣的定序，則此欄位以及相關的綱要與目錄欄位皆為 null。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/infoschema-character-sets.html)（原文版本：18.6；核對日期：2026-10-18）
