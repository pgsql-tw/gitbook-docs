# 27.4.6. 基礎備份進度回報

<a id="BASEBACKUP-PROGRESS-REPORTING"></a>

## 27.4.6. 基礎備份進度回報 [#](#basebackup-progress-reporting) <a href="#basebackup-progress-reporting" id="basebackup-progress-reporting"></a>

<a id="id-1.6.14.9.8.2"></a>

每當像 pg_basebackup 這樣的應用程式
正在取得基礎備份時，
`pg_stat_progress_basebackup`
檢視表中，就會針對每個目前正在執行
`BASE_BACKUP` 複寫命令、
並串流傳輸備份資料的 WAL 傳送程序，各含有一列。
下方的表格，說明了會被回報的資訊，
並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-BASEBACKUP-VIEW"></a>

### 表 27.47. `pg_stat_progress_basebackup` 檢視表 [#](#pg-stat-progress-basebackup-view) <a href="#pg-stat-progress-basebackup-view" id="pg-stat-progress-basebackup-view"></a>

<table border="1" class="table" summary="pg_stat_progress_basebackup View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       某個 WAL 傳送程序的程序 ID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">phase</code> <code class="type">text</code>
</p>
<p>
       目前的處理階段。請參閱<a class="xref" href="#basebackup-phases">表 27.48</a>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backup_total</code> <code class="type">bigint</code>
</p>
<p>
       將被串流傳輸的資料總量。此為預估值，
       在 <code class="literal">streaming database files</code>
       階段開始時回報。請注意，這只是一個近似值，
       因為在 <code class="literal">streaming database files</code>
       階段期間，資料庫可能會發生變化，
       且 WAL 日誌之後也可能會被納入備份中。
       一旦已串流傳輸的資料量超過預估的總大小，
       此值就會與 <code class="structfield">backup_streamed</code>
       永遠保持相同。若在
       <span class="application">pg_basebackup</span>
       中停用了此項預估（也就是指定了
       <code class="literal">--no-estimate-size</code> 選項），
       則此值為 <code class="literal">NULL</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">backup_streamed</code> <code class="type">bigint</code>
</p>
<p>
       已串流傳輸的資料量。此計數器只會在
       階段為 <code class="literal">streaming database files</code>
       或 <code class="literal">transferring wal files</code>
       時才會前進。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespaces_total</code> <code class="type">bigint</code>
</p>
<p>
       將被串流傳輸的資料表空間總數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tablespaces_streamed</code> <code class="type">bigint</code>
</p>
<p>
       已串流傳輸的資料表空間數。此計數器只會在
       階段為 <code class="literal">streaming database files</code>
       時才會前進。
      </p></td></tr></tbody></table>

<br><a id="BASEBACKUP-PHASES"></a>

### 表 27.48. 基礎備份各階段 [#](#basebackup-phases) <a href="#basebackup-phases" id="basebackup-phases"></a>

<table border="1" class="table" summary="Base Backup Phases"><colgroup><col class="col1"/><col class="col2"/></colgroup><thead><tr><th>階段</th><th>說明</th></tr></thead><tbody><tr><td><code class="literal">initializing</code></td><td>
       此 WAL 傳送程序正在準備開始備份。
       預期此階段耗時應非常短暫。
      </td></tr><tr><td><code class="literal">waiting for checkpoint to finish</code></td><td>
       此 WAL 傳送程序目前正在執行
       <code class="function">pg_backup_start</code>，
       以準備取得基礎備份，
       並正在等待備份開始檢查點完成。
      </td></tr><tr><td><code class="literal">estimating backup size</code></td><td>
       此 WAL 傳送程序目前正在預估，
       將以基礎備份形式串流傳輸之資料庫檔案的總量。
      </td></tr><tr><td><code class="literal">streaming database files</code></td><td>
       此 WAL 傳送程序目前正在以基礎備份形式，
       串流傳輸資料庫檔案。
      </td></tr><tr><td><code class="literal">waiting for wal archiving to finish</code></td><td>
       此 WAL 傳送程序目前正在執行
       <code class="function">pg_backup_stop</code>
       以完成此次備份，
       並正在等待此次基礎備份所需的所有 WAL 檔案，
       都成功歸檔完成。
       若在
       <span class="application">pg_basebackup</span>
       中指定了 <code class="literal">--wal-method=none</code>
       或 <code class="literal">--wal-method=stream</code>，
       則此階段完成後，備份就會結束。
      </td></tr><tr><td><code class="literal">transferring wal files</code></td><td>
       此 WAL 傳送程序目前正在傳輸備份期間
       所產生的所有 WAL 日誌。此階段會在
       <code class="literal">waiting for wal archiving to finish</code>
       階段之後發生，前提是在
       <span class="application">pg_basebackup</span>
       中指定了 <code class="literal">--wal-method=fetch</code>。
       此階段完成後，備份就會結束。
      </td></tr></tbody></table>

<br>

[返回 27.4. 進度回報](../progress-reporting.md#progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
