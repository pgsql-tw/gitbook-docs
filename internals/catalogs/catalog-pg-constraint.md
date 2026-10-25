<a id="CATALOG-PG-CONSTRAINT"></a>

## 52.13. `pg_constraint` [#](#catalog-pg-constraint) <a href="#catalog-pg-constraint" id="catalog-pg-constraint"></a>

<a id="id-1.10.4.15.2"></a>

目錄 `pg_constraint` 儲存資料表上的檢查、非空值、
主鍵、唯一、外鍵與排除限制條件。
（欄位限制條件不會被特別處理。每個欄位限制條件都
等同於某個資料表限制條件。）

使用者定義的限制條件觸發程序（以 [`CREATE CONSTRAINT TRIGGER`](../../reference/sql-commands/sql-createtrigger.md) 建立）也會在此資料表中產生一筆項目。

網域上的檢查限制條件也儲存在這裡。

<a id="id-1.10.4.15.6"></a>

**表 52.13. `pg_constraint` 欄位**

<table border="1" class="table" summary="表 52.13. pg_constraint 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">conname</code> <code class="type">name</code>
</p>
<p>
       限制條件名稱（不一定唯一！）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">connamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此限制條件之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">contype</code> <code class="type">char</code>
</p>
<p>
<code class="literal">c</code> = 檢查限制條件，
       <code class="literal">f</code> = 外鍵限制條件，
       <code class="literal">n</code> = 非空值限制條件，
       <code class="literal">p</code> = 主鍵限制條件，
       <code class="literal">u</code> = 唯一限制條件，
       <code class="literal">t</code> = 限制條件觸發程序，
       <code class="literal">x</code> = 排除限制條件
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">condeferrable</code> <code class="type">bool</code>
</p>
<p>
       此限制條件是否可延遲？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">condeferred</code> <code class="type">bool</code>
</p>
<p>
       此限制條件是否預設為延遲？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conenforced</code> <code class="type">bool</code>
</p>
<p>
       此限制條件是否強制執行？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">convalidated</code> <code class="type">bool</code>
</p>
<p>
       此限制條件是否已驗證？
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此限制條件所在的資料表；若不是資料表限制條件則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">contypid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此限制條件所在的網域；若不是網域限制條件則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conindid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若此限制條件是唯一、主鍵、外鍵或排除限制條件，
       則為支援此限制條件的索引；否則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conparentid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若此為分割區上的限制條件，則為上層分割資料表中
       對應的限制條件；否則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若為外鍵，則為被參照的資料表；否則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confupdtype</code> <code class="type">char</code>
</p>
<p>
       外鍵更新動作代碼：
       <code class="literal">a</code> = 無動作（NO ACTION），
       <code class="literal">r</code> = 限制（RESTRICT），
       <code class="literal">c</code> = 串聯（CASCADE），
       <code class="literal">n</code> = 設為 NULL（SET NULL），
       <code class="literal">d</code> = 設為預設值（SET DEFAULT）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confdeltype</code> <code class="type">char</code>
</p>
<p>
       外鍵刪除動作代碼：
       <code class="literal">a</code> = 無動作（NO ACTION），
       <code class="literal">r</code> = 限制（RESTRICT），
       <code class="literal">c</code> = 串聯（CASCADE），
       <code class="literal">n</code> = 設為 NULL（SET NULL），
       <code class="literal">d</code> = 設為預設值（SET DEFAULT）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confmatchtype</code> <code class="type">char</code>
</p>
<p>
       外鍵比對類型：
       <code class="literal">f</code> = 完全（FULL），
       <code class="literal">p</code> = 部分（PARTIAL），
       <code class="literal">s</code> = 簡單（SIMPLE）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conislocal</code> <code class="type">bool</code>
</p>
<p>
       此限制條件是在該關聯上本地定義的。請注意，一個
       限制條件可以同時是本地定義且繼承而來的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">coninhcount</code> <code class="type">int2</code>
</p>
<p>
       此限制條件擁有的直接繼承祖先數。
       祖先數不為零的
       限制條件既不能被移除，也不能被重新命名。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">connoinherit</code> <code class="type">bool</code>
</p>
<p>
       此限制條件是在該關聯上本地定義的。它是一個
       不可繼承的限制條件。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conperiod</code> <code class="type">bool</code>
</p>
<p>
       此限制條件是以 <code class="literal">WITHOUT OVERLAPS</code>
       （用於主鍵與唯一限制條件）或 <code class="literal">PERIOD</code>
       （用於外鍵）定義的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conkey</code> <code class="type">int2[]</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       若為資料表限制條件（包括外鍵，但不包括限制條件
       觸發程序），則為受限制的欄位清單
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confkey</code> <code class="type">int2[]</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       若為外鍵，則為被參照的欄位清單
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conpfeqop</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若為外鍵，則為用於 PK = FK 比較的相等運算子清單
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conppeqop</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若為外鍵，則為用於 PK = PK 比較的相等運算子清單
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conffeqop</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若為外鍵，則為用於 FK = FK 比較的相等運算子清單
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">confdelsetcols</code> <code class="type">int2[]</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       若為刪除動作是 <code class="literal">SET NULL</code> 或 <code class="literal">SET
       DEFAULT</code> 的外鍵，則為將被更新的欄位。
       若為 null，則所有參照欄位都會被更新。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conexclop</code> <code class="type">oid[]</code>
       （參照 <a class="link" href="catalog-pg-operator.md"><code class="structname">pg_operator</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       若為排除限制條件或 <code class="literal">WITHOUT OVERLAPS</code>
       主鍵／唯一限制條件，則為各欄位的排除運算子清單。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">conbin</code> <code class="type">pg_node_tree</code>
</p>
<p>
       若為檢查限制條件，則為該運算式的內部表示形式。
       （建議使用
       <code class="function">pg_get_constraintdef()</code> 來擷取
       檢查限制條件的定義。）
      </p></td></tr></tbody></table>

<br>

對於排除限制條件，`conkey`
只對屬於簡單欄位參照的限制條件元素有用。
其他情況下，`conkey` 中會出現零，
必須查閱相關聯的索引，才能找出受限制的
運算式。（因此 `conkey` 的內容與該索引的
[`pg_index`](catalog-pg-index.md).`indkey`
相同。）

### 注意

`pg_class.relchecks` 需要與此資料表中
針對每個關聯所找到的檢查限制條件項目數
一致。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-constraint.html)（原文版本：18.6；核對日期：2026-10-17）
