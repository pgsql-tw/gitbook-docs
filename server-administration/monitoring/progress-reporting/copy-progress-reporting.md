# 27.4.3. COPY 進度回報

<a id="COPY-PROGRESS-REPORTING"></a>

## 27.4.3. COPY 進度回報 [#](#copy-progress-reporting) <a href="#copy-progress-reporting" id="copy-progress-reporting"></a>

<a id="id-1.6.14.9.5.2"></a>

每當 `COPY` 正在執行時，
`pg_stat_progress_copy` 檢視表中，
就會針對每個目前正在執行 `COPY` 命令的後端，
各含有一列。下方的表格，
說明了會被回報的資訊，並提供如何解讀這些資訊的說明。

<a id="PG-STAT-PROGRESS-COPY-VIEW"></a>

### 表 27.42. `pg_stat_progress_copy` 檢視表 [#](#pg-stat-progress-copy-view) <a href="#pg-stat-progress-copy-view" id="pg-stat-progress-copy-view"></a>

<table border="1" class="table" summary="pg_stat_progress_copy View"><colgroup><col/></colgroup><thead><tr><th class="catalog_table_entry"><p class="column_definition">
       欄位型別
      </p>
<p>
       說明
      </p></th></tr></thead><tbody><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">pid</code> <code class="type">integer</code>
</p>
<p>
       後端程序的 ID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datid</code> <code class="type">oid</code>
</p>
<p>
       此後端所連線之資料庫的 OID。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">datname</code> <code class="type">name</code>
</p>
<p>
       此後端所連線之資料庫的名稱。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">relid</code> <code class="type">oid</code>
</p>
<p>
       正在對其執行 <code class="command">COPY</code> 命令之資料表的
       OID。此值設為 <code class="literal">0</code>，適用於複製來源為
       <code class="command">SELECT</code> 查詢的情況。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">command</code> <code class="type">text</code>
</p>
<p>
       目前正在執行的命令：<code class="literal">COPY FROM</code>，
       或 <code class="literal">COPY TO</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">type</code> <code class="type">text</code>
</p>
<p>
       讀取或寫入資料所使用的 I/O 類型：
       <code class="literal">FILE</code>、<code class="literal">PROGRAM</code>、
       <code class="literal">PIPE</code>（用於 <code class="command">COPY FROM STDIN</code> 與
       <code class="command">COPY TO STDOUT</code>），
       或 <code class="literal">CALLBACK</code>
       （例如用於邏輯複寫中初始資料表同步時）。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bytes_processed</code> <code class="type">bigint</code>
</p>
<p>
       <code class="command">COPY</code> 命令已處理的位元組數。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">bytes_total</code> <code class="type">bigint</code>
</p>
<p>
       <code class="command">COPY FROM</code> 命令來源檔案的大小，
       以位元組表示。若無法取得，則設為
       <code class="literal">0</code>。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_processed</code> <code class="type">bigint</code>
</p>
<p>
       <code class="command">COPY</code> 命令已處理的資料列數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_excluded</code> <code class="type">bigint</code>
</p>
<p>
       因被 <code class="command">WHERE</code> 子句（此子句屬於
       <code class="command">COPY</code> 命令）排除，而未被處理的
       資料列數量。
      </p></td></tr><tr><td class="catalog_table_entry"><p class="column_definition">
<code class="structfield">tuples_skipped</code> <code class="type">bigint</code>
</p>
<p>
       因含有格式錯誤的資料而被略過的資料列數量。
       此計數器只會在
       非 <code class="literal">stop</code> 的值被指定給
       <code class="literal">ON_ERROR</code> 選項時才會前進。
      </p></td></tr></tbody></table>

<br>

[返回 27.4. 進度回報](../progress-reporting.md#progress-reporting)

---

原文：[PostgreSQL 18.6 Documentation](https://www.postgresql.org/docs/18/progress-reporting.html)（原文版本：18.6；核對日期：2026-09-26）
