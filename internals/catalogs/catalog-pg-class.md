<a id="CATALOG-PG-CLASS"></a>

## 52.11. `pg_class` [#](#catalog-pg-class) <a href="#catalog-pg-class" id="catalog-pg-class"></a>

<a id="id-1.10.4.13.2"></a>

目錄 `pg_class` 描述資料表，以及其他具有欄位或在其他方面
與資料表相似的物件。這包括索引（另請參閱 [`pg_index`](catalog-pg-index.md)）、
序列（另請參閱 [`pg_sequence`](catalog-pg-sequence.md)）、
檢視表、具體化檢視表、複合型別與 TOAST 資料表；
請參閱 `relkind`。
以下當我們指稱所有這些種類的物件時，會稱之為
「關聯」。並非 `pg_class` 的所有
欄位對所有關聯種類都有意義。

<a id="id-1.10.4.13.4"></a>

**表 52.11. `pg_class` 欄位**

<table border="1" class="table" summary="表 52.11. pg_class 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">relname</code> <code class="type">name</code>
</p>
<p>
       資料表、索引、檢視表等的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relnamespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-namespace.md"><code class="structname">pg_namespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       包含此關聯之命名空間的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對應此資料表資料列型別之資料型別的 OID（若有）；
       索引、序列與 TOAST 資料表沒有
       <code class="structname">pg_type</code> 項目，因此為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reloftype</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-type.md"><code class="structname">pg_type</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對於型別化資料表，為其底層複合型別的 OID；
       其他所有關聯則為零
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       關聯的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relam</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-am.md"><code class="structname">pg_am</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       用來存取此資料表或索引的存取方法。
       若關聯是序列或
       沒有磁碟上的檔案，則此欄位無意義，
       但分割資料表除外：對分割資料表而言，若已設定此欄位，
       則當建立命令中未指定存取方法時，在決定新建分割區要使用的存取方法上，
       此欄位優先於 <code class="varname">default_table_access_method</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relfilenode</code> <code class="type">oid</code>
</p>
<p>
       此關聯在磁碟上的檔案名稱；零表示這是一個
       <span class="quote">“<span class="quote">對應式（mapped）</span>”</span>關聯，其磁碟檔案名稱由
       低階狀態決定
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltablespace</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-tablespace.md"><code class="structname">pg_tablespace</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       存放此關聯的資料表空間。
       若為零，則表示使用資料庫的預設資料表空間。
       若關聯沒有磁碟上的檔案，則此欄位無意義，
       但分割資料表除外：對分割資料表而言，這是在建立命令中
       未指定資料表空間時，用來建立分割區的資料表空間。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relpages</code> <code class="type">int4</code>
</p>
<p>
       此資料表在磁碟上的大小，以頁面為單位（每頁大小為
       <code class="symbol">BLCKSZ</code>）。這只是規劃器使用的
       估計值。它由 <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>、
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a> 以及少數 DDL 命令（例如
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>）更新。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltuples</code> <code class="type">float4</code>
</p>
<p>
       資料表中存活資料列的數量。這只是規劃器使用的
       估計值。它由 <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>、
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a> 以及少數 DDL 命令（例如
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>）更新。
       若資料表從未被清理（vacuum）或
       分析過，<code class="structfield">reltuples</code>
       會是 <code class="literal">-1</code>，表示資料列數
       未知。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relallvisible</code> <code class="type">int4</code>
</p>
<p>
       在資料表的可見性對應表中被標記為全部可見的
       頁面數。這只是規劃器使用的
       估計值。它由 <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>、
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a> 以及少數 DDL 命令（例如
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>）更新。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relallfrozen</code> <code class="type">int4</code>
</p>
<p>
       在資料表的可見性對應表中被標記為全部凍結的頁面數。
       這只是用於觸發自動清理（autovacuum）的估計值。它也可以
       與 <code class="structfield">relallvisible</code> 搭配使用，
       用於排程手動清理，以及調校 <a class="link" href="../../server-administration/runtime-config/runtime-config-vacuum.md#runtime-config-vacuum-freezing">VACUUM 的凍結
       行為</a>。

       它由
       <a class="link" href="../../reference/sql-commands/sql-vacuum.md"><code class="command">VACUUM</code></a>、
       <a class="link" href="../../reference/sql-commands/sql-analyze.md"><code class="command">ANALYZE</code></a>
       以及少數 DDL 命令（例如
       <a class="link" href="../../reference/sql-commands/sql-createindex.md"><code class="command">CREATE INDEX</code></a>）更新。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reltoastrelid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       與此資料表關聯之 TOAST 資料表的 OID；若無則為零。
       TOAST 資料表會將大型屬性以<span class="quote">“<span class="quote">行外（out of line）</span>”</span>方式存放在
       次要資料表中。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhasindex</code> <code class="type">bool</code>
</p>
<p>
       若此為資料表且具有（或最近曾具有）任何索引，則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relisshared</code> <code class="type">bool</code>
</p>
<p>
       若此資料表由叢集中所有資料庫共用，則為真。只有
       某些系統目錄（例如 <a class="link" href="catalog-pg-database.md"><code class="structname">pg_database</code></a>）
       是共用的。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relpersistence</code> <code class="type">char</code>
