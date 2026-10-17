<a id="CATALOG-PG-TRIGGER"></a>

## 52.58. `pg_trigger` [#](#CATALOG-PG-TRIGGER)

<a id="id-1.10.4.60.2"></a>

目錄 `pg_trigger` 儲存資料表與檢視表上的觸發程序。詳細資訊請參閱 [CREATE TRIGGER](../../reference/sql-commands/sql-createtrigger.md)。

<a id="id-1.10.4.60.4"></a>

**表 52.58. `pg_trigger` 欄位**

<table border="1" class="table" summary="表 52.58. pg_trigger 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">tgrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此觸發程序所在的資料表
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgparentid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-trigger.md"><code class="structname">pg_trigger</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       此觸發程序複製自的父觸發程序（在建立分割區或將分割區附加到分割資料表時會發生）；
       若不是複製而來則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgname</code> <code class="type">name</code>
</p>
<p>
       觸發程序名稱（在同一資料表的觸發程序中必須唯一）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgfoid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-proc.md"><code class="structname">pg_proc</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       要呼叫的函式
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgtype</code> <code class="type">int2</code>
</p>
<p>
       識別觸發程序觸發條件的位元遮罩
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgenabled</code> <code class="type">char</code>
</p>
<p>
       控制觸發程序在哪些 <a class="xref" href="../../server-administration/runtime-config/runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">session_replication_role</a> 模式下觸發。
       <code class="literal">O</code> = 觸發程序在<span class="quote">“<span class="quote">origin</span>”</span>與<span class="quote">“<span class="quote">local</span>”</span>模式下觸發，
       <code class="literal">D</code> = 觸發程序已停用，
       <code class="literal">R</code> = 觸發程序在<span class="quote">“<span class="quote">replica</span>”</span>模式下觸發，
       <code class="literal">A</code> = 觸發程序一律觸發。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgisinternal</code> <code class="type">bool</code>
</p>
<p>
       若觸發程序為內部產生（通常是為了強制執行
       <code class="structfield">tgconstraint</code> 所識別的限制條件），則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgconstrrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       參照完整性限制條件所參照的資料表
       （若觸發程序不是用於參照完整性限制條件，則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgconstrindid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       支援唯一、主鍵、參照完整性或排除限制條件的索引
       （若觸發程序不是用於這幾類限制條件之一，則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgconstraint</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       與觸發程序相關聯的 <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a> 項目
       （若觸發程序不是用於限制條件，則為零）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgdeferrable</code> <code class="type">bool</code>
</p>
<p>
       若限制條件觸發程序可延遲，則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tginitdeferred</code> <code class="type">bool</code>
</p>
<p>
       若限制條件觸發程序初始即延遲（initially deferred），則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgnargs</code> <code class="type">int2</code>
</p>
<p>
       傳給觸發程序函式的引數字串數目
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgattr</code> <code class="type">int2vector</code>
       （參照 <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a>.<code class="structfield">attnum</code>）
      </p>
<p>
       若觸發程序限定於特定欄位，則為欄位編號；否則為空陣列
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgargs</code> <code class="type">bytea</code>
</p>
<p>
       要傳給觸發程序的引數字串，每個都以 NULL 結尾
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgqual</code> <code class="type">pg_node_tree</code>
</p>
<p>
       以 <code class="function">nodeToString()</code>
       表示法呈現的觸發程序 <code class="literal">WHEN</code> 條件運算式樹，若無則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgoldtable</code> <code class="type">name</code>
</p>
<p>
<code class="literal">REFERENCING</code> 子句中 <code class="literal">OLD TABLE</code> 的名稱，
       若無則為 null
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tgnewtable</code> <code class="type">name</code>
</p>
<p>
<code class="literal">REFERENCING</code> 子句中 <code class="literal">NEW TABLE</code> 的名稱，
       若無則為 null
      </p></td></tr></tbody></table>

<br>

目前只有 `UPDATE` 事件支援限定欄位的觸發，因此 `tgattr` 只與該事件類型相關。`tgtype` 也可能包含其他事件類型的位元，但無論 `tgattr` 的內容為何，這些事件類型都被視為作用於整個資料表。

### 注意

當 `tgconstraint` 不為零時，`tgconstrrelid`、`tgconstrindid`、`tgdeferrable` 與 `tginitdeferred` 大致上與所參照的 [`pg_constraint`](catalog-pg-constraint.md) 項目重複。不過，不可延遲的觸發程序有可能與可延遲的限制條件相關聯：外鍵限制條件可以同時擁有一些可延遲的觸發程序與一些不可延遲的觸發程序。

### 注意

若某個關聯在此目錄中有任何觸發程序，`pg_class.relhastriggers` 必須為真。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-trigger.html)（原文版本：18.6；核對日期：2026-10-17）
