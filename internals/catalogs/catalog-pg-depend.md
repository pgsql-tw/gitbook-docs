<a id="CATALOG-PG-DEPEND"></a>

## 52.18. `pg_depend` [#](#catalog-pg-depend) <a href="#catalog-pg-depend" id="catalog-pg-depend"></a>

<a id="id-1.10.4.20.2"></a>

系統目錄 `pg_depend` 記錄資料庫物件之間的相依關係。這些資訊讓 `DROP` 命令能夠找出哪些其他物件必須由 `DROP CASCADE` 一併刪除，或在 `DROP
RESTRICT` 的情況下阻止刪除。

另請參閱 [`pg_shdepend`](catalog-pg-shdepend.md)，它對涉及在整個資料庫叢集中共享之物件的相依關係執行類似的功能。

<a id="id-1.10.4.20.5"></a>

**表 52.18. `pg_depend` 欄位**

<table border="1" class="table" summary="表 52.18. pg_depend 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位類型
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">classid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       相依物件所在系統目錄的 OID
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
       被參照物件所在系統目錄的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">refobjid</code> <code class="type">oid</code>
       （參照任何 OID 欄位）
      </p>
<p>
       特定被參照物件的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">refobjsubid</code> <code class="type">int4</code>
</p>
<p>
       對於資料表欄位，這是欄位編號（<code class="structfield">refobjid</code> 與 <code class="structfield">refclassid</code> 參照資料表本身）。對於所有其他物件類型，此欄位為零。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">deptype</code> <code class="type">char</code>
</p>
<p>
       定義此相依關係特定語意的代碼；請參閱正文
      </p></td></tr></tbody></table>

<br>

在所有情況下，`pg_depend` 項目都表示：若不同時刪除相依物件，就無法刪除被參照物件。不過，`deptype` 還區分出數種子類型：

`DEPENDENCY_NORMAL` (`n`)
:   分別建立之物件之間的一般關係。相依物件可以被刪除而不影響被參照物件。被參照物件只能透過指定 `CASCADE` 來刪除，此時相依物件也會一併被刪除。範例：資料表欄位對其資料型別具有一般相依。

`DEPENDENCY_AUTO` (`a`)
:   相依物件可以與被參照物件分開刪除，而且在被參照物件被刪除時應該自動刪除（不論是 `RESTRICT` 或 `CASCADE` 模式）。範例：資料表上具名的限制條件會被設為自動相依於該資料表，因此資料表被刪除時，它也會隨之消失。

`DEPENDENCY_INTERNAL` (`i`)
:   相依物件是在建立被參照物件的過程中一併建立的，實際上只是其內部實作的一部分。直接對相依物件執行 `DROP` 會被一律禁止（我們會告訴使用者改為對被參照物件執行 `DROP`）。對被參照物件執行 `DROP` 時，無論是否指定 `CASCADE`，都會自動刪除相依物件。若相依物件因為相依於某個正被移除的其他物件而必須刪除，則它的刪除會轉換為刪除被參照物件，使得相依物件的 `NORMAL` 與 `AUTO` 相依關係，表現得很像是被參照物件的相依關係。範例：檢視表的 `ON SELECT` 規則被設為內部相依於該檢視表，以防止在檢視表仍存在時刪除該規則。該規則的相依關係（例如它所參照的資料表）的作用，就如同它們是檢視表的相依關係。

`DEPENDENCY_PARTITION_PRI` (`P`)<br>`DEPENDENCY_PARTITION_SEC` (`S`)
:   相依物件是在建立被參照物件的過程中一併建立的，實際上只是其內部實作的一部分；不過，與 `INTERNAL` 不同的是，這類被參照物件超過一個。除非這些被參照物件中至少有一個被刪除，否則不得刪除相依物件；只要其中任何一個被刪除，無論是否指定 `CASCADE`，相依物件都應該被刪除。同樣與 `INTERNAL` 不同的是，刪除相依物件所相依的某個其他物件，並不會導致自動刪除任何分割區相依所參照的物件。因此，若該刪除沒有經由其他路徑串聯到這些物件中的至少一個，就會被拒絕。（在大多數情況下，相依物件的所有非分割區相依關係，都與至少一個分割區相依所參照的物件共有，因此這項限制不會導致阻擋任何串聯刪除。）主要與次要分割區相依的行為完全相同，差別只在於錯誤訊息中會優先使用主要相依；因此，一個分割區相依物件應該具有一個主要分割區相依，以及一個或多個次要分割區相依。請注意，分割區相依是在物件通常會有的任何相依關係之外另行建立的，而不是取代這些相依關係。這簡化了 `ATTACH/DETACH PARTITION` 操作：只需要新增或移除分割區相依即可。範例：子分割索引會被設為分割區相依於它所在的分割區資料表以及父分割索引，因此當兩者中任一個被刪除時它就會消失，否則不會。對父索引的相依是主要相依，因此若使用者嘗試刪除子分割索引，錯誤訊息會建議改為刪除父索引（而不是資料表）。

`DEPENDENCY_EXTENSION` (`e`)
:   相依物件是被參照物件這個*擴充功能*的成員（請參閱 [`pg_extension`](catalog-pg-extension.md)）。相依物件只能透過對被參照物件執行 [`DROP EXTENSION`](../../reference/sql-commands/sql-dropextension.md) 來刪除。在功能上，此相依類型的作用與 `INTERNAL` 相依相同，但為了清楚起見並簡化 pg_dump，而將它分開保留。

`DEPENDENCY_AUTO_EXTENSION` (`x`)
:   相依物件不是被參照物件這個擴充功能的成員（因此 pg_dump 不應忽略它），但它沒有該擴充功能就無法運作，而且在擴充功能被刪除時應該自動刪除。相依物件也可以單獨被刪除。在功能上，此相依類型的作用與 `AUTO` 相依相同，但為了清楚起見並簡化 pg_dump，而將它分開保留。

未來可能需要其他相依類型。

請注意，兩個物件完全有可能由超過一個 `pg_depend` 項目連結。例如，子分割索引會同時對其相關聯的分割區資料表具有分割區類型的相依，並對該資料表中它所索引的每個欄位具有自動相依。這種情況表達的是多種相依語意的聯集。若相依物件的任何一個相依關係滿足其自動刪除的條件，就可以不使用 `CASCADE` 刪除它。反過來說，所有相依關係中關於哪些物件必須一起刪除的限制，都必須滿足。

大多數在 initdb 期間建立的物件都被視為「釘住」（pinned）的物件，這表示系統本身相依於它們。因此，它們永遠不允許被刪除。此外，由於知道釘住的物件不會被刪除，相依機制不會費心建立顯示對它們之相依關係的 `pg_depend` 項目。因此，舉例來說，型別為 `numeric` 的資料表欄位在概念上對 `numeric` 資料型別具有 `NORMAL` 相依，但 `pg_depend` 中實際上並不會出現這樣的項目。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-depend.html)（原文版本：18.6；核對日期：2026-10-17）