</p>
<p>
<code class="literal">p</code> = 永久資料表／序列，<code class="literal">u</code> = 無日誌資料表／序列，
       <code class="literal">t</code> = 暫存資料表／序列
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relkind</code> <code class="type">char</code>
</p>
<p>
<code class="literal">r</code> = 一般資料表，
       <code class="literal">i</code> = 索引，
       <code class="literal">S</code> = 序列，
       <code class="literal">t</code> = TOAST 資料表，
       <code class="literal">v</code> = 檢視表，
       <code class="literal">m</code> = 具體化檢視表，
       <code class="literal">c</code> = 複合型別，
       <code class="literal">f</code> = 外部資料表，
       <code class="literal">p</code> = 分割資料表，
       <code class="literal">I</code> = 分割索引
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relnatts</code> <code class="type">int2</code>
</p>
<p>
       關聯中使用者欄位的數量（不計系統欄位）。
       <a class="link" href="catalog-pg-attribute.md"><code class="structname">pg_attribute</code></a> 中必須有
       這麼多筆對應的項目。另請參閱
       <code class="structname">pg_attribute</code>.<code class="structfield">attnum</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relchecks</code> <code class="type">int2</code>
</p>
<p>
       資料表上 <code class="literal">CHECK</code> 限制條件的數量；請參閱
       <a class="link" href="catalog-pg-constraint.md"><code class="structname">pg_constraint</code></a> 目錄
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhasrules</code> <code class="type">bool</code>
</p>
<p>
       若資料表具有（或曾經具有）規則，則為真；請參閱
       <a class="link" href="catalog-pg-rewrite.md"><code class="structname">pg_rewrite</code></a> 目錄
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhastriggers</code> <code class="type">bool</code>
</p>
<p>
       若資料表具有（或曾經具有）觸發程序，則為真；請參閱
       <a class="link" href="catalog-pg-trigger.md"><code class="structname">pg_trigger</code></a> 目錄
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relhassubclass</code> <code class="type">bool</code>
</p>
<p>
       若資料表或索引具有（或曾經具有）任何繼承子資料表或分割區，則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relrowsecurity</code> <code class="type">bool</code>
</p>
<p>
       若資料表已啟用資料列層級安全性，則為真；請參閱
       <a class="link" href="catalog-pg-policy.md"><code class="structname">pg_policy</code></a> 目錄
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relforcerowsecurity</code> <code class="type">bool</code>
</p>
<p>
       若資料列層級安全性（啟用時）也會套用於資料表擁有者，則為真；請參閱
       <a class="link" href="catalog-pg-policy.md"><code class="structname">pg_policy</code></a> 目錄
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relispopulated</code> <code class="type">bool</code>
</p>
<p>
       若關聯已填入資料，則為真（除了某些具體化檢視表之外，
       所有關聯皆為真）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relreplident</code> <code class="type">char</code>
</p>
<p>
       用來構成資料列<span class="quote">“<span class="quote">複寫識別（replica identity）</span>”</span>的欄位：
       <code class="literal">d</code> = 預設（主鍵，若有），
       <code class="literal">n</code> = 無，
       <code class="literal">f</code> = 所有欄位，
       <code class="literal">i</code> = 設定了
       <code class="structfield">indisreplident</code> 的索引（若所使用的索引
       已被移除，則等同於「無」）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relispartition</code> <code class="type">bool</code>
</p>
<p>
       若資料表或索引是分割區，則為真
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relrewrite</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-class.md"><code class="structname">pg_class</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       對於在需要改寫資料表的 DDL 操作期間正在寫入的新關聯，
       此欄位包含原始關聯的 OID；
       否則為零。該狀態只在內部可見；對於使用者可見的關聯，
       此欄位不應該包含零以外的任何值。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relfrozenxid</code> <code class="type">xid</code>
</p>
<p>
       此資料表中，在此值之前的所有交易 ID 都已被替換為永久的
       （<span class="quote">“<span class="quote">凍結（frozen）</span>”</span>）交易 ID。這用於追蹤
       資料表是否需要清理，以防止交易
       ID 回捲，或讓 <code class="literal">pg_xact</code> 得以縮減。若關聯不是資料表，
       則為零（<code class="symbol">InvalidTransactionId</code>）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relminmxid</code> <code class="type">xid</code>
</p>
<p>
       此資料表中，在此值之前的所有 multixact ID 都已被替換為
       交易 ID。這用於追蹤
       資料表是否需要清理，以防止 multixact ID
       回捲，或讓 <code class="literal">pg_multixact</code> 得以縮減。若關聯不是資料表，
       則為零（<code class="symbol">InvalidMultiXactId</code>）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relacl</code> <code class="type">aclitem[]</code>
</p>
<p>
       存取權限；詳細資訊請參閱<a class="xref" href="../../the-sql-language/ddl/ddl-priv.md">第 5.8 節</a>
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">reloptions</code> <code class="type">text[]</code>
</p>
<p>
       存取方法特定的選項，以 <span class="quote">“<span class="quote">keyword=value</span>”</span> 字串表示
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relpartbound</code> <code class="type">pg_node_tree</code>
</p>
<p>
       若資料表是分割區（請參閱 <code class="structfield">relispartition</code>），
       則為分割區邊界的內部表示形式
      </p></td></tr></tbody></table>

<br>

`pg_class` 中有幾個布林旗標是以延遲方式
維護的：若為真是正確的狀態，就保證它們為真，但
當條件不再成立時，它們可能不會立即重設為假。
例如，`relhasindex` 由
[`CREATE INDEX`](../../reference/sql-commands/sql-createindex.md) 設定，但絕不會被
[`DROP INDEX`](../../reference/sql-commands/sql-dropindex.md) 清除。而是由 [`VACUUM`](../../reference/sql-commands/sql-vacuum.md) 在發現資料表沒有索引時
清除 `relhasindex`。這種
安排可避免競爭條件並改善並行性。

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-class.html)（原文版本：18.6；核對日期：2026-10-17）
