<a id="CATALOG-PG-SUBSCRIPTION"></a>

## 52.54. `pg_subscription` [#](#catalog-pg-subscription) <a href="#catalog-pg-subscription" id="catalog-pg-subscription"></a>

<a id="id-1.10.4.56.2"></a>

目錄 `pg_subscription` 包含所有現有的邏輯複寫訂閱。關於邏輯複寫的更多資訊，請參閱[第 29 章](../../server-administration/logical-replication/README.md)。

與大多數系統目錄不同，`pg_subscription` 由叢集中的所有資料庫共用：每個叢集只有一份 `pg_subscription`，而不是每個資料庫各一份。

一般使用者對欄位 `subconninfo` 的存取權已被撤銷，因為其中可能包含明文密碼。

<a id="id-1.10.4.56.6"></a>

**表 52.54. `pg_subscription` 欄位**

<table border="1" class="table" summary="表 52.54. pg_subscription 欄位"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
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
<code class="structfield">subdbid</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-database.md"><code class="structname">pg_database</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       訂閱所在資料庫的 OID
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subskiplsn</code> <code class="type">pg_lsn</code>
</p>
<p>
       若為有效的 LSN，則為其變更將被略過之交易的結束 LSN；
       否則為 <code class="literal">0/0</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subname</code> <code class="type">name</code>
</p>
<p>
       訂閱的名稱
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subowner</code> <code class="type">oid</code>
       （參照 <a class="link" href="catalog-pg-authid.md"><code class="structname">pg_authid</code></a>.<code class="structfield">oid</code>）
      </p>
<p>
       訂閱的擁有者
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subenabled</code> <code class="type">bool</code>
</p>
<p>
       若為真，表示訂閱已啟用，且應該正在進行複寫
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subbinary</code> <code class="type">bool</code>
</p>
<p>
       若為真，訂閱會要求發佈者以二進位格式傳送資料
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">substream</code> <code class="type">char</code>
</p>
<p>
       控制如何處理進行中交易的串流：
       <code class="literal">f</code> = 不允許串流進行中的交易，
       <code class="literal">t</code> = 將進行中交易的變更寫出到磁碟，
       待交易在發佈者端提交並由訂閱者接收後再一次套用，
       <code class="literal">p</code> = 若有可用的平行套用工作程序，則直接使用它套用變更
       （若沒有可用的工作程序，則與 <code class="literal">t</code> 相同）
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subtwophasestate</code> <code class="type">char</code>
</p>
<p>
       兩階段模式的狀態代碼：
       <code class="literal">d</code> = 已停用，
       <code class="literal">p</code> = 等待啟用，
       <code class="literal">e</code> = 已啟用
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subdisableonerr</code> <code class="type">bool</code>
</p>
<p>
       若為真，當訂閱的某個工作程序偵測到錯誤時，訂閱將被停用
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subpasswordrequired</code> <code class="type">bool</code>
</p>
<p>
       若為真，訂閱將被要求指定密碼以進行身分驗證
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subrunasowner</code> <code class="type">bool</code>
</p>
<p>
       若為真，訂閱將以訂閱擁有者的權限執行
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subfailover</code> <code class="type">bool</code>
</p>
<p>
       若為真，上游資料庫中相關聯的複寫插槽（即主插槽與資料表同步插槽）
       已啟用為可同步至備用伺服器
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subconninfo</code> <code class="type">text</code>
</p>
<p>
       連線至上游資料庫的連線字串
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subslotname</code> <code class="type">name</code>
</p>
<p>
       上游資料庫中複寫插槽的名稱（也用作本地端複寫來源的名稱）；
       null 代表 <code class="literal">NONE</code>
</p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subsynccommit</code> <code class="type">text</code>
</p>
<p>
       訂閱的工作程序所使用的 <code class="varname">synchronous_commit</code>
       設定
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">subpublications</code> <code class="type">text[]</code>
</p>
<p>
       所訂閱之發佈的名稱陣列。這些名稱參照上游資料庫中定義的發佈。
       關於發佈的更多資訊，請參閱<a class="xref" href="../../server-administration/logical-replication/logical-replication-publication.md">第 29.1 節</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">suborigin</code> <code class="type">text</code>
</p>
<p>
       來源（origin）值必須是 <code class="literal">none</code> 或
       <code class="literal">any</code>。預設為 <code class="literal">any</code>。
       若為 <code class="literal">none</code>，訂閱會要求發佈者
       只傳送沒有來源的變更。若為
       <code class="literal">any</code>，發佈者無論變更的來源為何都會傳送。
      </p></td></tr></tbody></table>

<br>

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/catalog-pg-subscription.html)（原文版本：18.6；核對日期：2026-10-17）
